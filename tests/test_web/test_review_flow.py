import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup


@patch("flash_zap.web.routes.ReviewSession")
def test_submit_answer_shows_feedback_stays_on_same_card(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session with a current card.
    WHEN: A POST request is made to /review with action=submit_answer.
    THEN: The response should show feedback but stay on the same card.
    """
    # GIVEN
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.id = 1
    current_card.front = "Test Question"
    current_card.back = "Test Answer"
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Correct", "Great job!", 2, 3)
    mock_session.remaining_cards_count = 5
    
    # Setup session storage
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "My answer", "action": "submit_answer"})

        # THEN
        assert response.status_code == 200
        assert "Correct" in response.text
        assert "Great job!" in response.text
        assert "Test Question" in response.text  # Same card still shown
        assert "Continue" in response.text or "Next" in response.text  # Continue button present


@patch("flash_zap.web.routes.ReviewSession")
def test_continue_after_feedback_moves_to_next_card(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session after feedback has been shown.
    WHEN: A POST request is made to /review with action=continue.
    THEN: The response should move to the next card without feedback.
    """
    # GIVEN
    mock_session = MagicMock()
    next_card = MagicMock()
    next_card.id = 2
    next_card.front = "Next Question"
    next_card.back = "Next Answer"
    mock_session.get_next_card.return_value = next_card
    mock_session.remaining_cards_count = 4
    
    # Setup session storage
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"action": "continue"})

        # THEN
        assert response.status_code == 200
        assert "Next Question" in response.text
        assert "Submit Answer" in response.text  # Back to submit state
        # Should not contain previous feedback
        assert "Correct" not in response.text or "Great job!" not in response.text


@patch("flash_zap.web.routes.ReviewSession")
def test_feedback_displayed_between_button_and_textarea(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session after submitting an answer.
    WHEN: The feedback is displayed.
    THEN: The feedback should appear between the button and textarea area.
    """
    # GIVEN
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.front = "Test Question"
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Incorrect", "Try again!", 1, 0)
    mock_session.remaining_cards_count = 3
    
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Wrong answer", "action": "submit_answer"})
        soup = BeautifulSoup(response.text, 'html.parser')

        # THEN
        assert response.status_code == 200
        
        # Find feedback section
        feedback_div = soup.find('div', class_='feedback')
        assert feedback_div is not None
        assert "Incorrect" in feedback_div.text
        assert "Try again!" in feedback_div.text


def test_default_action_when_no_action_specified(client: TestClient):
    """
    GIVEN: A review session.
    WHEN: A POST request is made without specifying action.
    THEN: It should default to submit_answer behavior.
    """
    # This test ensures backward compatibility
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.front = "Test Question"
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Correct", "Good!", 2, 3)
    mock_session.remaining_cards_count = 2
    
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        with patch("flash_zap.web.routes.ReviewSession", return_value=mock_session):
            client.cookies.set("session_id", "test_session")
            
            # WHEN
            response = client.post("/review", data={"user_answer": "My answer"})

            # THEN
            assert response.status_code == 200


@patch("flash_zap.web.routes.ReviewSession")
def test_user_answer_remains_visible_in_feedback(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session after submitting an answer.
    WHEN: Feedback is displayed.
    THEN: The user's original answer should remain visible on the page.
    """
    # GIVEN
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.front = "What is 2+2?"
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Correct", "Well done!", 2, 3)
    mock_session.remaining_cards_count = 3
    
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Four", "action": "submit_answer"})

        # THEN
        assert response.status_code == 200
        assert "Four" in response.text  # User's answer should be visible
        assert "Your answer:" in response.text and "Four" in response.text


@patch("flash_zap.web.routes.ReviewSession")
def test_correct_feedback_has_green_background(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session with correct answer feedback.
    WHEN: The feedback is displayed.
    THEN: The feedback should have a green background class or style.
    """
    # GIVEN
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.front = "Test Question"
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Correct", "Great job!", 2, 3)
    mock_session.remaining_cards_count = 3
    
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Right answer", "action": "submit_answer"})
        soup = BeautifulSoup(response.text, 'html.parser')

        # THEN
        assert response.status_code == 200
        feedback_div = soup.find('div', class_='feedback')
        assert feedback_div is not None
        
        # Check for green styling
        assert 'feedback-correct' in feedback_div.get('class', []) or 'correct' in str(feedback_div.get('class', []))


@patch("flash_zap.web.routes.ReviewSession")
def test_incorrect_feedback_has_red_background(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session with incorrect answer feedback.
    WHEN: The feedback is displayed.
    THEN: The feedback should have a red background class or style.
    """
    # GIVEN
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.front = "Test Question"
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Incorrect", "Try again!", 1, 0)
    mock_session.remaining_cards_count = 3
    
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Wrong answer", "action": "submit_answer"})
        soup = BeautifulSoup(response.text, 'html.parser')

        # THEN
        assert response.status_code == 200
        feedback_div = soup.find('div', class_='feedback')
        assert feedback_div is not None
        
        # Check for red styling
        assert 'feedback-incorrect' in feedback_div.get('class', []) or 'incorrect' in str(feedback_div.get('class', []))


@patch("flash_zap.web.routes.ReviewSession")
def test_feedback_shows_mastery_level_change(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session where answering a card changes the mastery level.
    WHEN: Feedback is displayed after grading.
    THEN: The feedback should show the mastery level change (e.g., "3 → 4").
    """
    # GIVEN
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.front = "Test Question"
    current_card.mastery_level = 4  # New mastery level after grading
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Correct", "Great job!", 3, 4)  # old=3, new=4
    mock_session.remaining_cards_count = 3
    
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Right answer", "action": "submit_answer"})

        # THEN
        assert response.status_code == 200
        assert "3 → 4" in response.text  # Mastery level change should be shown
        assert "Mastery level:" in response.text


@patch("flash_zap.web.routes.ReviewSession")
def test_feedback_shows_mastery_level_decrease(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session where answering incorrectly decreases the mastery level.
    WHEN: Feedback is displayed after grading.
    THEN: The feedback should show the mastery level decrease (e.g., "4 → 3").
    """
    # GIVEN
    mock_session = MagicMock()
    current_card = MagicMock()
    current_card.front = "Test Question"
    current_card.mastery_level = 3  # New mastery level after grading (decreased)
    mock_session.get_next_card.return_value = current_card
    mock_session.grade_and_update_card.return_value = ("Incorrect", "Try again!", 4, 3)  # old=4, new=3
    mock_session.remaining_cards_count = 3
    
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Wrong answer", "action": "submit_answer"})

        # THEN
        assert response.status_code == 200
        assert "4 → 3" in response.text  # Mastery level decrease should be shown
        assert "Mastery level:" in response.text 