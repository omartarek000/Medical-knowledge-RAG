from .BaseDataModel import BaseDataModel
from src.app.Models.db_schemes.asset import Asset
from src.app.Models.enums.DataBaseEnum import DataBaseEnum
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId

class AssetModel(BaseDataModel):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls , db_client : AsyncIOMotorDatabase):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"], name=index["name"], unique=index["unique"])


    async def create_asset(self , asset:Asset):
        result = await self.collection.insert_one(asset.dict(by_alias=True , exclude_unset=True))
        asset.id = result.inserted_id
        return asset


    async def get_all_project_assets(
        self, 
        project_id: str, 
        asset_type: str, 
        limit: int = 100,  # Prevents crashing on massive datasets
        skip: int = 0
        ):
        # Query with safety limits and offset pagination
        cursor = self.collection.find({
            "asset_project_id": project_id,
            "asset_type": asset_type
        }).skip(skip).limit(limit)
        
        records = await cursor.to_list(length=limit)

        # Convert dictionary data into typed Asset objects
        return [
            Asset(**record)
            for record in records
            ]


    async def get_asset_record(self , asset_project_id : str , asset_name : str):
        asset_record = await self.collection.find_one({
            "asset_project_id": asset_project_id,
            "asset_name": asset_name
        })
        if asset_record is None:
            return None
        return Asset(**asset_record)
    