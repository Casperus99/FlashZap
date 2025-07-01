"""
Application configuration loading and management.
"""

# Example configuration
# You can load from environment variables, .env files, or other sources.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class LoggingSettings(BaseSettings):
    """
    Logging configuration settings.
    """
    log_level: str = "INFO"
    log_file: str = "flash_zap.log"
    log_format: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

class Settings(BaseSettings):
    """
    Application settings, loaded from .env file.
    """
    APP_NAME: str = "FlashZap"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./flashzap.db"
    GEMINI_API_KEY: str = "YOUR_API_KEY_HERE"
    AI_GRADER_MODEL_NAME: str = "gemini-1.5-flash-latest"
    SRS_INTERVALS: List[int] = [1, 3, 7, 14, 30] # in days
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"client_encoding": "utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
