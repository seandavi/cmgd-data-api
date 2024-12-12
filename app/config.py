from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_HOST: str
    CLICKHOUSE_DB: str
    CLICKHOUSE_PORT: Optional[int] = 8123

    class Config:
        env_file = ".env"


settings = Settings()
