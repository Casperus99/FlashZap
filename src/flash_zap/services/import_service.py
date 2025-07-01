from rich import print
import json
from json import JSONDecodeError
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from flash_zap.core.exceptions import InvalidFileError, ValidationError
from flash_zap.models.card import Card

def _parse_and_validate_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        logging.error(f"File not found at path: {file_path}", exc_info=True)
        raise e
    except JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from file: {file_path}", exc_info=True)
        raise InvalidFileError(f"The file '{file_path}' is not a valid JSON file.") from e

    if not isinstance(data, list):
        logging.error("Validation Error: JSON root is not a list.")
        raise ValidationError("JSON root is not a list.")
    
    logging.info(f"Found {len(data)} cards in the JSON file.")

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logging.error(f"Validation Error: Item at index {i} is not an object.")
            raise ValidationError("JSON list item is not an object.")
        if "front" not in item or "back" not in item:
            logging.error(f"Validation Error: Item at index {i} is missing 'front' or 'back' key.")
            raise ValidationError("Missing 'front' or 'back' key in object.")
        if len(item["front"]) > 200 or len(item["back"]) > 200:
            logging.error(f"Validation Error: Item at index {i} exceeds character limit.")
            raise ValidationError("Card content exceeds 200 characters.")

    return data

def _save_cards_to_db(cards_data: List[Dict[str, Any]], db_session: Session):
    """
    Saves a list of card data to the database.
    """
    for card_data in cards_data:
        card = Card(front=card_data["front"], back=card_data["back"])
        db_session.add(card)
    db_session.commit()
    logging.info(f"Successfully saved {len(cards_data)} cards to the database.")

def import_cards_from_json(db_session: Session):
    """
    Orchestrates the import process from a JSON file, handling exceptions.
    """
    logging.info("Starting flashcard import process.")
    try:
        file_path = input("Enter the path to the JSON file: ")
        logging.info(f"Attempting to import from file: {file_path}")
        cards_data = _parse_and_validate_file(file_path)
        _save_cards_to_db(cards_data, db_session)
        print(f"[green]Successfully imported {len(cards_data)} cards.[/green]")
        logging.info("Flashcard import process finished successfully.")
    except FileNotFoundError:
        print(f"[bold red]Error: File not found.[/bold red]")
        logging.warning("Import failed because file was not found.")
    except (InvalidFileError, ValidationError) as e:
        print(f"[bold red]Error: {e}[/bold red]")
        logging.error(f"Import failed due to validation or file error: {e}", exc_info=True)
    except Exception as e:
        print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        logging.critical("An unexpected error occurred during the import process.", exc_info=True) 