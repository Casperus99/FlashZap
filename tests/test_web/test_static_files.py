import pytest
from fastapi.testclient import TestClient


def test_css_file_is_served(client: TestClient):
    """
    GIVEN: The FastAPI application with static file mounting.
    WHEN: A GET request is made to /static/style.css.
    THEN: The CSS file should be served with correct content type.
    """
    # WHEN
    response = client.get("/static/style.css")

    # THEN
    assert response.status_code == 200
    assert "text/css" in response.headers.get("content-type", "")


def test_main_menu_includes_css(client: TestClient):
    """
    GIVEN: The main menu template.
    WHEN: A GET request is made to the root endpoint.
    THEN: The HTML should include a link to the CSS file.
    """
    # WHEN
    response = client.get("/")

    # THEN
    assert response.status_code == 200
    assert 'href="/static/style.css"' in response.text
    assert 'rel="stylesheet"' in response.text 