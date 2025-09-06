import secrets
from typing import Any, Optional

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    PROJECT_NAME: str = Field(default="FastAPI MongoDB Starter")
    API_V1_STR: str = Field(default="/api/v1")
    DEBUG: bool = Field(default=False)
    
    # Security
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALLOWED_HOSTS: list[str] = Field(default=["*"])
    
    # MongoDB
    MONGODB_URL: Optional[str] = Field(default=None)
    MONGO_HOST: str = Field(default="localhost")
    MONGO_PORT: int = Field(default=27017)
    MONGO_USER: str = Field(default="")
    MONGO_PASSWORD: str = Field(default="")
    MONGO_DB: str = Field(default="fastapi")
    
    # Connection pool
    MAX_CONNECTIONS_COUNT: int = Field(default=10)
    MIN_CONNECTIONS_COUNT: int = Field(default=10)
    
    # Collections
    MOVIE_COLLECTION: str = Field(default="movies")
    
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [host.strip() for host in v.split(",") if host.strip()]
        return v
    
    @model_validator(mode="after")
    def build_mongodb_url(self) -> "Settings":
        if not self.MONGODB_URL:
            if self.MONGO_USER and self.MONGO_PASSWORD:
                self.MONGODB_URL = (
                    f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@"
                    f"{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
                )
            else:
                self.MONGODB_URL = (
                    f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
                )
        return self
    
    @field_validator("SECRET_KEY", mode="after")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if v == "secret key for project":
            raise ValueError(
                "SECRET_KEY must be changed from default value! "
                "Generate a new one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v


settings = Settings()