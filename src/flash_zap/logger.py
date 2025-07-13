import logging
import sys
from flash_zap.config import settings

def setup_logging():
    """
    Set up the root logger for the application.
    """
    log_level = settings.logging.log_level.upper()
    log_format = settings.logging.log_format
    log_file = settings.logging.log_file

    # Basic configuration
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
        ]
    )

    # Quieten SQLAlchemy unless we are in DEBUG mode
    if log_level == "DEBUG":
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    else:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info("Logging has been configured.") 