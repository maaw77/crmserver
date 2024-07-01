from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from pathlib import Path

# Defining the paths.
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR/'.env', env_file_encoding='utf-8')
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    HOST_DB: str
    PORT_DB: int


config = Settings()
