from pydantic import BaseModel , Field , validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(... , min_length=1)
    asset_name: str = Field(... , min_length=1)
    asset_path: str = Field(... , min_length=1)
    asset_size: int = Field(ge=0 , default=None)
    asset_created_at: datetime = Field(default_factory=datetime.now)
    asset_updated_at: datetime = Field(default_factory=datetime.now)
    asset_deleted_at: Optional[datetime] = None
    asset_config: dict  = Field(default=None)



    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("asset_project_id", 1)],
                "name": "asset_project_id_idx",
                "unique" : False
            } ,
            {
                "key" : [
                    ("asset_project_id", 1),
                    ("asset_type", 1),
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_type_name_idx",
                "unique" : True
            }
        ]