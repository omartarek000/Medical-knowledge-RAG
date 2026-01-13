from src.app.Controllers.BaseController import BaseController
from fastapi import UploadFile , HTTPException , status


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



