import pytest
from sqlalchemy.orm import Session
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

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
    session = ReviewSession(test_db_session, shuffle=False)

    # Assert: First call returns the first card
    next_card_1 = session.get_next_card()
    assert next_card_1 is not None
    assert next_card_1.id == card1.id
    assert next_card_1.front == "Question 1"
    # To simulate the card being "seen", we need to process it.
    # We can mock the grading to simplify this.
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(next_card_1, "Answer 1")

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
    session = ReviewSession(test_db_session, shuffle=False)

    # Assert: First call returns the card
    first_call = session.get_next_card()
    assert first_call is not None
    assert first_call.id == card1.id
    # Simulate seeing the card
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(first_call, "Answer 1")

    # Assert: Second call returns None
    second_call = session.get_next_card()
    assert second_call is None


def test_get_next_card_returns_only_due_cards(test_db_session: Session):
    """
    Tests that get_next_card only returns cards that are due for review.
    """
    # Arrange: Seed the database with cards in various states
    now = datetime.now(timezone.utc)
    card_due = Card(front="Due", back="A", next_review_date=now - timedelta(days=1))
    card_not_due = Card(front="Not Due", back="B", next_review_date=now + timedelta(days=1))
    card_legacy = Card(front="Legacy", back="C", next_review_date=None) # Old card, no review date
    
    test_db_session.add_all([card_due, card_not_due, card_legacy])
    test_db_session.commit()

    # Act
    session = ReviewSession(test_db_session, shuffle=False)

    # Assert: First call should return the due card
    next_card_1 = session.get_next_card()
    assert next_card_1 is not None
    assert next_card_1.front == "Due"
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(next_card_1, "A")

    # Assert: Second call should return the legacy card
    next_card_2 = session.get_next_card()
    assert next_card_2 is not None
    assert next_card_2.front == "Legacy"
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(next_card_2, "C")
    
    # Assert: Third call should return None, as the 'Not Due' card shouldn't be selected
    next_card_3 = session.get_next_card()
    assert next_card_3 is None


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
        question=card.front,
        user_answer=user_answer,
        correct_answer=card.back,
    )
    assert result == "Correct"
    assert feedback == "Good job!"


@patch("flash_zap.core.review_session.ai_grader.grade_answer")
def test_grade_and_update_card_persists_changes(mock_grade_answer, test_db_session: Session):
    """
    Tests that grade_and_update_card correctly calls the SRS engine
    and persists the changes to the database.
    """
    # Arrange
    # We want a real SRSEngine, so we don't mock it.
    # We only mock the AI grader to control the outcome.
    mock_grade_answer.return_value = ("Correct", "Feedback")
    
    # Create a card and save it to the DB
    card = Card(front="Q", back="A", mastery_level=1)
    test_db_session.add(card)
    test_db_session.commit()
    
    initial_level = card.mastery_level
    
    session = ReviewSession(test_db_session)
    user_answer = "A"

    # Act
    session.grade_and_update_card(card, user_answer)

    # Assert
    # Verify the AI grader was called
    mock_grade_answer.assert_called_once()

    # Verify the change was persisted in the database
    test_db_session.refresh(card)
    assert card.mastery_level == initial_level + 1


@patch("flash_zap.core.review_session.SRSEngine")
@patch("flash_zap.core.review_session.ai_grader.grade_answer")
@pytest.mark.parametrize("grade, expected_call", [
    ("Correct", "promote_card"),
    ("Incorrect", "demote_card"),
])
def test_grade_and_update_card_calls_srs_engine(
    mock_grade_answer, mock_srs_engine_cls, grade, expected_call, test_db_session: Session
):
    # Arrange
    mock_grade_answer.return_value = (grade, "Feedback")
    mock_srs_engine_instance = mock_srs_engine_cls.return_value
    
    session = ReviewSession(test_db_session)
    card = Card(front="Q", back="A")
    user_answer = "A"
    session._review_deck = [card] # Manually set the deck

    # Act
    session.grade_and_update_card(card, user_answer)

    # Assert
    # Verify that the correct method on the SRSEngine instance was called
    method_to_check = getattr(mock_srs_engine_instance, expected_call)
    method_to_check.assert_called_once_with(card)

    # Verify the other method was not called
    unexpected_call = "demote_card" if expected_call == "promote_card" else "promote_card"
    unexpected_method = getattr(mock_srs_engine_instance, unexpected_call)
    unexpected_method.assert_not_called() 