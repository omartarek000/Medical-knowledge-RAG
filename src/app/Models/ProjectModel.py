from .BaseDataModel import BaseDataModel
from src.app.Models.db_schemes.project import Project
from src.app.Models.enums.DataBaseEnum import DataBaseEnum
from motor.motor_asyncio import AsyncIOMotorDatabase

class ProjectModel(BaseDataModel):
    
    def __init__(self, _db_client : AsyncIOMotorDatabase):
        super().__init__(_db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]



    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])
            
    @classmethod
    async def create_instance(cls , db_client : AsyncIOMotorDatabase):
        instance = cls(db_client)
        await instance.init_collection()
        return instance


    async def create_project(self,Project : Project):
        result = await self.collection.insert_one(Project.dict())
        Project._id = result.inserted_id

        return Project

    async def get_project_create_one(self,_project_name : str):
        record = await self.collection.find_one({"project_name" : _project_name})
        if record:
            return Project(**record)
        else:
            project_created = Project(project_name=_project_name)
            project_created = await self.create_project(project_created)
            return project_created

    async def get_all_projects(self , page : int = 1 , page_size : int = 10):
        total_documents  = await self.collection.count_documents({})
        skip = (page - 1) * page_size
        cursor = self.collection.find().skip(skip).limit(page_size)
        total_pages = (total_documents + page_size - 1) // page_size
        projects = [Project(**doc) async for doc in cursor]
        return projects , total_pages

    