import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Panuval Book Store API"
    
    # MySQL database connection settings
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "panuval689")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "panuval_oc3")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # JWT token config
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings()
