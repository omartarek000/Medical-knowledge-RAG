from src.app.stores.Vectordb.providers import QdrantDb
from .VectordbEnum import VectordbEnum
from src.app.Controllers.BaseController import BaseController



class VectordbFactory:
    def __init__(self , config:dict):
        self.config = config

    def create_provider(self , provider: str ):
        if provider == VectordbEnum.QDRANT.value:
            return QdrantDb(
                db_path = BaseController().get_vector_db_path(provider), 
                distance_method = self.config.VECTOR_DB_DISTANCE_METHOD,
                vector_size = self.config.VECTOR_DB_VECTOR_SIZE
            )
        
        else:
            raise ValueError(f"Invalid vector db provider: {provider}")