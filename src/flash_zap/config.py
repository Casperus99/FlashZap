"""
Application configuration loading and management.
"""

# Example configuration
# You can load from environment variables, .env files, or other sources.

class Settings:
    """
    Application settings.
    """
    APP_NAME: str = "FlashZap"
    DEBUG: bool = False


settings = Settings()
