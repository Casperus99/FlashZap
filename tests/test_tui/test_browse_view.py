import pytest
from unittest.mock import patch, Mock, call
from datetime import date
from flash_zap.models.card import Card
from flash_zap.tui import browse_view


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("flash_zap.tui.browse_view.readchar.readkey")
@patch("flash_zap.tui.browse_view.get_card_by_id", return_value=None)
@patch("builtins.input", return_value="123")
def test_show_card_view_prompts_for_id_and_handles_not_found(
    mock_input, mock_get_card_by_id, mock_readkey, mock_clear
):
    """Tests that show_card_view prompts for ID and handles a card not being found."""
    mock_session = Mock()
    browse_view.show_card_view(mock_session)

    mock_clear.assert_called_once()
    mock_input.assert_called_once_with("Enter the ID of the card you want to view: ")
    mock_get_card_by_id.assert_called_once_with(mock_session, 123)
    mock_readkey.assert_called_once()  # For "Press any key to continue"


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("flash_zap.tui.browse_view.readchar.readkey")
@patch("builtins.input", return_value="abc")
def test_show_card_view_handles_invalid_id_input(mock_input, mock_readkey, mock_clear):
    """Tests that show_card_view handles non-integer input for the card ID."""
    mock_session = Mock()
    browse_view.show_card_view(mock_session)
    mock_clear.assert_called_once()
    mock_input.assert_called_once_with("Enter the ID of the card you want to view: ")
    mock_readkey.assert_called_once()  # For "Press any key to continue"


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("readchar.readkey", side_effect=["4"])  # Exit menu
@patch("builtins.input", side_effect=["1"])  # Card ID
@patch("flash_zap.tui.browse_view.get_card_by_id")
@patch("builtins.print")
def test_show_card_view_displays_card_and_menu(
    mock_print, mock_get_card_by_id, mock_input, mock_readkey, mock_clear
):
    """Tests that card details and the edit menu are displayed correctly."""
    mock_session = Mock()
    test_card = Card(front="Test Front", back="Test Back", mastery_level=3)
    test_card.id = 1
    test_card.next_review_date = date(2025, 1, 1)
    mock_get_card_by_id.return_value = test_card

    browse_view.show_card_view(mock_session)

    assert mock_clear.call_count == 2  # Once at start, once after finding card
    # Assert that card details and menu were printed
    assert any("--- Card Details ---" in str(c) for c in mock_print.call_args_list)
    assert any("--- Edit Options ---" in str(c) for c in mock_print.call_args_list)


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("flash_zap.tui.browse_view.update_card_front")
@patch("readchar.readkey", side_effect=["1", "any_key", "4"])  # Edit front, continue, cancel
@patch("builtins.input", side_effect=["1", "New Front"])  # Card ID, new front text
@patch("flash_zap.tui.browse_view.get_card_by_id")
@patch("builtins.print")
def test_edit_front_option(
    mock_print, mock_get_card, mock_input, mock_readkey, mock_update, mock_clear
):
    """Tests the 'Edit front' option flow."""
    mock_session = Mock()
    test_card = Card(front="Old Front", back="Test Back")
    test_card.id = 1
    mock_get_card.return_value = test_card

    browse_view.show_card_view(mock_session)

    mock_input.assert_has_calls([call("Enter the ID of the card you want to view: "), call("Enter the new text for the front: ")])
    mock_update.assert_called_once_with(mock_session, 1, "New Front")
    mock_print.assert_any_call("Current front: Old Front")
    mock_print.assert_any_call("Card front updated successfully.")
    assert mock_clear.call_count > 2  # Start, after find, before prompt, then loops


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("flash_zap.tui.browse_view.update_card_back")
@patch("readchar.readkey", side_effect=["2", "any_key", "4"])  # Edit back, continue, cancel
@patch("builtins.input", side_effect=["1", "New Back"])  # Card ID, new back text
@patch("flash_zap.tui.browse_view.get_card_by_id")
@patch("builtins.print")
def test_edit_back_option(
    mock_print, mock_get_card, mock_input, mock_readkey, mock_update, mock_clear
):
    """Tests the 'Edit back' option flow."""
    mock_session = Mock()
    test_card = Card(front="Test Front", back="Old Back")
    test_card.id = 1
    mock_get_card.return_value = test_card

    browse_view.show_card_view(mock_session)

    mock_input.assert_has_calls([call("Enter the ID of the card you want to view: "), call("Enter the new text for the back: ")])
    mock_update.assert_called_once_with(mock_session, 1, "New Back")
    mock_print.assert_any_call("Current back: Old Back")
    mock_print.assert_any_call("Card back updated successfully.")


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("flash_zap.tui.browse_view.update_card_mastery")
@patch("readchar.readkey", side_effect=["3", "any_key", "4"])  # Lower mastery, continue, cancel
@patch("builtins.input", side_effect=["1", "2"])  # Card ID, new mastery level
@patch("flash_zap.tui.browse_view.get_card_by_id")
@patch("builtins.print")
def test_lower_mastery_option_valid(
    mock_print, mock_get_card, mock_input, mock_readkey, mock_update, mock_clear
):
    """Tests the 'Lower mastery level' option with a valid new level."""
    mock_session = Mock()
    test_card = Card(front="Test Front", back="Test Back", mastery_level=3)
    test_card.id = 1
    mock_get_card.return_value = test_card

    browse_view.show_card_view(mock_session)

    mock_update.assert_called_once_with(mock_session, 1, 2)
    mock_print.assert_any_call("Current mastery level: 3")
    mock_print.assert_any_call("Mastery level updated successfully.")


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("flash_zap.tui.browse_view.update_card_mastery")
@patch("readchar.readkey", side_effect=["3", "any_key", "4"])  # Lower mastery, continue, cancel
@patch("builtins.input", side_effect=["1", "4"])  # Card ID, new (higher) mastery level
@patch("flash_zap.tui.browse_view.get_card_by_id")
@patch("builtins.print")
def test_lower_mastery_option_invalid_higher(
    mock_print, mock_get_card, mock_input, mock_readkey, mock_update, mock_clear
):
    """Tests that mastery level cannot be raised."""
    mock_session = Mock()
    test_card = Card(front="Test Front", back="Test Back", mastery_level=3)
    test_card.id = 1
    mock_get_card.return_value = test_card

    browse_view.show_card_view(mock_session)
    mock_update.assert_not_called()
    mock_print.assert_any_call("Current mastery level: 3")
    mock_print.assert_any_call("New mastery level cannot be higher than the current one.")


@patch("flash_zap.tui.browse_view.clear_screen")
@patch("flash_zap.tui.browse_view.update_card_mastery")
@patch("readchar.readkey", side_effect=["3", "any_key", "4"])  # Lower mastery, continue, cancel
@patch("builtins.input", side_effect=["1", "abc"])  # Card ID, new (invalid) mastery level
@patch("flash_zap.tui.browse_view.get_card_by_id")
@patch("builtins.print")
def test_lower_mastery_option_invalid_nan(
    mock_print, mock_get_card, mock_input, mock_readkey, mock_update, mock_clear
):
    """Tests 'Lower mastery level' with non-numeric input."""
    mock_session = Mock()
    test_card = Card(front="Test Front", back="Test Back", mastery_level=3)
    test_card.id = 1
    mock_get_card.return_value = test_card

    browse_view.show_card_view(mock_session)
    mock_update.assert_not_called()
    mock_print.assert_any_call("Current mastery level: 3")
    mock_print.assert_any_call("Invalid input. Please enter a number.") 