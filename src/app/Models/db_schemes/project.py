from pydantic import BaseModel , Field , validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias='_id')
    project_name: str = Field(..., min_length=1)
    
    @validator("project_name")
    def validate_project_name(cls, value: str):
        if not value.isalnum():
            raise ValueError("project_name must be alphanumeric")
        return value
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True  