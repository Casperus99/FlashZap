import pytest
from fastapi.testclient import TestClient

from src.flash_zap.web.app import app


@pytest.fixture(scope="function")
def client():
    """
    Test client for the web application.
    """
    with TestClient(app) as c:
        yield c 