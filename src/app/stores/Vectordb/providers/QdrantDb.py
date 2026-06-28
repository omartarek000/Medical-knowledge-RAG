from qdrant_client import  AsyncQdrantClient , models
from ..VectordbInterface import VectordbInterface
from ..VectordbEnum import DistanceMethodEnums
import logging 
from typing import List 
import uuid


class QdrantDb(VectordbInterface):
    def __init__(self, db_path: str, distance_method: str = DistanceMethodEnums.COSINE.value, vector_size: int = 1536):
        self.db_path = db_path
        self.distance_method = distance_method
        self.vector_size = vector_size
        self.client = None

    async def connect(self):
        try:
            self.client = AsyncQdrantClient(path=self.db_path)
        except Exception as e:
            logging.error(f"Error connecting to QdrantDb: {e}")
            raise e

    async def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

        else:
            logging.info("QdrantDb is not connected")


    async def is_collection_exists(self , collection_name:str)->bool:
        try:
            self.client.collection_exists(collection_name=collection_name)
            return True
        except Exception as e:
            return False

    
    def get_collection_info(self , collection_name:str)->dict:
        return self.client.get_collection(collection_name=collection_name).dict()

    async def delete_collection(self , collection_name:str)->bool:
        
        if not self.is_collection_exists(collection_name):
            logging.info(f"Collection {collection_name} does not exist")
            return False
        else:
            self.client.delete_collection(collection_name=collection_name)
            return True

    async def create_collection(self , collection_name:str , embedding_size:int,):


        if self.is_collection_exists(collection_name):
            logging.info(f"Collection {collection_name} already exists")
            return False

        else:
            self.client.create_collection(
                collection_name=collection_name, 
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=models.Distance[self.distance_method.upper()]
                )
            )
            return True

        return False 


    async def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         record_id: str = None) -> bool: 
        

        if not self.is_collection_exists(collection_name):
            logging.info(f"Collection {collection_name} does not exist")
            return False
        else:
            
            payload = metadata if metadata else {}
            if text:
                payload["text"] = text
            
            record_id = record_id if record_id else str(uuid.uuid4())
            
            try:
                await self.client.upsert(
                    collection_name=collection_name,
                    points=models.PointStruct(
                        id=record_id,
                        vector=vector,
                        payload=payload
                    )
                )

                return True
            except Exception as e:
                logging.error(f"Error inserting vector into QdrantDb: {e}")
                return False


    async def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50) -> bool:

        if not await self.is_collection_exists(collection_name):
            logging.info(f"Collection {collection_name} does not exist")
            return False

        if len(texts) != len(vectors):
            logging.error(f"Mismatch: {len(texts)} texts vs {len(vectors)} vectors")
            return False

        # Default metadata and record_ids if not provided
        if metadata is None:
            metadata = [{}] * len(texts)
        if record_ids is None:
            record_ids = [str(uuid.uuid4()) for _ in range(len(texts))]

        # Build all points
        points = []
        for i in range(len(texts)):
            payload = metadata[i].copy() if metadata[i] else {}
            if texts[i]:
                payload["text"] = texts[i]

            points.append(models.PointStruct(
                id=record_ids[i],
                vector=vectors[i],
                payload=payload
            ))

        # Upsert in batches
        try:
            for i in range(0, len(points), batch_size):
                batch = points[i : i + batch_size]
                await self.client.upsert(
                    collection_name=collection_name,
                    points=batch
                )
            logging.info(f"Inserted {len(points)} vectors into '{collection_name}'")
            return True
        except Exception as e:
            logging.error(f"Error inserting vectors into QdrantDb: {e}")
            return False


    async def search_by_vector(self, collection_name: str, query_vector: list, top_k: int = 5):
        
        if not await self.is_collection_exists(collection_name):
            logging.info(f"Collection {collection_name} does not exist")
            return []
        else:
            try:
                results = await self.client.query_points(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=top_k
                )
                return results
            except Exception as e:
                logging.error(f"Error searching in QdrantDb: {e}")
                return []