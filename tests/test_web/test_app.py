
from fastapi.testclient import TestClient
import pytest


def test_root_returns_200_and_welcome_message(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the root ('/') endpoint.
    THEN: The response should have a 200 OK status code and contain the welcome message.
    """
    # WHEN
    response = client.get("/")

    # THEN
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FlashZap Web UI!"} 