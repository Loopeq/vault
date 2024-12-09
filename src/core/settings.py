from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", ".env")


class S3Settings(BaseModel):
    access_key: str
    secret_key: str
    url: str
    bucket: str


class StrategyManagerSettings(BaseModel):
    data: str = "data"
    params: str = "params"


class PostgresSettings(BaseSettings):
    user: str
    password: str
    server: str
    port: str
    db: str
    async_prefix: str
    sync_prefix: str

    @property
    def uri(self) -> str:
        return (
            f"{self.user}:{self.password}@{self.server}:{self.port}/{self.db}"
        )

    @property
    def url_sync(self) -> str:
        return f"{self.sync_prefix}{self.uri}"

    @property
    def url_async(self) -> str:
        return f"{self.async_prefix}{self.uri}"

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthConfig(BaseModel):
    secret: str
    algorithm: str
    expire_token_minute: int


class AdminConfig(BaseModel):
    username: str
    email: str
    password: str


class Settings(BaseSettings):
    auth: AuthConfig
    db: PostgresSettings
    admin: AdminConfig
    strategy_manager: StrategyManagerSettings
    s3: S3Settings

    class Config:
        env_nested_delimiter = "__"
        env_file = env_path
        extra = "ignore"


settings = Settings(_case_sensitive=False)
