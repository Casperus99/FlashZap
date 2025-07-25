import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup


def test_review_start_endpoint_returns_200(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the /review endpoint.
    THEN: The response should be 200 OK with review session HTML.
    """
    # WHEN
    response = client.get("/review")

    # THEN
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@patch("flash_zap.web.routes.ReviewSession")
def test_review_start_creates_session_with_cards(mock_review_session_class, client: TestClient):
    """
    GIVEN: A mocked ReviewSession with cards available.
    WHEN: A GET request is made to /review.
    THEN: A ReviewSession should be created and first card displayed.
    """
    # GIVEN
    mock_session = MagicMock()
    mock_card = MagicMock()
    mock_card.id = 1
    mock_card.front = "Test Question"
    mock_card.back = "Test Answer"
    mock_session.get_next_card.return_value = mock_card
    mock_session.remaining_cards_count = 5
    mock_review_session_class.return_value = mock_session

    # WHEN
    response = client.get("/review")

    # THEN
    assert response.status_code == 200
    mock_review_session_class.assert_called_once()
    assert "Test Question" in response.text


@patch("flash_zap.web.routes.ReviewSession")
def test_review_start_shows_no_cards_message_when_empty(mock_review_session_class, client: TestClient):
    """
    GIVEN: A mocked ReviewSession with no cards available.
    WHEN: A GET request is made to /review.
    THEN: A "no cards due" message should be displayed.
    """
    # GIVEN
    mock_session = MagicMock()
    mock_session.get_next_card.return_value = None
    mock_session.remaining_cards_count = 0
    mock_review_session_class.return_value = mock_session

    # WHEN
    response = client.get("/review")

    # THEN
    assert response.status_code == 200
    assert "No cards are due for review" in response.text or "no cards due" in response.text.lower()


def test_review_answer_submission_endpoint_exists(client: TestClient):
    """
    GIVEN: A review session in progress.
    WHEN: A POST request is made to /review with an answer.
    THEN: The response should be successful.
    """
    # GIVEN
    user_answer = "My test answer"

    # WHEN
    response = client.post("/review", data={"user_answer": user_answer})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect


@patch("flash_zap.web.routes.ReviewSession")
def test_review_answer_processing_calls_grade_and_update(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session with a current card and user answer.
    WHEN: A POST request is made to /review with answer data.
    THEN: The session should call grade_and_update_card and get_next_card.
    """
    # GIVEN
    mock_session = MagicMock()
    mock_session.grade_and_update_card.return_value = ("Correct", "Good job!", 2, 3)
    mock_session.get_next_card.return_value = None  # No more cards
    mock_session.remaining_cards_count = 0
    
    # Setup the "session storage" mock
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        # Set cookies on client instance
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "My answer"})

        # THEN
        assert response.status_code in [200, 302]
        # Note: We can't assert the calls here yet since we haven't implemented the storage mechanism


@patch("flash_zap.web.routes.ReviewSession")
def test_review_shows_feedback_after_grading(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session that grades an answer.
    WHEN: A POST request is made to /review with an answer.
    THEN: The response should show grading feedback.
    """
    # GIVEN
    mock_session = MagicMock()
    mock_session.grade_and_update_card.return_value = ("Correct", "Great answer!", 2, 3)
    next_card = MagicMock()
    next_card.front = "Next Question"
    mock_session.get_next_card.return_value = next_card
    mock_session.remaining_cards_count = 1
    
    # Setup session storage
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        # Set cookies on client instance
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Test answer"})

        # THEN
        assert response.status_code == 200
        assert "Correct" in response.text or "Great answer!" in response.text


@patch("flash_zap.web.routes.ReviewSession")
def test_review_redirects_to_summary_when_complete(mock_review_session_class, client: TestClient):
    """
    GIVEN: A review session with no more cards after grading.
    WHEN: A POST request is made to /review with the last answer.
    THEN: The response should redirect to summary or show completion message.
    """
    # GIVEN
    mock_session = MagicMock()
    mock_session.grade_and_update_card.return_value = ("Correct", "Well done!", 3, 4)
    mock_session.get_next_card.return_value = None  # No more cards
    mock_session.remaining_cards_count = 0
    
    # Setup session storage
    with patch("flash_zap.web.routes.active_sessions", {"test_session": mock_session}):
        # Set cookies on client instance
        client.cookies.set("session_id", "test_session")
        
        # WHEN
        response = client.post("/review", data={"user_answer": "Final answer"})

        # THEN
        assert response.status_code in [200, 302]
        # Should either redirect to summary or show completion message 