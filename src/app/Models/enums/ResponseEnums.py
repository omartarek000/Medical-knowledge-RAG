from enum import Enum

class ResponseEnums(Enum):
    
    FILE_VALIDATION_ERROR = "File validation error"
    FILE_TYPE_NOT_ALLOWED = "File type is not allowed."
    FILE_SIZE_EXCEEDED = "File size exceeds the allowed limit."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
