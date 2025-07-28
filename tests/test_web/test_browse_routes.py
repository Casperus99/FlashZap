import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup


def test_browse_form_endpoint_returns_200(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the /browse endpoint.
    THEN: The response should be 200 OK with browse form HTML.
    """
    # WHEN
    response = client.get("/browse")

    # THEN
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_browse_form_contains_card_id_input(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to /browse.
    THEN: The HTML should contain a form with card ID input field.
    """
    # WHEN
    response = client.get("/browse")
    soup = BeautifulSoup(response.text, 'html.parser')

    # THEN
    assert response.status_code == 200
    form = soup.find('form')
    assert form is not None
    card_id_input = soup.find('input', {'name': 'card_id'})
    assert card_id_input is not None


@patch("flash_zap.web.routes.card_manager")
def test_browse_card_endpoint_calls_card_manager(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and mocked card_manager.
    WHEN: A GET request is made to /browse/{card_id}.
    THEN: card_manager.get_card_by_id should be called with correct parameters.
    """
    # GIVEN
    card_id = 1
    mock_card = MagicMock()
    mock_card.id = 1
    mock_card.front = "Test Question"
    mock_card.back = "Test Answer"
    mock_card.mastery_level = 2
    mock_card.next_review_date = "2024-01-01"
    mock_card_manager.get_card_by_id.return_value = mock_card

    # WHEN
    response = client.get(f"/browse/{card_id}")

    # THEN
    mock_card_manager.get_card_by_id.assert_called_once()
    call_args = mock_card_manager.get_card_by_id.call_args[0]
    assert call_args[1] == card_id  # Second arg should be card_id


@patch("flash_zap.web.routes.card_manager")
def test_browse_card_endpoint_displays_card_details(mock_card_manager, client: TestClient):
    """
    GIVEN: A valid card ID and existing card.
    WHEN: A GET request is made to /browse/{card_id}.
    THEN: The HTML should display card details and edit options.
    """
    # GIVEN
    card_id = 1
    mock_card = MagicMock()
    mock_card.id = 1
    mock_card.front = "Test Question"
    mock_card.back = "Test Answer"
    mock_card.mastery_level = 2
    mock_card.next_review_date = "2024-01-01"
    mock_card_manager.get_card_by_id.return_value = mock_card

    # WHEN
    response = client.get(f"/browse/{card_id}")
    soup = BeautifulSoup(response.text, 'html.parser')

    # THEN
    assert response.status_code == 200
    assert "Test Question" in response.text
    assert "Test Answer" in response.text
    assert "2" in response.text  # mastery level


@patch("flash_zap.web.routes.card_manager")
def test_edit_card_front_endpoint_exists(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and new front text.
    WHEN: A POST request is made to /browse/{card_id}/edit-front.
    THEN: The response should be successful and card_manager.update_card_front should be called.
    """
    # GIVEN
    card_id = 1
    new_front = "Updated Question"
    mock_card = MagicMock()
    mock_card_manager.update_card_front.return_value = mock_card

    # WHEN
    response = client.post(f"/browse/{card_id}/edit-front", data={"new_front": new_front})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect
    mock_card_manager.update_card_front.assert_called_once()


@patch("flash_zap.web.routes.card_manager")
def test_edit_card_back_endpoint_exists(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and new back text.
    WHEN: A POST request is made to /browse/{card_id}/edit-back.
    THEN: The response should be successful and card_manager.update_card_back should be called.
    """
    # GIVEN
    card_id = 1
    new_back = "Updated Answer"
    mock_card = MagicMock()
    mock_card_manager.update_card_back.return_value = mock_card

    # WHEN
    response = client.post(f"/browse/{card_id}/edit-back", data={"new_back": new_back})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect
    mock_card_manager.update_card_back.assert_called_once()


@patch("flash_zap.web.routes.card_manager")
def test_edit_card_mastery_endpoint_exists(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and new mastery level.
    WHEN: A POST request is made to /browse/{card_id}/edit-mastery.
    THEN: The response should be successful and card_manager.update_card_mastery should be called.
    """
    # GIVEN
    card_id = 1
    new_mastery = 1
    mock_card_manager.update_card_mastery.return_value = (MagicMock(), True)

    # WHEN
    response = client.post(f"/browse/{card_id}/edit-mastery", data={"new_mastery_level": new_mastery})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect
    mock_card_manager.update_card_mastery.assert_called_once()


@patch("flash_zap.web.routes.card_manager")
def test_browse_card_template_contains_remove_option(mock_card_manager, client: TestClient):
    """
    GIVEN: A valid card ID and existing card.
    WHEN: A GET request is made to /browse/{card_id}.
    THEN: The HTML should contain a red-colored remove card option.
    """
    # GIVEN
    card_id = 1
    mock_card = MagicMock()
    mock_card.id = 1
    mock_card.front = "Test Question"
    mock_card.back = "Test Answer"
    mock_card.mastery_level = 2
    mock_card.next_review_date = "2024-01-01"
    mock_card_manager.get_card_by_id.return_value = mock_card

    # WHEN
    response = client.get(f"/browse/{card_id}")
    soup = BeautifulSoup(response.text, 'html.parser')

    # THEN
    assert response.status_code == 200
    # Look for the remove card option link
    remove_link = soup.find('a', string=lambda text: text and 'Remove card' in text)
    assert remove_link is not None
    # Check if the link has red styling (either inline or class)
    assert 'color: red' in str(remove_link) or 'red' in remove_link.get('class', [])


@patch("flash_zap.web.routes.card_manager")
def test_remove_card_endpoint_deletes_card(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and confirmation.
    WHEN: A POST request is made to /browse/{card_id}/remove with confirmation.
    THEN: The card_manager.delete_card should be called and redirect to browse.
    """
    # GIVEN
    card_id = 1
    mock_card_manager.delete_card.return_value = True

    # WHEN
    response = client.post(f"/browse/{card_id}/remove", data={"confirm": "yes"}, follow_redirects=False)

    # THEN
    assert response.status_code == 302  # Redirect after deletion
    mock_card_manager.delete_card.assert_called_once()
    call_args = mock_card_manager.delete_card.call_args[0]
    assert call_args[1] == card_id  # Second arg should be card_id


@patch("flash_zap.web.routes.card_manager")
def test_remove_card_endpoint_without_confirmation_redirects_back(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID without confirmation.
    WHEN: A POST request is made to /browse/{card_id}/remove without confirmation.
    THEN: The card should not be deleted and user redirected back to card.
    """
    # GIVEN
    card_id = 1

    # WHEN
    response = client.post(f"/browse/{card_id}/remove", data={}, follow_redirects=False)

    # THEN
    assert response.status_code == 302  # Redirect back
    mock_card_manager.delete_card.assert_not_called() 