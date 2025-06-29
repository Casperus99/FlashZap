import os
import readchar

from flash_zap.config import SessionLocal, engine
from flash_zap.models.base import Base
from flash_zap.services.import_service import import_cards_from_json


def display_main_menu():
    """Displays the main menu."""
    return (
        "--- FlashZap Main Menu ---\n"
        "1. Review Due Cards\n"
        "2. Import Flashcards from JSON\n"
        "3. Exit\n"
        "Select an option (1-3)"
    )


def navigate_to_review_session():
    """Placeholder function for the 'Review Session' flow."""
    pass


def _handle_import_json():
    """Handles the JSON import flow."""
    db_session = SessionLocal()
    try:
        import_cards_from_json(db_session)
    finally:
        db_session.close()
    
    input("\\nPress Enter to return to the main menu...")


def handle_menu_input(key):
    """Handles user input for the main menu."""
    if key == '1':
        navigate_to_review_session()
        return "continue"
    elif key == '2':
        _handle_import_json()
        return "continue"
    elif key == '3':
        return "exit"
    else:
        return None


def run_main_menu_loop():
    """Displays the main menu and handles user input."""
    Base.metadata.create_all(bind=engine)
    while True:
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

        print(display_main_menu())

        key = readchar.readkey()

        action = handle_menu_input(key)

        if action == "exit":
            break 