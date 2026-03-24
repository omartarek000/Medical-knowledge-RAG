from .BaseDataModel import BaseDataModel
from src.app.Models.db_schemes.DataChunk import DataChunk
from src.app.Models.enums.DataBaseEnum import DataBaseEnum
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId
from pymongo import InsertOne

class DataChunkModel(BaseDataModel):
    
    def __init__(self, _db_client : AsyncIOMotorDatabase):
        super().__init__(_db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_DATA_CHUNK_NAME.value]

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_DATA_CHUNK_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_DATA_CHUNK_NAME.value]
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])

    @classmethod
    async def create_instance(cls , db_client : AsyncIOMotorDatabase):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def create_data_chunk(self, data_chunk: DataChunk):
        result = await self.collection.insert_one(data_chunk.dict())
        data_chunk._id = result.inserted_id
        return data_chunk


    async def get_chunk (self , chunk_id :str):
        record = await self.collection.find_one({"_id" : ObjectId(chunk_id)})
        if record:
            return DataChunk(**record)
        else:
            return None

    async def insert_many_chunks(self , data_chunks : list[DataChunk] , batch_size : int = 100):
        total_inserted = 0
        for i in range(0 , len(data_chunks) , batch_size):
            batch = data_chunks[i:i+batch_size]
            operations = [InsertOne(chunk.dict()) for chunk in batch]
            result = await self.collection.bulk_write(operations)
            total_inserted += result.inserted_count
        

        return True, total_inserted




    async def delete_by_project_id(self , project_id : ObjectId):
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count

    
    