from pydantic_settings import BaseSettings , SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "default-app"
    APP_VERSION: str = "1.0.0"
    OPENAI_API_KEY: str = ""
    FILE_ALLOWED_EXTENSIONS: list = []
    FILE_ALLOWED_SIZE_MB: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
