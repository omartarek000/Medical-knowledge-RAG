from src.app.helpers.config import get_settings , Settings
from src.app.Models.db_schemes.project import Project
from .enums.DataBaseEnum import DataBaseEnum
from motor.motor_asyncio import AsyncIOMotorDatabase

class BaseDataModel:
    def __init__(self, _db_client : AsyncIOMotorDatabase):
        self.db_client = _db_client
        self.settings : Settings = get_settings()

