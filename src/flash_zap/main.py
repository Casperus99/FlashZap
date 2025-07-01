"""
Main module for the FlashZap application.
This module serves as the entry point for the FlashZap program.
"""

import logging
from flash_zap.logger import setup_logging
from flash_zap.tui.main_menu import run_main_menu_loop


def main():
    """
    Main function that serves as the entry point of the application.
    """
    setup_logging()
    logging.info("FlashZap application starting.")
    run_main_menu_loop()
    logging.info("FlashZap application shutting down.")


if __name__ == "__main__":
    main()
