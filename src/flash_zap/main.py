"""
Main module for the FlashZap application.
This module serves as the entry point for the FlashZap program.
"""

from flash_zap.tui.main_menu import run_main_menu_loop


def main():
    """
    Main function that serves as the entry point of the application.
    """
    run_main_menu_loop()


if __name__ == "__main__":
    main()
