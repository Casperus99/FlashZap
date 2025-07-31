import logging
import sys
from flash_zap.config import settings

def setup_logging():
    """
    Set up the root logger for the application.
    """
    log_level = settings.logging.log_level.upper()
    log_format = settings.logging.log_format

    # Create console handler only
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Set format for console handler
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)

    # Basic configuration
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            console_handler,
        ]
    )

    # Quieten SQLAlchemy unless we are in DEBUG mode
    if log_level == "DEBUG":
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    else:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info("Logging has been configured.") 