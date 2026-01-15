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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
