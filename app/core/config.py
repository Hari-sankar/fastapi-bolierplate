from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "FastAPI-BoilerPlate"
    APP_ENV: str = "production"
    DEBUG: bool = False
    STRUCTURED_LOGGING:bool= True

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

    # CORS 
    CORS_METHOD : list[str] = Field(default=["*"], alias="CORS_METHOD") 
    CORS_ORIGIN : list[str] = Field(default=["*"], alias="CORS_ORIGIN") 
    CORS_HEADER : list[str] = Field(default=["*"], alias="CORS_HEADER") 


    # Logging
    LOG_LEVEL: str = "info"
    LOG_FILE: str = "logs/app.log"
    SAVE_LOG: bool


    # Redis
    REDIS_HOST : str
    REDIS_PORT : str
    REDIS_DB  : str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
