from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

current_dir = Path(__file__).resolve().parent.parent
env_path = current_dir.parent / ".env"

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMBEDDINGS_MODEL: str

    model_config = SettingsConfigDict(env_file=env_path)

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()