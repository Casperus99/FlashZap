from unittest.mock import Mock
import pytest

from flash_zap.core.card_manager import get_card_by_id
from flash_zap.models.card import Card

def test_get_card_by_id_returns_card_when_found():
    """
    Tests that get_card_by_id returns the correct card object when found.
    """
    mock_session = Mock()
    expected_card = Card(front="Front", back="Back")
    expected_card.id = 1
    
    # Mock the query chain
    mock_session.query.return_value.filter_by.return_value.first.return_value = expected_card
    
    card = get_card_by_id(mock_session, 1)
    
    mock_session.query.assert_called_once_with(Card)
    mock_session.query.return_value.filter_by.assert_called_once_with(id=1)
    assert card == expected_card

def test_get_card_by_id_returns_none_when_not_found():
    """
    Tests that get_card_by_id returns None when a card is not found.
    """
    mock_session = Mock()
    
    # Mock the query chain to return None
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    card = get_card_by_id(mock_session, 999)
    
    mock_session.query.assert_called_once_with(Card)
    mock_session.query.return_value.filter_by.assert_called_once_with(id=999)
    assert card is None 