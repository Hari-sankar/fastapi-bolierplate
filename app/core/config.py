from pydantic_settings import BaseSettings
from typing import List
from pydantic import Field

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "FastAPI-BoilerPlate"
    APP_ENV: str = "production"
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = Field(default=["*"], alias="ALLOWED_ORIGINS")

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str
    MIGRATION:bool

    # Email
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    # Logging
    LOG_LEVEL: str = "info"
    LOG_FILE: str = "logs/app.log"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
