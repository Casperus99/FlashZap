import pytest
from unittest.mock import patch, Mock
from datetime import date
from flash_zap.models.card import Card

from flash_zap.tui import browse_view

@patch('flash_zap.tui.browse_view.readchar.readkey')
@patch('flash_zap.tui.browse_view.get_card_by_id')
@patch('builtins.input', return_value='123')
def test_show_card_view_prompts_for_id_and_retrieves_card(mock_input, mock_get_card_by_id, mock_readkey):
    """
    Tests that show_card_view prompts for a card ID and attempts to fetch the card.
    """
    mock_session = Mock()
    mock_get_card_by_id.return_value = None # Assume card not found for now

    browse_view.show_card_view(mock_session)

    mock_input.assert_called_once_with("Enter the ID of the card you want to view: ")
    mock_get_card_by_id.assert_called_once_with(mock_session, 123)

@patch('flash_zap.tui.browse_view.readchar.readkey')
@patch('flash_zap.tui.browse_view.get_card_by_id')
@patch('builtins.input', return_value='1') # First input for ID
@patch('builtins.print')
def test_show_card_view_displays_card_details_when_found(mock_print, mock_input, mock_get_card_by_id, mock_readkey):
    """
    Tests that show_card_view displays the details of a found card and waits for input.
    """
    mock_session = Mock()
    test_card = Card(front="Test Front", back="Test Back", mastery_level=3)
    test_card.id = 1
    test_card.next_review_date = date(2025, 1, 1)

    mock_get_card_by_id.return_value = test_card

    browse_view.show_card_view(mock_session)

    # Verify that the card details were printed
    expected_prints = [
        "--- Card Details ---",
        f"ID: {test_card.id}",
        f"Front: {test_card.front}",
        f"Back: {test_card.back}",
        f"Mastery Level: {test_card.mastery_level}",
        f"Next Review: {test_card.next_review_date}",
        "--------------------",
    ]

    actual_prints = [call.args[0] for call in mock_print.call_args_list]
    for expected_print in expected_prints:
        assert expected_print in actual_prints, f"Expected print '{expected_print}' not found."

    # Verify it waits for user input before returning
    mock_print.assert_any_call("\nPress any key to return to the main menu...")
    mock_readkey.assert_called_once()

@patch('flash_zap.tui.browse_view.readchar.readkey')
@patch('flash_zap.tui.browse_view.get_card_by_id')
@patch('builtins.input', return_value='abc') # Invalid ID
@patch('builtins.print')
def test_show_card_view_handles_invalid_id_input(mock_print, mock_input, mock_get_card_by_id, mock_readkey):
    """
    Tests that show_card_view handles non-integer input for the card ID.
    """
    mock_session = Mock()

    browse_view.show_card_view(mock_session)

    mock_print.assert_any_call("Invalid ID. Please enter a number.")
    mock_get_card_by_id.assert_not_called()

@patch('flash_zap.tui.browse_view.readchar.readkey')
@patch('flash_zap.tui.browse_view.get_card_by_id', return_value=None)
@patch('builtins.input', return_value='999') # Valid but non-existent ID
@patch('builtins.print')
def test_show_card_view_handles_card_not_found(mock_print, mock_input, mock_get_card_by_id, mock_readkey):
    """
    Tests that show_card_view displays a 'not found' message for a non-existent card.
    """
    mock_session = Mock()

    browse_view.show_card_view(mock_session)

    mock_print.assert_any_call("Card not found.")
    mock_get_card_by_id.assert_called_once_with(mock_session, 999) 