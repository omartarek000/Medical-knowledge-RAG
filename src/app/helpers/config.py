from pydantic_settings import BaseSettings , SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "default-app"
    APP_VERSION: str = "1.0.0"
    OPENAI_API_KEY: str = ""
    FILE_ALLOWED_TYPES: list = []
    FILE_ALLOWED_MAX_SIZE_MB: int = 10
    PROJECTS_DIR: str = ""
    FILE_DEFAULT_CHUNK_SIZE: int = 512000 #512KB change this as you want 
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DATABASE: str = "MedicalRAG"


    GENERATION_BACKEND: str = "OPENAI"
    EMBEDDING_BACKEND: str = "COHERE"

    OPENAI_URL: str = ""
    OPENAI_API_KEY: str = ""

    GENERATION_MODEL_ID: str = "qwen3.5:9b"
    EMBEDDING_MODEL_ID: str = "bge-m3:567m"
    EMBEDDING_MODEL_SIZE: int = 384

    INPUT_DEFAULT_MAX_CHAR: int = 1024
    GENERATION_DEFAULT_MAX_TOKENS: int = 200
    GENERATION_DEFAULT_TEMP: float = 0.1



    VECTOR_DB_BACKEND: str = "QDRANT"
    VECTOR_DB_PATH: str = "qdrant_db"
    VECTOR_DB_DISTANCE_METHOD: str = "cosine"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
