import unittest.mock
from rich.console import Console

from flash_zap.models.card import Card
from flash_zap.tui import review_view


def test_review_view_displays_card_front():
    # Arrange
    console = Console()
    card = Card(front="Question: What is TDD?", back="Answer: Test-Driven Development")

    # Act
    with console.capture() as capture:
        review_view.display_card_front(card, console)

    output = capture.get()

    # Assert
    assert "Question: What is TDD?" in output


def test_review_view_shows_loading_indicator():
    # Arrange
    console = Console()

    # Act
    with console.capture() as capture:
        review_view.display_loading_indicator(console)

    output = capture.get()

    # Assert
    assert "Grading..." in output


def test_review_view_displays_grade_and_feedback():
    # Arrange
    console = Console()
    grade = "Correct"
    feedback = "Good job!"
    card = Card(
        front="What is love?",
        back="Baby don't hurt me",
        mastery_level=1,
    )

    # Act
    with console.capture() as capture:
        review_view.display_grade_and_feedback(grade, feedback, card, console)

    output = capture.get()

    # Assert
    assert "Correct" in output
    assert "Feedback: Good job!" in output
    assert "Mastery level updated to: 1" in output


def test_review_view_displays_no_cards_due_message():
    # Arrange
    console = Console()

    # Act
    with console.capture() as capture, unittest.mock.patch("rich.prompt.Prompt.ask"):
        review_view.display_no_cards_due_message(console)

    output = capture.get()

    # Assert
    assert "Great job! No cards are due for review." in output


def test_review_view_displays_service_error_message():
    # Arrange
    console = Console()

    # Act
    with console.capture() as capture:
        review_view.display_service_error_message(console)

    output = capture.get()

    # Assert
    assert "Sorry, the AI grading service is currently unavailable." in output 