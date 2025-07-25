
from fastapi.testclient import TestClient


def test_main_menu_renders_correctly(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the root ('/') endpoint.
    THEN: The response should be a 200 OK HTML response with the main menu content.
    """
    # WHEN
    response = client.get("/")

    # THEN
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    content = response.text
    assert "Browse Cards" in content
    assert "Start a review session" in content 
    assert "Import Flashcards from JSON" in content 