"""
Application configuration loading and management.
"""

# Example configuration
# You can load from environment variables, .env files, or other sources.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings, loaded from .env file.
    """
    APP_NAME: str = "FlashZap"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./flashzap.db"
    GEMINI_API_KEY: str
    AI_GRADER_MODEL_NAME: str = "gemini-1.5-flash-latest"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"client_encoding": "utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
