# GLOBAL CONFIG FOR THE APP

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_parse_none_str="None",
        case_sensitive=True,
        env_ignore_empty=True,
    )


class Config(BaseConfig):
    environment: str = "prod"


class DatabaseConfig(BaseConfig):
    # The driver must be async
    DB_DRIVERNAME: str = "postgresql+asyncpg"
    DB_USERNAME: str = "example"
    DB_PASSWORD: str = "example"
    DB_HOST: str = "localhost"
    DB_PORT: int | None = None
    DB_NAME: str = "example"


database_config = DatabaseConfig()
