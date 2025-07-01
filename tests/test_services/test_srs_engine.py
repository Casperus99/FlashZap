from datetime import datetime, timedelta, timezone
import pytest

from flash_zap.models.card import Card
from flash_zap.services.srs_engine import SRSEngine


def test_promote_card_from_level_0():
    # Arrange
    srs_intervals = [1, 3, 7]
    srs_engine = SRSEngine(srs_intervals)
    card = Card(front="Q", back="A", mastery_level=0)

    # Act
    srs_engine.promote_card(card)

    # Assert
    assert card.mastery_level == 1
    expected_date = datetime.now(timezone.utc).date() + timedelta(days=srs_intervals[0])
    assert card.next_review_date.date() == expected_date


def test_promote_card_from_intermediate_level():
    # Arrange
    srs_intervals = [1, 3, 7, 14]
    srs_engine = SRSEngine(srs_intervals)
    card = Card(front="Q", back="A", mastery_level=2)

    # Act
    srs_engine.promote_card(card)

    # Assert
    assert card.mastery_level == 3
    expected_date = datetime.now(timezone.utc).date() + timedelta(days=srs_intervals[2])
    assert card.next_review_date.date() == expected_date


def test_promote_card_at_max_level():
    # Arrange
    srs_intervals = [1, 3, 7]
    srs_engine = SRSEngine(srs_intervals)
    max_level = len(srs_intervals)
    card = Card(front="Q", back="A", mastery_level=max_level)

    # Act
    srs_engine.promote_card(card)

    # Assert
    assert card.mastery_level == max_level
    expected_date = datetime.now(timezone.utc).date() + timedelta(days=srs_intervals[-1])
    assert card.next_review_date.date() == expected_date


def test_demote_card_from_intermediate_level():
    # Arrange
    srs_intervals = [1, 3, 7, 14, 30]
    srs_engine = SRSEngine(srs_intervals)
    card = Card(front="Q", back="A", mastery_level=4)

    # Act
    srs_engine.demote_card(card)

    # Assert
    assert card.mastery_level == 3
    expected_date = datetime.now(timezone.utc).date() + timedelta(days=srs_intervals[2])
    assert card.next_review_date.date() == expected_date


def test_demote_card_at_level_1():
    # Arrange
    srs_intervals = [1, 3, 7]
    srs_engine = SRSEngine(srs_intervals)
    card = Card(front="Q", back="A", mastery_level=1)

    # Act
    srs_engine.demote_card(card)

    # Assert
    assert card.mastery_level == 0
    # The next review should still be based on the first interval
    expected_date = datetime.now(timezone.utc).date() + timedelta(days=srs_intervals[0])
    assert card.next_review_date.date() == expected_date


def test_demote_card_at_level_0():
    # Arrange
    srs_intervals = [1, 3, 7]
    srs_engine = SRSEngine(srs_intervals)
    card = Card(front="Q", back="A", mastery_level=0)

    # Act
    srs_engine.demote_card(card)

    # Assert
    assert card.mastery_level == 0
    expected_date = datetime.now(timezone.utc).date() + timedelta(days=srs_intervals[0])
    assert card.next_review_date.date() == expected_date 