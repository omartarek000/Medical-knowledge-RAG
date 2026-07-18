from fastapi import FastAPI
from src.app.routes import base , data , nlp
from motor.motor_asyncio import AsyncIOMotorClient
from src.app.helpers.config import get_settings
from src.app.stores.LLM.LLmProviderFactory import LLmProviderFactory
from src.app.stores.Vectordb.VectordbProviderFactory import VectordbFactory
from src.app.Models.ProjectModel import ProjectModel
from src.app.Models.DataChunkModel import DataChunkModel
from src.app.Models.AssetModel import AssetModel


app = FastAPI()
app_settings = get_settings()

@app.on_event("startup")
async def startup_span():
    app.mongodb_client = AsyncIOMotorClient(app_settings.MONGO_URL)
    app.mongodb = app.mongodb_client[app_settings.MONGO_DATABASE]
    
    llm_factory = LLmProviderFactory()
    vector_db_factory = VectordbFactory(config=app_settings)

    app.generation_client = llm_factory.create_llm_provider(app_settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(app_settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_factory.create_llm_provider(app_settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(app_settings.EMBEDDING_MODEL_ID)

    app.vectordb_client = vector_db_factory.create_provider(app_settings.VECTOR_DB_BACKEND)
    
    app.vectordb_client.connect()

    # Initialize DB collections once at startup
    project_model = ProjectModel(app.mongodb)
    await project_model.init_collection()

    chunk_model = DataChunkModel(app.mongodb)
    await chunk_model.init_collection()

    asset_model = AssetModel(app.mongodb)
    await asset_model.init_collection()


@app.on_event("shutdown")
async def shutdown_span():
    app.mongodb_client.close()
    app.vectordb_client.disconnect()

app.include_router(base.api_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)


