from fastapi import  APIRouter , Depends , UploadFile
from src.app.helpers.config import get_settings , Settings
from src.app.Controllers.DataController import DataController


data_router = APIRouter(
    prefix="/api/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id : str , file : UploadFile , app_settings : Settings = Depends(get_settings)
                      , controller : DataController = Depends(DataController)):
    
    controller.validate_file(file)
    return {"message": "File uploaded successfully"}