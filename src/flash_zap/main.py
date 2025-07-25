"""
Main module for the FlashZap application.
This module serves as the entry point for the FlashZap program.

Note: FlashZap has been migrated to a web interface.
To run the application, use: python run_web.py
"""

import logging
from flash_zap.logger import setup_logging


def main():
    """
    Main function that serves as the entry point of the application.
    
    Note: The terminal interface has been deprecated. 
    Please use the web interface by running: python run_web.py
    """
    setup_logging()
    logging.info("FlashZap terminal interface is deprecated.")
    print("FlashZap has been migrated to a web interface.")
    print("To use FlashZap, please run: python run_web.py")
    print("Then open your browser to http://localhost:8000")


if __name__ == "__main__":
    main()
