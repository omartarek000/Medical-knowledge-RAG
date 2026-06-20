from fastapi import FastAPI
from src.app.routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient
from src.app.helpers.config import get_settings
from src.app.stores.LLM.LLmProviderFactory import LLmProviderFactory


app = FastAPI()
app_settings = get_settings()

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = AsyncIOMotorClient(app_settings.MONGO_URL)
    app.mongodb = app.mongodb_client[app_settings.MONGO_DATABASE]
    
    llm_factory = LLmProviderFactory()

    app.generation_client = llm_factory.create_llm_provider(app_settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(app_settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_factory.create_llm_provider(app_settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(app_settings.EMBEDDING_MODEL_ID)


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(base.api_router)
app.include_router(data.data_router)


