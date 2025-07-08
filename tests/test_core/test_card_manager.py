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

def test_update_card_front(test_db_session):
    """
    Tests that update_card_front correctly changes the front of a card.
    """
    # Arrange
    from flash_zap.core.card_manager import update_card_front
    original_front = "Original Front"
    new_front = "New Front"
    card = Card(front=original_front, back="Back")
    test_db_session.add(card)
    test_db_session.commit()

    # Act
    updated_card = update_card_front(test_db_session, card.id, new_front)
    test_db_session.refresh(card)

    # Assert
    assert updated_card is not None
    assert updated_card.id == card.id
    assert updated_card.front == new_front
    assert card.front == new_front

def test_update_card_back(test_db_session):
    """
    Tests that update_card_back correctly changes the back of a card.
    """
    # Arrange
    from flash_zap.core.card_manager import update_card_back
    original_back = "Original Back"
    new_back = "New Back"
    card = Card(front="Front", back=original_back)
    test_db_session.add(card)
    test_db_session.commit()

    # Act
    updated_card = update_card_back(test_db_session, card.id, new_back)
    test_db_session.refresh(card)

    # Assert
    assert updated_card is not None
    assert updated_card.id == card.id
    assert updated_card.back == new_back
    assert card.back == new_back

def test_update_card_mastery_level_success(test_db_session):
    """
    Tests that update_card_mastery correctly lowers the mastery level.
    """
    # Arrange
    from flash_zap.core.card_manager import update_card_mastery
    card = Card(front="Front", back="Back", mastery_level=3)
    test_db_session.add(card)
    test_db_session.commit()

    # Act
    updated_card, success = update_card_mastery(test_db_session, card.id, 1)
    test_db_session.refresh(card)

    # Assert
    assert success is True
    assert updated_card.mastery_level == 1
    assert card.mastery_level == 1

def test_update_card_mastery_level_fail_on_increase(test_db_session):
    """
    Tests that update_card_mastery fails if the new level is higher.
    """
    # Arrange
    from flash_zap.core.card_manager import update_card_mastery
    card = Card(front="Front", back="Back", mastery_level=3)
    test_db_session.add(card)
    test_db_session.commit()

    # Act
    updated_card, success = update_card_mastery(test_db_session, card.id, 4)
    test_db_session.refresh(card)

    # Assert
    assert success is False
    assert updated_card.mastery_level == 3
    assert card.mastery_level == 3 