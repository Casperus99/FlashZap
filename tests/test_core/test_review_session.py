import pytest
from sqlalchemy.orm import Session
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from flash_zap.models.card import Card
from flash_zap.core.review_session import ReviewSession


def test_get_next_card_returns_unseen_card(test_db_session: Session):
    """
    GIVEN: A database with multiple cards.
    WHEN: Retrieving cards sequentially from a review session.
    THEN: Each call to get_next_card returns the next unseen card.
    """
    # GIVEN: Seed the database with cards and create a review session
    card1 = Card(front="Question 1", back="Answer 1")
    card2 = Card(front="Question 2", back="Answer 2")
    test_db_session.add_all([card1, card2])
    test_db_session.commit()
    session = ReviewSession(test_db_session, shuffle=False)

    # WHEN: The first card is retrieved
    next_card_1 = session.get_next_card()

    # THEN: It is the first card from the database
    assert next_card_1 is not None
    assert next_card_1.id == card1.id
    assert next_card_1.front == "Question 1"

    # WHEN: The first card is processed and marked as seen
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(next_card_1, "Answer 1")
    
    # WHEN: The next card is retrieved
    next_card_2 = session.get_next_card()
    
    # THEN: It is the second card from the database
    assert next_card_2 is not None
    assert next_card_2.id == card2.id
    assert next_card_2.front == "Question 2"


def test_get_next_card_returns_none_when_all_cards_are_seen(test_db_session: Session):
    """
    GIVEN: A review session where all cards have been seen.
    WHEN: get_next_card is called.
    THEN: It returns None.
    """
    # GIVEN: A database with one card, and a review session
    card1 = Card(front="Question 1", back="Answer 1")
    test_db_session.add(card1)
    test_db_session.commit()
    session = ReviewSession(test_db_session, shuffle=False)
    
    # WHEN: The only card is retrieved and processed
    first_call = session.get_next_card()
    assert first_call is not None # Sanity check
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(first_call, "Answer 1")

    # THEN: The next call to get_next_card returns None
    second_call = session.get_next_card()
    assert second_call is None


def test_get_next_card_returns_only_due_cards(test_db_session: Session):
    """
    GIVEN: A database with cards that are due, not due, and legacy (no date).
    WHEN: get_next_card is called.
    THEN: Only the due and legacy cards are returned in order.
    """
    # GIVEN: Cards with different due dates
    now = datetime.now(timezone.utc)
    card_due = Card(front="Due", back="A", next_review_date=now - timedelta(days=1))
    card_not_due = Card(front="Not Due", back="B", next_review_date=now + timedelta(days=1))
    card_legacy = Card(front="Legacy", back="C", next_review_date=None)
    test_db_session.add_all([card_due, card_not_due, card_legacy])
    test_db_session.commit()
    session = ReviewSession(test_db_session, shuffle=False)

    # WHEN: The first card is retrieved and processed
    next_card_1 = session.get_next_card()

    # THEN: It is the due card
    assert next_card_1 is not None
    assert next_card_1.front == "Due"
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(next_card_1, "A")

    # WHEN: The second card is retrieved and processed
    next_card_2 = session.get_next_card()
    
    # THEN: It is the legacy card
    assert next_card_2 is not None
    assert next_card_2.front == "Legacy"
    with patch("flash_zap.core.review_session.ReviewSession.process_answer", return_value=("Correct", "")):
        session.grade_and_update_card(next_card_2, "C")

    # WHEN: The third card is retrieved
    next_card_3 = session.get_next_card()

    # THEN: No card is returned, as the remaining one is not due
    assert next_card_3 is None


@patch("flash_zap.core.review_session.ai_grader.grade_answer")
def test_review_session_calls_ai_grader_service(mock_grade_answer, test_db_session: Session):
    """
    GIVEN: A review session.
    WHEN: The process_answer method is called.
    THEN: The ai_grader service is called with the correct parameters.
    """
    # GIVEN: A mock AI grader, a card, and a review session
    mock_grade_answer.return_value = ("Correct", "Good job!")
    card = Card(front="Question", back="Answer")
    user_answer = "Answer"
    session = ReviewSession(test_db_session)

    # WHEN: The answer is processed
    result, feedback = session.process_answer(card, user_answer)

    # THEN: The AI grader is called correctly and returns the mocked response
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
    GIVEN: A card in the database.
    WHEN: The card is answered correctly and grade_and_update_card is called.
    THEN: The card's mastery level is increased and the change is persisted to the database.
    """
    # GIVEN: A card with an initial mastery level in the database
    # and a mock AI grader that returns "Correct"
    mock_grade_answer.return_value = ("Correct", "Feedback")
    card = Card(front="Q", back="A", mastery_level=1)
    test_db_session.add(card)
    test_db_session.commit()
    initial_level = card.mastery_level
    session = ReviewSession(test_db_session)
    user_answer = "A"

    # WHEN: The card is graded and updated
    session.grade_and_update_card(card, user_answer)

    # THEN: The AI grader was called and the card's mastery level is updated in the DB
    mock_grade_answer.assert_called_once()
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
    """
    GIVEN: A review session with a mock SRS Engine.
    WHEN: A card is graded.
    THEN: The correct method on the SRS Engine is called based on the grade.
    """
    # GIVEN: A mock AI grader returning a specific grade, and a mock SRS engine
    mock_grade_answer.return_value = (grade, "Feedback")
    mock_srs_engine_instance = mock_srs_engine_cls.return_value
    session = ReviewSession(test_db_session)
    card = Card(front="Q", back="A")
    user_answer = "A"
    # The card must be in the review deck to be processed
    session._review_deck = [card]

    # WHEN: The card is graded and updated
    session.grade_and_update_card(card, user_answer)

    # THEN: The appropriate SRS Engine method is called
    method_to_check = getattr(mock_srs_engine_instance, expected_call)
    method_to_check.assert_called_once_with(card)

    unexpected_call = "demote_card" if expected_call == "promote_card" else "promote_card"
    unexpected_method = getattr(mock_srs_engine_instance, unexpected_call)
    unexpected_method.assert_not_called() 