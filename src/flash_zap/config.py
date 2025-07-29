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
    
    # Cloud database settings are now the only option
    CLOUD_DB_HOST: str
    CLOUD_DB_NAME: str
    CLOUD_DB_USER: str
    CLOUD_DB_PASSWORD: str

    # SRS settings
    SRS_LEARNING_RATE: float = 0.1

    # AI settings
    GEMINI_API_KEY: str = "YOUR_API_KEY_HERE"
    AI_GRADER_MODEL_NAME: str = "gemini-2.5-flash-lite-preview-06-17"
    AI_GRADER_PROMPT_TEMPLATE: str = """
You are an AI assistant for a flashcard application. Your task is to evaluate a user's answer to a flashcard question.

You must compare the user's answer to the correct answer (the back of the flashcard) and determine if it is "Correct" or "Incorrect".

**Primary Rule: Semantic Equivalence is Key**
Your primary goal is to check if the user's answer is **semantically equivalent** to the correct answer. If the meaning is the same, the answer is "Correct", even if there are minor grammatical errors, typos, or differences in wording.

**Grading Rules:**

1.  **Grammar and Typos:** Ignore minor grammatical errors (like incorrect noun declension, e.g., "grudzień" vs "grudnia") or small typos, as long as the core meaning of the answer remains clear and unambiguous.
2.  **Keywords and Names:** If a flashcard asks for a specific keyword or name, a spelling mistake can only be accepted if it's a very minor typo that doesn't create confusion with another term (e.g., "Waszyngton" vs "Waszyngtom" is acceptable, but "Bitwa pod Grunwaldem" vs "Bitwa pod Grunwald" is not).
3.  **Dates:** If a flashcard asks for a date, the user may provide it in any valid format. This explicitly includes variations in the grammatical case of the month's name. As long as the day, month, and year are correct, the answer should be marked as "Correct".

Provide a brief, helpful feedback message. If the answer was not fully correct, also provide the correct answer or explain what was missing.

Reply in the polish language.

**Question:** "{question}"
**Correct answer:** "{correct_answer}"
**User's Answer:** "{user_answer}"

**Output format:**
Result: [Correct/Incorrect]
Feedback: [Your feedback here]
"""
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

def get_database_url() -> str:
    """
    Constructs the database URL from the required cloud settings.
    """
    # This function now assumes a cloud connection is always used.
    # The settings class will raise an error if these are not set in the .env file.
    return (
        f"postgresql+psycopg2://{settings.CLOUD_DB_USER}:{settings.CLOUD_DB_PASSWORD}"
        f"@{settings.CLOUD_DB_HOST}/{settings.CLOUD_DB_NAME}"
        f"?sslmode=require"
    )


engine = create_engine(
    get_database_url(),
    # The 'client_encoding' arg is specific to PostgreSQL and will cause errors with SQLite in tests
    # We can check the URL scheme to apply it conditionally.
    connect_args={"client_encoding": "utf8"} if get_database_url().startswith("postgresql") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
