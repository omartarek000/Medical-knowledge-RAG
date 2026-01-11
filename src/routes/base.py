from fastapi import FastAPI , APIRouter
import os 
api_router = APIRouter(
    prefix="/RAG",
    tags=["NLP"]
)

@api_router.get("/")
async def welcome():
    app_name , app_version = os.getenv("APP_NAME" , "API") , os.getenv("APP_VERSION" , "1.0.0")
    return {"message": f"Welcome to the {app_name}  v{app_version}!"}