from fastapi import APIRouter , Depends , UploadFile , Request , status
from src.app.helpers.config import get_settings , Settings
from src.app.Controllers import DataController, ProjectController, ProcessController
import aiofiles
import os
from src.app.Models.enums import ResponseEnums , AssetTypeEnum
from fastapi import HTTPException 
import logging
from src.app.routes.schemes.data import ProcessRequest
from src.app.Models.ProjectModel import ProjectModel 
from src.app.Models.DataChunkModel import DataChunkModel
from src.app.Models.db_schemes.DataChunk import DataChunk
from src.app.Models.AssetModel import AssetModel
from src.app.Models.db_schemes.asset import Asset


logger = logging.getLogger("error_logger")

data_router = APIRouter(
    prefix="/api/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request : Request,project_id : str , file : UploadFile , app_settings : Settings = Depends(get_settings)
                      , controller : DataController = Depends(DataController)):

    project_model = await ProjectModel.create_instance(request.app.mongodb)
    project = await project_model.get_project_create_one(project_id)
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


    asset_model = await AssetModel.create_instance(request.app.mongodb)
    asset = Asset(
        asset_project_id=project.id,
        asset_type=file.content_type,
        asset_name=filename,
        asset_path=file_path,
        asset_size=os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset)


    return {"message": ResponseEnums.FILE_UPLOAD_SUCCESS
    , "filename" : asset_record.asset_name,
      "asset record id " : str(asset_record.id)
     }


@data_router.post("/process/{project_id}")
async def process_data(project_id : str , request : ProcessRequest , app_request : Request):

    do_reset = request.do_reset
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size


    project_model = await ProjectModel.create_instance(app_request.app.mongodb) ## connect the fastapi to the database and init indexes
    project = await project_model.get_project_create_one(project_id)
    asset_model = await AssetModel.create_instance(app_request.app.mongodb)

    project_file_id = {}
    if request.file_id:
        asset_record = await asset_model.get_asset_record(project.id , request.file_id)
        if asset_record is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ResponseEnums.FILE_NOT_FOUND.value}")
        project_file_id = {asset_record.id : asset_record.asset_name}
        
    else:

        project_files = await asset_model.get_all_project_assets(project.id , AssetTypeEnum.PDF.value)

        project_file_id =  { 
            record.id : record.asset_name
            for record in project_files
        } 

        if len(project_file_id) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ResponseEnums.FILE_NOT_FOUND.value}")

    data_chunk_model = await DataChunkModel.create_instance(app_request.app.mongodb)

    if do_reset:
        _ = await data_chunk_model.delete_by_project_id(project.id)


    process_controller = ProcessController(project_id)   
    for asset_id , file_id in project_file_id.items():
        
        file_content = process_controller.get_file_content(file_id)

        if file_content is None:
            logger.error(f"Failed to get file content for file_id: {file_id}")
            continue

        chunks = process_controller.process_document(file_content=file_content , file_id=file_id ,
                    chunk_size=request.chunk_size , chunk_overlap=request.overlap_size )
    
        if chunks is None or len(chunks) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ResponseEnums.FILE_PROCESSING_FAILED}")

        file_chunks_records = [
            DataChunk(chunk_text=chunk.page_content, chunk_metadata=chunk.metadata , chunk_order= i + 1 ,
             chunk_project_id= project.id , chunk_asset_id= asset_id)
            for i , chunk in enumerate(chunks)
        ]
        
        try:
            is_inserted, inserted_count = await data_chunk_model.insert_many_chunks(file_chunks_records)
        except Exception as e:
            logger.error(f"Failed to insert chunks: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to insert chunks into the database"
            )

        if not is_inserted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to insert chunks into the database"
            )

        return {
            "status": "success",
            "message": "Document processed successfully",
            "data": {
                "file_id": file_id,
                "project_id": str(project.id),
                "chunks_created": inserted_count,
                "chunk_size": request.chunk_size
            }
        }

    
