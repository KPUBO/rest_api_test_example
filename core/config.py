from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import PostgresDsn

from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = 'localhost'
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/api_v1"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    max_overflow: int = 10
    pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class ApiAuthConfig(BaseModel):
    api_key_name: str
    api_key: str

class TestDBConfig(BaseModel):
    test_database_url: PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    load_dotenv()
    db: DatabaseConfig
    auth: ApiAuthConfig
    test_db: TestDBConfig


settings = Settings()
