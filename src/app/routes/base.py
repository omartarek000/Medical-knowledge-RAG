from fastapi import FastAPI , APIRouter , Depends
from src.app.helpers.config import get_settings , Settings
api_router = APIRouter(
    prefix="/welcome",
    tags=["Base"]
)

@api_router.get("/")
async def welcome(app_settings : Settings = Depends(get_settings)):
    
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"message": f"Welcome to the {app_name}  v{app_version}!"}