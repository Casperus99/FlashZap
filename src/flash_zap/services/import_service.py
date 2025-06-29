from rich import print
import json
from json import JSONDecodeError
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from flash_zap.core.exceptions import InvalidFileError, ValidationError
from flash_zap.models.card import Card

def _parse_and_validate_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise e
    except JSONDecodeError as e:
        raise InvalidFileError(f"The file '{file_path}' is not a valid JSON file.") from e

    if not isinstance(data, list):
        raise ValidationError("JSON root is not a list.")

    for item in data:
        if not isinstance(item, dict):
            raise ValidationError("JSON list item is not an object.")
        if "front" not in item or "back" not in item:
            raise ValidationError("Missing 'front' or 'back' key in object.")
        if len(item["front"]) > 200 or len(item["back"]) > 200:
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

def import_cards_from_json(db_session: Session):
    """
    Orchestrates the import process from a JSON file, handling exceptions.
    """
    try:
        file_path = input("Enter the path to the JSON file: ")
        cards_data = _parse_and_validate_file(file_path)
        _save_cards_to_db(cards_data, db_session)
        print(f"[green]Successfully imported {len(cards_data)} cards.[/green]")
    except FileNotFoundError:
        print(f"[bold red]Error: File not found.[/bold red]")
    except (InvalidFileError, ValidationError) as e:
        print(f"[bold red]Error: {e}[/bold red]")
    except Exception as e:
        print(f"[bold red]An unexpected error occurred: {e}[/bold red]") 