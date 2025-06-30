import pytest
from sqlalchemy.orm import Session
from unittest.mock import patch

from flash_zap.models.card import Card
from flash_zap.core.review_session import ReviewSession


def test_get_next_card_returns_unseen_card(test_db_session: Session):
    """
    Tests that get_next_card returns unseen cards sequentially from the database.
    """
    # Arrange: Seed the database with cards
    card1 = Card(front="Question 1", back="Answer 1")
    card2 = Card(front="Question 2", back="Answer 2")
    test_db_session.add_all([card1, card2])
    test_db_session.commit()

    # Act
    session = ReviewSession(test_db_session)

    # Assert: First call returns the first card
    next_card_1 = session.get_next_card()
    assert next_card_1 is not None
    assert next_card_1.id == card1.id
    assert next_card_1.front == "Question 1"

    # Assert: Second call returns the second card
    next_card_2 = session.get_next_card()
    assert next_card_2 is not None
    assert next_card_2.id == card2.id
    assert next_card_2.front == "Question 2"


def test_get_next_card_returns_none_when_all_cards_are_seen(test_db_session: Session):
    """
    Tests that get_next_card returns None after all cards have been seen.
    """
    # Arrange: Seed the database with one card
    card1 = Card(front="Question 1", back="Answer 1")
    test_db_session.add(card1)
    test_db_session.commit()

    # Act
    session = ReviewSession(test_db_session)

    # Assert: First call returns the card
    first_call = session.get_next_card()
    assert first_call is not None
    assert first_call.id == card1.id

    # Assert: Second call returns None
    second_call = session.get_next_card()
    assert second_call is None


@patch("flash_zap.core.review_session.ai_grader.grade_answer")
def test_review_session_calls_ai_grader_service(mock_grade_answer, test_db_session: Session):
    """
    Tests that ReviewSession.process_answer calls the ai_grader service.
    """
    # Arrange
    mock_grade_answer.return_value = ("Correct", "Good job!")
    card = Card(front="Question", back="Answer")
    user_answer = "Answer"
    session = ReviewSession(test_db_session)

    # Act
    result, feedback = session.process_answer(card, user_answer)

    # Assert
    mock_grade_answer.assert_called_once_with(
        user_answer=user_answer,
        correct_answer=card.back,
    )
    assert result == "Correct"
    assert feedback == "Good job!" 