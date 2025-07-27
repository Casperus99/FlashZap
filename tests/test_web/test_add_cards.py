from fastapi.testclient import TestClient
from bs4 import BeautifulSoup
import tempfile
import json
from unittest.mock import patch, MagicMock


def test_add_cards_page_returns_200_ok(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the '/add-cards' endpoint.
    THEN: The response should be a 200 OK status.
    """
    # WHEN
    response = client.get("/add-cards")

    # THEN
    assert response.status_code == 200


def test_add_cards_page_has_correct_title(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the '/add-cards' endpoint.
    THEN: The response should contain the correct page title.
    """
    # WHEN
    response = client.get("/add-cards")

    # THEN
    soup = BeautifulSoup(response.text, 'html.parser')
    assert soup.find('h1').text.strip() == "Add new flashcards"


def test_add_cards_page_has_manual_entry_form(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the '/add-cards' endpoint.
    THEN: The page should contain a form for manual card entry with front and back inputs.
    """
    # WHEN
    response = client.get("/add-cards")

    # THEN
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form', {'id': 'manual-cards-form'})
    assert form is not None
    
    # Check for initial card input pair
    front_input = form.find('input', {'name': 'front_0'})
    back_input = form.find('textarea', {'name': 'back_0'}) or form.find('input', {'name': 'back_0'})
    assert front_input is not None
    assert back_input is not None


def test_add_cards_page_has_add_more_button(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the '/add-cards' endpoint.
    THEN: The page should contain a button to add more card pairs.
    """
    # WHEN
    response = client.get("/add-cards")

    # THEN
    soup = BeautifulSoup(response.text, 'html.parser')
    add_button = soup.find('button', {'id': 'add-more-cards'})
    assert add_button is not None
    assert "+" in add_button.text or "Add" in add_button.text


def test_add_cards_page_has_json_upload_section(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the '/add-cards' endpoint.
    THEN: The page should contain a section for JSON file upload.
    """
    # WHEN
    response = client.get("/add-cards")

    # THEN
    soup = BeautifulSoup(response.text, 'html.parser')
    file_input = soup.find('input', {'type': 'file'})
    assert file_input is not None
    assert file_input.get('accept') == '.json' or 'json' in file_input.get('accept', '')


@patch("flash_zap.models.card.Card")
@patch("flash_zap.web.routes.SessionLocal")
def test_submit_manual_cards_creates_cards_in_database(mock_session_local, mock_card_class, client: TestClient):
    """
    GIVEN: Valid card data is submitted via the manual form.
    WHEN: A POST request is made to the '/add-cards' endpoint.
    THEN: The cards should be created in the database and user redirected to success page.
    """
    # GIVEN
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session
    
    card_data = {
        "front_0": "Question 1",
        "back_0": "Answer 1",
        "front_1": "Question 2", 
        "back_1": "Answer 2"
    }

    # WHEN
    response = client.post("/add-cards", data=card_data, follow_redirects=False)

    # THEN
    assert response.status_code == 302  # Redirect after successful creation
    
    # Verify the right number of cards were created
    assert mock_card_class.call_count == 2
    
    # Verify card data
    card_calls = mock_card_class.call_args_list
    assert card_calls[0][1]["front"] == "Question 1"
    assert card_calls[0][1]["back"] == "Answer 1"
    assert card_calls[1][1]["front"] == "Question 2"
    assert card_calls[1][1]["back"] == "Answer 2"
    
    # Verify session operations
    assert mock_session.add.call_count == 2
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


def test_json_upload_shows_cards_as_editable_forms(client: TestClient):
    """
    GIVEN: A valid JSON file with flashcard data.
    WHEN: The file is uploaded via the JSON upload section.
    THEN: The cards should be displayed as editable forms before final submission.
    """
    # GIVEN
    cards_data = [
        {"front": "What is Python?", "back": "A programming language"},
        {"front": "What is FastAPI?", "back": "A web framework"}
    ]
    
    # Create temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(cards_data, f)
        temp_file_path = f.name

    # WHEN
    with open(temp_file_path, 'rb') as f:
        response = client.post("/add-cards", files={"json_file": ("test.json", f, "application/json")})

    # THEN
    assert response.status_code == 200
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Should show editable forms for each imported card
    form = soup.find('form', {'id': 'imported-cards-form'})
    assert form is not None
    
    # Check that imported cards are shown as editable inputs
    front_inputs = form.find_all('input', {'name': lambda x: x and x.startswith('front_')})
    back_inputs = form.find_all(['textarea', 'input'], {'name': lambda x: x and x.startswith('back_')})
    
    assert len(front_inputs) == 2
    assert len(back_inputs) == 2
    
    # Check that values are pre-filled from JSON
    assert front_inputs[0].get('value') == "What is Python?"
    assert front_inputs[1].get('value') == "What is FastAPI?"


def test_empty_manual_form_shows_validation_error(client: TestClient):
    """
    GIVEN: An empty manual card form is submitted.
    WHEN: A POST request is made to the '/add-cards' endpoint.
    THEN: The page should show validation errors and not create any cards.
    """
    # GIVEN - empty form data
    card_data = {"front_0": "", "back_0": ""}

    # WHEN
    response = client.post("/add-cards", data=card_data)

    # THEN
    assert response.status_code == 200  # Stay on same page
    soup = BeautifulSoup(response.text, 'html.parser')
    error_message = soup.find(class_='error') or soup.find(text=lambda text: 'error' in text.lower() if text else False)
    assert error_message is not None 