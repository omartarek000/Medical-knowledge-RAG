from fastapi import APIRouter , Depends , UploadFile , Request , status
from fastapi.responses import JSONResponse
from src.app.routes.schemes.nlp import PushRequest 
from src.app.Models.ProjectModel import ProjectModel
import logging 



logger = logging.getLogger("uvicorn.error")
nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"]
)


@nlp_router.post("/index/push/{project_id}")
async def index_project(project_id : str , request : Request , push_request : PushRequest):
    
    project_model = ProjectModel(request.app.mongodb)
    project = await project_model.get_project_create_one(project_id)
    
    
    