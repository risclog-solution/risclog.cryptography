from functools import lru_cache
from pydantic_settings import SettingsConfigDict

from risclog.fastapi.config import MetadataSettings


class Settings(MetadataSettings):
    server_name: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
