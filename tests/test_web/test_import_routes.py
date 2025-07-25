import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import io


def test_import_form_endpoint_returns_200(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the /import endpoint.
    THEN: The response should be 200 OK with import form HTML.
    """
    # WHEN
    response = client.get("/import")

    # THEN
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_import_form_contains_file_upload(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to /import.
    THEN: The HTML should contain a file upload form.
    """
    # WHEN
    response = client.get("/import")
    soup = BeautifulSoup(response.text, 'html.parser')

    # THEN
    assert response.status_code == 200
    form = soup.find('form')
    assert form is not None
    file_input = soup.find('input', {'type': 'file'})
    assert file_input is not None


@patch("flash_zap.web.routes.import_cards_from_json")
def test_import_post_endpoint_exists(mock_import_function, client: TestClient):
    """
    GIVEN: A JSON file for import.
    WHEN: A POST request is made to /import with file upload.
    THEN: The response should be successful.
    """
    # GIVEN
    test_file_content = '[{"front": "Q1", "back": "A1"}]'
    test_file = io.BytesIO(test_file_content.encode())
    
    # WHEN
    response = client.post("/import", files={"file": ("test.json", test_file, "application/json")})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect


@patch("flash_zap.web.routes.import_cards_from_json")
def test_import_calls_import_service(mock_import_function, client: TestClient):
    """
    GIVEN: A valid JSON file and mocked import service.
    WHEN: A POST request is made to /import with the file.
    THEN: The import_cards_from_json function should be called.
    """
    # GIVEN
    test_file_content = '[{"front": "Question", "back": "Answer"}]'
    test_file = io.BytesIO(test_file_content.encode())
    mock_import_function.return_value = None  # Successful import

    # WHEN
    response = client.post("/import", files={"file": ("cards.json", test_file, "application/json")})

    # THEN
    assert response.status_code in [200, 302]
    mock_import_function.assert_called_once()


@patch("flash_zap.web.routes.import_cards_from_json")
def test_import_shows_success_message(mock_import_function, client: TestClient):
    """
    GIVEN: A successful import operation.
    WHEN: A POST request is made to /import.
    THEN: A success message should be displayed.
    """
    # GIVEN
    test_file_content = '[{"front": "Test Q", "back": "Test A"}]'
    test_file = io.BytesIO(test_file_content.encode())
    mock_import_function.return_value = None

    # WHEN
    response = client.post("/import", files={"file": ("test.json", test_file, "application/json")})

    # THEN
    assert response.status_code == 200
    assert "success" in response.text.lower() or "imported" in response.text.lower()


@patch("flash_zap.web.routes.import_cards_from_json")
def test_import_handles_errors(mock_import_function, client: TestClient):
    """
    GIVEN: An import operation that raises an exception.
    WHEN: A POST request is made to /import.
    THEN: An error message should be displayed.
    """
    # GIVEN
    test_file_content = '[{"invalid": "json"}]'
    test_file = io.BytesIO(test_file_content.encode())
    mock_import_function.side_effect = Exception("Import failed")

    # WHEN
    response = client.post("/import", files={"file": ("bad.json", test_file, "application/json")})

    # THEN
    assert response.status_code == 200
    assert "error" in response.text.lower() or "failed" in response.text.lower() 