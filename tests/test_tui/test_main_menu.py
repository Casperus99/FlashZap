from unittest.mock import patch
import pytest

from flash_zap.tui.main_menu import display_main_menu, handle_menu_input


def test_display_main_menu_structure_and_content():
    """
    Tests if the main menu display function returns the correct, fully formatted string.
    This test covers the requirements of sub-tasks 1.1, 1.2, 1.3, 1.4, and 1.5.
    """
    expected_output = (
        "--- FlashZap Main Menu ---\n"
        "1. Review Due Cards\n"
        "2. Import Flashcards from JSON\n"
        "3. Exit\n"
        "Select an option (1-3)"
    )

    actual_output = display_main_menu()

    assert actual_output == expected_output


@patch('flash_zap.tui.main_menu.navigate_to_review_session')
def test_handle_menu_input_navigates_to_review_on_1(mock_navigate_review):
    """
    Tests if handle_menu_input calls the correct placeholder function when '1' is pressed.
    This test covers sub-task 2.1.
    """
    action = handle_menu_input('1')
    mock_navigate_review.assert_called_once()
    assert action == "continue"


@patch('flash_zap.tui.main_menu.navigate_to_import_flow')
def test_handle_menu_input_navigates_to_import_on_2(mock_navigate_import):
    """
    Tests if handle_menu_input calls the correct placeholder function when '2' is pressed.
    This test covers sub-task 2.2.
    """
    action = handle_menu_input('2')
    mock_navigate_import.assert_called_once()
    assert action == "continue"


def test_handle_menu_input_returns_exit_on_3():
    """
    Tests if handle_menu_input returns 'exit' when '3' is pressed.
    This test covers sub-task 3.1.
    """
    action = handle_menu_input('3')
    assert action == "exit"


@pytest.mark.parametrize("invalid_input", ["5", "a", "ArrowUp", " "])
def test_handle_menu_input_ignores_invalid_input(invalid_input):
    """
    Tests if handle_menu_input returns a value indicating no action for invalid keys.
    This test covers sub-tasks 4.1, 4.2, and 4.3.
    """
    action = handle_menu_input(invalid_input)
    assert action is None 