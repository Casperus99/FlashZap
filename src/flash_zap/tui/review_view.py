from rich.console import Console
from rich.prompt import Prompt
from sqlalchemy.orm import Session

from flash_zap.core.exceptions import AIGraderError
from flash_zap.core.review_session import ReviewSession
from flash_zap.models.card import Card


def start_review_session(db_session: Session) -> None:
    """Starts a review session."""
    console = Console()
    session = ReviewSession(db_session)

    card = session.get_next_card()
    if not card:
        display_no_cards_due_message(console)
        return

    while card:
        display_card_front(card, console)
        user_answer = Prompt.ask("Your answer")

        if user_answer.lower() == "exit":
            break

        display_loading_indicator(console)
        try:
            grade, feedback = session.grade_and_update_card(card, user_answer)
            display_grade_and_feedback(grade, feedback, card, console)
        except AIGraderError:
            display_service_error_message(console)

        Prompt.ask("Press Enter to continue...")
        card = session.get_next_card()

    console.print("Review session ended.")


def display_card_front(card: Card, console: Console) -> None:
    """Displays the front of a card."""
    console.print(card.front)


def display_loading_indicator(console: Console) -> None:
    """Displays a loading indicator."""
    console.print("[yellow]Grading...[/yellow]", justify="center")


def display_grade_and_feedback(
    grade: str, feedback: str, card: Card, console: Console
) -> None:
    """Displays the grade and feedback."""
    grade_color = "green" if grade == "Correct" else "red"
    console.print(f"────── [bold {grade_color}]{grade}[/bold {grade_color}] ──────", justify="center")
    console.print(f"[bold]Feedback:[/bold] {feedback}")
    console.print(f"[dim]Mastery level updated to: {card.mastery_level}[/dim]")


def display_no_cards_due_message(console: Console) -> None:
    """Displays a message when no cards are due for review."""
    console.print("Great job! No cards are due for review.")


def display_service_error_message(console: Console) -> None:
    """Displays a message when the AI service is unavailable."""
    console.print("Sorry, the AI grading service is currently unavailable.") 