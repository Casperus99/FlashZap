from flash_zap.core.card_manager import get_card_by_id
from flash_zap.models.card import Card

def test_get_card_by_id_returns_card_when_found(test_db_session):
    """
    GIVEN: A card is present in the database.
    WHEN: The get_card_by_id function is called with the card's ID.
    THEN: The function returns the correct card object.
    """
    # GIVEN
    session = test_db_session
    expected_card = Card(front="Front", back="Back")
    session.add(expected_card)
    session.commit()

    # WHEN
    card = get_card_by_id(session, expected_card.id)

    # THEN
    assert card is not None
    assert card.id == expected_card.id
    assert card.front == "Front"
    assert card.back == "Back"


def test_get_card_by_id_returns_none_when_not_found(test_db_session):
    """
    GIVEN: A card ID that does not exist in the database.
    WHEN: The get_card_by_id function is called with the non-existent ID.
    THEN: The function returns None.
    """
    # GIVEN
    session = test_db_session

    # WHEN
    card = get_card_by_id(session, 999)

    # THEN
    assert card is None

def test_update_card_front(test_db_session):
    """
    GIVEN: An existing card in the database.
    WHEN: The update_card_front function is called with a new front content.
    THEN: The card's front content is successfully updated.
    """
    # GIVEN
    from flash_zap.core.card_manager import update_card_front
    session = test_db_session
    original_front = "Original Front"
    new_front = "New Front"
    card = Card(front=original_front, back="Back")
    session.add(card)
    session.commit()

    # WHEN
    updated_card = update_card_front(session, card.id, new_front)
    session.refresh(card)

    # THEN
    assert updated_card is not None
    assert updated_card.id == card.id
    assert updated_card.front == new_front
    assert card.front == new_front

def test_update_card_back(test_db_session):
    """
    GIVEN: An existing card in the database.
    WHEN: The update_card_back function is called with a new back content.
    THEN: The card's back content is successfully updated.
    """
    # GIVEN
    from flash_zap.core.card_manager import update_card_back
    session = test_db_session
    original_back = "Original Back"
    new_back = "New Back"
    card = Card(front="Front", back=original_back)
    session.add(card)
    session.commit()

    # WHEN
    updated_card = update_card_back(session, card.id, new_back)
    session.refresh(card)

    # THEN
    assert updated_card is not None
    assert updated_card.id == card.id
    assert updated_card.back == new_back
    assert card.back == new_back

def test_update_card_mastery_level_success(test_db_session):
    """
    GIVEN: An existing card with a certain mastery level.
    WHEN: The update_card_mastery function is called to lower the mastery level.
    THEN: The card's mastery level is successfully updated.
    """
    # GIVEN
    from flash_zap.core.card_manager import update_card_mastery
    session = test_db_session
    card = Card(front="Front", back="Back", mastery_level=3)
    session.add(card)
    session.commit()

    # WHEN
    updated_card, success = update_card_mastery(session, card.id, 1)
    session.refresh(card)

    # THEN
    assert success is True
    assert updated_card.mastery_level == 1
    assert card.mastery_level == 1

def test_update_card_mastery_level_fail_on_increase(test_db_session):
    """
    GIVEN: An existing card with a certain mastery level.
    WHEN: The update_card_mastery function is called to increase the mastery level.
    THEN: The card's mastery level remains unchanged and the operation fails.
    """
    # GIVEN
    from flash_zap.core.card_manager import update_card_mastery
    session = test_db_session
    card = Card(front="Front", back="Back", mastery_level=3)
    session.add(card)
    session.commit()

    # WHEN
    updated_card, success = update_card_mastery(session, card.id, 4)
    session.refresh(card)

    # THEN
    assert success is False
    assert updated_card.mastery_level == 3
    assert card.mastery_level == 3 