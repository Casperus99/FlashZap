import sys
import os
import pytest
from unittest.mock import MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flash_zap.models.base import Base
# Import all models here to ensure they are registered with Base
from flash_zap.models.card import Card

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture(scope="function")
def test_db_session():
    """
    Pytest fixture for an isolated in-memory SQLite database session.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def mock_ai_client():
    """
    Pytest fixture for a mocked AI grading service client.

    This avoids making real network calls during tests, making them
    faster and more reliable.
    """
    client = MagicMock()
    # Example of configuring the mock for a specific test:
    # client.grade_answer.return_value = {"grade": "good", "feedback": "Well done!"}
    return client
