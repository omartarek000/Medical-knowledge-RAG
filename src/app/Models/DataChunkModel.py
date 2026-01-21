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
        for i in range(0 , len(data_chunks) , batch_size):
            batch = data_chunks[i:i+batch_size]
            operations = [InsertOne(chunk.dict()) for chunk in batch]
            await self.collection.bulk_write(operations)
        

        return True

    
    