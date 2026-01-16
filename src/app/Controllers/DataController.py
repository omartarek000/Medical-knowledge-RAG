from src.app.Controllers.BaseController import BaseController
from fastapi import UploadFile , HTTPException 
from .ProjectController import ProjectController
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.scaler = 1024 * 1024 


    def validate_file(self , file : UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type is not allowed."
            )
        if file.size is not None and file.size > self.app_settings.FILE_ALLOWED_MAX_SIZE_MB * self.scaler:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds the allowed limit of {self.app_settings.FILE_ALLOWED_MAX_SIZE_MB} MB."
            )


    def generate_unique_filepath(self , original_filename : str , project_id : str):
        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)
        clean_filename = self.clean_filename(original_filename)
        new_file_path = os.path.join(project_path , random_filename + "_" + clean_filename)

        # recursively call this function until a unique filename is generated
        if os.path.exists(new_file_path):
            return self.generate_unique_filename(original_filename , project_id)
        return new_file_path , random_filename + "_" + clean_filename
    

    def clean_filename(self , original_filename : str):
        return original_filename.replace(" ", "_")
    

