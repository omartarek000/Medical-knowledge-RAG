from fastapi import APIRouter , Depends , UploadFile
from src.app.helpers.config import get_settings , Settings
from src.app.Controllers.DataController import DataController
from src.app.Controllers.ProjectController import ProjectController
import aiofiles
import os
from src.app.Models.enums import ResponseEnums
from fastapi import HTTPException 
import logging


logger = logging.getLogger("error_logger")

data_router = APIRouter(
    prefix="/api/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id : str , file : UploadFile , app_settings : Settings = Depends(get_settings)
                      , controller : DataController = Depends(DataController)):
    
    controller.validate_file(file)
    
    project_dir_path = ProjectController().get_project_path(project_id)
    file_path = os.path.join(project_dir_path, controller.generate_unique_filename(file.filename, project_id))

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file.file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE))
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ResponseEnums.FILE_UPLOAD_FAILED}")

    return {"message": ResponseEnums.FILE_UPLOAD_SUCCESS}

