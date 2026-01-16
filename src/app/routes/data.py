from fastapi import APIRouter , Depends , UploadFile
from src.app.helpers.config import get_settings , Settings
from src.app.Controllers import DataController, ProjectController, ProcessController
import aiofiles
import os
from src.app.Models.enums import ResponseEnums
from fastapi import HTTPException 
import logging
from src.app.routes.schemes.data import ProcessRequest


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
    file_path , filename = controller.generate_unique_filepath(file.filename, project_id)
    file_path = os.path.join(project_dir_path, filename)

    try:
        async with aiofiles.open(file_path, 'wb') as f: 
            while content := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(content)
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ResponseEnums.FILE_UPLOAD_FAILED}")

    return {"message": ResponseEnums.FILE_UPLOAD_SUCCESS
    , "filename" : filename}


@data_router.post("/process/{project_id}")
async def process_data(project_id : str , request : ProcessRequest):
    file_id = request.file_id

    process_controller = ProcessController(project_id)
    file_content = process_controller.get_file_content(file_id)
    chunks = process_controller.process_document(file_content=file_content , file_id=file_id ,
                chunk_size=request.chunk_size , chunk_overlap=request.overlap_size)
    
    if chunks is None or len(chunks) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ResponseEnums.FILE_PROCESSING_FAILED}")
    else:
        return {"message" : ResponseEnums.FILE_PROCESSING_SUCCESS, "file_id" : file_id  , "chunks" : chunks}

    
