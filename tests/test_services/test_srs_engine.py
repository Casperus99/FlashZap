from datetime import datetime, timedelta, timezone
import pytest

from flash_zap.models.card import Card
from flash_zap.services.srs_engine import SRSEngine


def test_promote_card_from_level_0():
    # Arrange
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=0)

    # Act
    srs_engine.promote_card(card)

    # Assert
    assert card.mastery_level == 1
    expected_date = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    assert card.next_review_date == expected_date


def test_promote_card_from_intermediate_level():
    # Arrange
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=2)

    # Act
    srs_engine.promote_card(card)

    # Assert
    assert card.mastery_level == 3
    expected_date = (datetime.now(timezone.utc) + timedelta(days=3)).date()
    assert card.next_review_date == expected_date


def test_promote_card_at_high_level():
    # Arrange
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=10)

    # Act
    srs_engine.promote_card(card)

    # Assert
    assert card.mastery_level == 11
    expected_date = (datetime.now(timezone.utc) + timedelta(days=11)).date()
    assert card.next_review_date == expected_date


def test_demote_card_from_intermediate_level():
    # Arrange
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=4)

    # Act
    srs_engine.demote_card(card)

    # Assert
    assert card.mastery_level == 3
    expected_date = (datetime.now(timezone.utc) + timedelta(days=3)).date()
    assert card.next_review_date == expected_date


def test_demote_card_at_level_1():
    # Arrange
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=1)

    # Act
    srs_engine.demote_card(card)

    # Assert
    assert card.mastery_level == 0
    expected_date = (datetime.now(timezone.utc) + timedelta(days=0)).date()
    assert card.next_review_date == expected_date


def test_demote_card_at_level_0():
    # Arrange
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=0)

    # Act
    srs_engine.demote_card(card)

    # Assert
    assert card.mastery_level == 0
    expected_date = (datetime.now(timezone.utc) + timedelta(days=0)).date()
    assert card.next_review_date == expected_date 