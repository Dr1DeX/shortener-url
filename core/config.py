import os
from uuid import uuid4

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Конфиг для приложения, подбирает .env файл и перезаписывает переменные, если имеются такие же тут,
    """

    # APP
    ENV: str = "development"

    # # FastAPI
    MICROSERVICE_NAME: str = "shortener"  # CHANGEME
    APP_HOST: str = "localhost"
    APP_PORT: int = 8889

    APP_UNIQUE_ID: str = str(uuid4().hex[:10])

    # # LOGGING
    DEBUG: bool = True

    # Databases
    # # Postgresql/sqlite3
    DB_PATH: str = "data/betronic.db"

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.DB_PATH}"


class DevelopmentConfig(Config):
    DATABASE_ECHO: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config() -> Config:
    env = os.getenv("ENV", "local")
    config_type = {
        "local": DevelopmentConfig(),
        "production": ProductionConfig(),
    }

    return config_type[env]


config: Config = get_config()
