import pytest

from flash_zap.models.card import Card


def test_card_model_can_be_created():
    """
    GIVEN: Card model.
    WHEN: A new card is created.
    THEN: The card's attributes are correctly set.
    """
    # GIVEN
    front = "What is the capital of France?"
    back = "Paris"

    # WHEN
    card = Card(front=front, back=back)

    # THEN
    assert card.front == front
    assert card.back == back 