from fastapi import FastAPI
from src.app.routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient
from src.app.helpers.config import get_settings


app = FastAPI()
app_settings = get_settings()

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = AsyncIOMotorClient(app_settings.MONGO_URL)
    app.mongodb = app.mongodb_client[app_settings.MONGO_DATABASE]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(base.api_router)
app.include_router(data.data_router)


