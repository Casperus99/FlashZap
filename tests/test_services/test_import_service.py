from flash_zap.services.import_service import (
    _parse_and_validate_file, 
    _save_cards_to_db,
    import_cards_from_json,
)
from flash_zap.core.exceptions import InvalidFileError, ValidationError
from flash_zap.models.card import Card
import json
import pytest
from unittest.mock import patch, Mock
from sqlalchemy.orm import Session


def test_parse_and_validate_file_with_valid_json_returns_data(tmp_path):
    # Arrange
    file_path = tmp_path / "valid.json"
    expected_data = [{"front": "What is the capital of France?", "back": "Paris"}]
    file_path.write_text(json.dumps(expected_data))

    # Act
    data = _parse_and_validate_file(str(file_path))

    # Assert
    assert data == expected_data


def test_parse_and_validate_file_raises_error_if_file_not_found():
    # Arrange
    non_existent_file = "non_existent_file.json"

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        _parse_and_validate_file(non_existent_file)


def test_parse_and_validate_file_raises_error_for_malformed_json(tmp_path):
    # Arrange
    file_path = tmp_path / "malformed.json"
    file_path.write_text("{'key': 'value'}")  # Malformed JSON

    # Act / Assert
    with pytest.raises(InvalidFileError):
        _parse_and_validate_file(str(file_path))


def test_parse_and_validate_file_raises_error_if_json_not_a_list(tmp_path):
    # Arrange
    file_path = tmp_path / "not_a_list.json"
    file_path.write_text(json.dumps({"key": "value"}))  # JSON object, not a list

    # Act / Assert
    with pytest.raises(ValidationError):
        _parse_and_validate_file(str(file_path))


def test_parse_and_validate_file_raises_error_for_missing_keys(tmp_path):
    # Arrange
    file_path = tmp_path / "missing_keys.json"
    invalid_data = [
        {"front": "Valid front"},  # Missing 'back'
        {"back": "Valid back"}    # Missing 'front'
    ]
    file_path.write_text(json.dumps(invalid_data))

    # Act / Assert
    with pytest.raises(ValidationError):
        _parse_and_validate_file(str(file_path))


def test_parse_and_validate_file_raises_error_for_content_too_long(tmp_path):
    # Arrange
    file_path = tmp_path / "content_too_long.json"
    long_string = "a" * 201
    invalid_data = [
        {"front": long_string, "back": "Valid back"},
        {"front": "Valid front", "back": long_string}
    ]
    file_path.write_text(json.dumps(invalid_data))

    # Act / Assert
    with pytest.raises(ValidationError):
        _parse_and_validate_file(str(file_path))


def test_save_cards_to_database(test_db_session):
    """
    GIVEN: A list of dictionaries with valid card data.
    WHEN: The _save_cards_to_db function is called.
    THEN: The new cards are correctly saved to the database.
    """
    # GIVEN
    cards_data = [
        {"front": "Q1", "back": "A1"},
        {"front": "Q2", "back": "A2"},
    ]
    session = test_db_session

    # WHEN
    _save_cards_to_db(cards_data, session)

    # THEN
    saved_cards = session.query(Card).all()
    assert len(saved_cards) == 2
    assert saved_cards[0].front == "Q1"
    assert saved_cards[0].back == "A1"
    assert saved_cards[1].front == "Q2"
    assert saved_cards[1].back == "A2"


def test_full_import_flow_success(tmp_path, test_db_session, capsys):
    """
    GIVEN: A valid JSON file and a database session.
    WHEN: The user is prompted for a file path and provides a valid one.
    THEN: The cards are imported and a success message is printed.
    """
    # GIVEN
    file_path = tmp_path / "valid_cards.json"
    cards_data = [
        {"front": "Q1", "back": "A1"},
        {"front": "Q2", "back": "A2"},
    ]
    file_path.write_text(json.dumps(cards_data))
    
    # WHEN
    with patch('builtins.input', return_value=str(file_path)):
        import_cards_from_json(test_db_session)

    # THEN
    captured = capsys.readouterr()
    assert "Successfully imported 2 cards." in captured.out
    
    saved_cards = test_db_session.query(Card).all()
    assert len(saved_cards) == 2


def test_full_import_flow_shows_file_not_found_error(capsys):
    """
    GIVEN: A non-existent file path.
    WHEN: The user is prompted and provides the non-existent path.
    THEN: A "File not found" error message is printed.
    """
    # GIVEN
    non_existent_path = "non_existent_file.json"
    mock_session = Mock(spec=Session)

    # WHEN
    with patch('builtins.input', return_value=non_existent_path):
        import_cards_from_json(db_session=mock_session)

    # THEN
    captured = capsys.readouterr()
    assert "Error: File not found." in captured.out


def test_full_import_flow_shows_invalid_format_error(tmp_path, capsys):
    """
    GIVEN: A malformed JSON file.
    WHEN: The user is prompted and provides the path to the malformed file.
    THEN: An "Invalid JSON format" error message is printed.
    """
    # GIVEN
    file_path = tmp_path / "malformed.json"
    file_path.write_text("{not-json}")  # Malformed JSON
    mock_session = Mock(spec=Session)

    # WHEN
    with patch('builtins.input', return_value=str(file_path)):
        import_cards_from_json(db_session=mock_session)

    # THEN
    captured = capsys.readouterr()
    assert "is not a valid JSON file" in captured.out


def test_full_import_flow_shows_missing_key_error(tmp_path, capsys):
    """
    GIVEN: A JSON file with a record missing a key.
    WHEN: The user is prompted and provides the path to the file.
    THEN: An "Invalid record" error message is printed.
    """
    # GIVEN
    file_path = tmp_path / "missing_key.json"
    invalid_data = [{"front": "This card is missing a back"}]
    file_path.write_text(json.dumps(invalid_data))
    mock_session = Mock(spec=Session)

    # WHEN
    with patch('builtins.input', return_value=str(file_path)):
        import_cards_from_json(db_session=mock_session)

    # THEN
    captured = capsys.readouterr()
    assert "Missing 'front' or 'back' key" in captured.out


def test_full_import_flow_shows_content_too_long_error(tmp_path, capsys):
    """
    GIVEN: A JSON file with a record containing content that is too long.
    WHEN: The user is prompted and provides the path to the file.
    THEN: A "Card content exceeds limit" error message is printed.
    """
    # GIVEN
    file_path = tmp_path / "content_too_long.json"
    long_string = "a" * 201
    invalid_data = [{"front": "Valid front", "back": long_string}]
    file_path.write_text(json.dumps(invalid_data))
    mock_session = Mock(spec=Session)

    # WHEN
    with patch('builtins.input', return_value=str(file_path)):
        import_cards_from_json(db_session=mock_session)

    # THEN
    captured = capsys.readouterr()
    assert "Card content exceeds 200 characters" in captured.out


def test_import_valid_json_returns_data(tmp_path):
    """
    GIVEN: A valid JSON file with card data.
    WHEN: The _parse_and_validate_file function is called.
    THEN: The function returns the expected data.
    """
    # Arrange
    file_path = tmp_path / "valid.json"
    expected_data = [{"front": "What is the capital of France?", "back": "Paris"}]
    file_path.write_text(json.dumps(expected_data))

    # Act
    data = _parse_and_validate_file(str(file_path))

    # Assert
    assert data == expected_data
