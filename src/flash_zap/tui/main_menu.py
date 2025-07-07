import os
import readchar
import logging

from flash_zap.config import SessionLocal, engine
from flash_zap.models.base import Base
from flash_zap.services.import_service import import_cards_from_json
from flash_zap.tui import review_view, browse_view


def display_main_menu():
    """Displays the main menu."""
    return (
        "--- FlashZap Main Menu ---\n"
        "1. Review Due Cards\n"
        "2. Import Flashcards from JSON\n"
        "3. Browse Cards\n"
        "4. Exit\n"
        "Select an option (1-4)"
    )


def navigate_to_review_session():
    """Starts the review session flow."""
    logging.info("Creating DB session for review session.")
    db_session = SessionLocal()
    try:
        review_view.start_review_session(db_session)
    finally:
        db_session.close()
        logging.info("DB session for review session closed.")


def navigate_to_browse_view():
    """Starts the browse card view flow."""
    logging.info("Creating DB session for browse view.")
    db_session = SessionLocal()
    try:
        browse_view.show_card_view(db_session)
    finally:
        db_session.close()
        logging.info("DB session for browse view closed.")


def _handle_import_json():
    """Handles the JSON import flow."""
    logging.info("Creating DB session for JSON import.")
    db_session = SessionLocal()
    try:
        import_cards_from_json(db_session)
    finally:
        db_session.close()
        logging.info("DB session for JSON import closed.")
    
    input("\\nPress Enter to return to the main menu...")


def handle_menu_input(key):
    """Handles user input for the main menu."""
    if key == '1':
        logging.info("User selected 'Review Due Cards' option.")
        navigate_to_review_session()
        return "continue"
    elif key == '2':
        logging.info("User selected 'Import Flashcards from JSON' option.")
        _handle_import_json()
        return "continue"
    elif key == '3':
        logging.info("User selected 'Browse Cards' option.")
        navigate_to_browse_view()
        return "continue"
    elif key == '4':
        logging.info("User selected 'Exit' option.")
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