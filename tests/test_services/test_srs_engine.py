from datetime import datetime, timedelta, timezone
import pytest

from flash_zap.models.card import Card
from flash_zap.services.srs_engine import SRSEngine, calculate_interval_days


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
    expected_date = (datetime.now(timezone.utc) + timedelta(days=18)).date()  # New algorithm: floor(18.531) = 18 days
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


def test_calculate_interval_days_level_0():
    """
    GIVEN: A mastery level of 0 and default learning rate.
    WHEN: calculate_interval_days is called.
    THEN: The interval should be 0 days.
    """
    # WHEN
    result = calculate_interval_days(0, learning_rate=0.1)
    
    # THEN
    assert result == 0


def test_calculate_interval_days_level_1():
    """
    GIVEN: A mastery level of 1 and default learning rate.
    WHEN: calculate_interval_days is called.
    THEN: The interval should be 1 day.
    """
    # WHEN
    result = calculate_interval_days(1, learning_rate=0.1)
    
    # THEN
    assert result == 1


def test_calculate_interval_days_level_2():
    """
    GIVEN: A mastery level of 2 and learning rate 0.1.
    WHEN: calculate_interval_days is called.
    THEN: The interval should be (1+0.1)^1 + previous_interval = 1.1 + 1 = 2.1.
    """
    # WHEN
    result = calculate_interval_days(2, learning_rate=0.1)
    
    # THEN
    assert result == 2.1


def test_calculate_interval_days_level_3():
    """
    GIVEN: A mastery level of 3 and learning rate 0.1.
    WHEN: calculate_interval_days is called.
    THEN: The interval should be (1+0.1)^2 + previous_interval = 1.21 + 2.1 = 3.31.
    """
    # WHEN
    result = calculate_interval_days(3, learning_rate=0.1)
    
    # THEN
    assert abs(result - 3.31) < 1e-10  # Using approximate equality for floating point


def test_calculate_interval_days_level_5():
    """
    GIVEN: A mastery level of 5 and learning rate 0.1.
    WHEN: calculate_interval_days is called.
    THEN: The interval should follow the recursive formula and return approximately 6.105.
    """
    # WHEN
    result = calculate_interval_days(5, learning_rate=0.1)
    
    # THEN
    assert abs(result - 6.1051) < 1e-3  # Using approximate equality for floating point


def test_calculate_interval_days_with_different_learning_rate():
    """
    GIVEN: A mastery level of 3 and learning rate 0.2 (higher than default).
    WHEN: calculate_interval_days is called.
    THEN: The interval should be larger than with learning rate 0.1.
    """
    # WHEN
    result_high_rate = calculate_interval_days(3, learning_rate=0.2)
    result_low_rate = calculate_interval_days(3, learning_rate=0.1)
    
    # THEN - higher learning rate should give longer intervals
    assert result_high_rate > result_low_rate
    # With learning_rate=0.2: (1+0.2)^2 + (1+0.2)^1 + 1 = 1.44 + 1.2 + 1 = 3.64
    assert abs(result_high_rate - 3.64) < 1e-10


def test_srs_engine_uses_configuration_learning_rate():
    """
    GIVEN: The default learning rate configuration is 0.1.
    WHEN: promote_card and demote_card are called.
    THEN: The SRS engine should use the configuration value for calculations.
    """
    # GIVEN
    from flash_zap.config import settings
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=2)  # Level 3 with 0.1 rate = ~3.31 days
    
    # WHEN - promote to level 3
    srs_engine.promote_card(card)
    
    # THEN - should use default learning rate (0.1) giving floor(3.31) = 3 days
    assert card.mastery_level == 3
    assert settings.SRS_LEARNING_RATE == 0.1  # Verify default config
    expected_date = (datetime.now(timezone.utc) + timedelta(days=3)).date()
    assert card.next_review_date == expected_date


def test_promote_demote_use_floored_values():
    """
    GIVEN: A card that will have fractional intervals.
    WHEN: promote_card and demote_card are called.
    THEN: The actual days scheduled should be floored integers.
    """
    # GIVEN
    srs_engine = SRSEngine()
    card = Card(front="Q", back="A", mastery_level=4)  # Level 5 will give ~6.105 days
    
    # WHEN - promote to level 5
    srs_engine.promote_card(card)
    
    # THEN - should use floor(6.105) = 6 days
    assert card.mastery_level == 5
    expected_date = (datetime.now(timezone.utc) + timedelta(days=6)).date()
    assert card.next_review_date == expected_date
    
    # WHEN - demote back to level 4  
    srs_engine.demote_card(card)
    
    # THEN - should use floor(4.641) = 4 days
    assert card.mastery_level == 4
    expected_date = (datetime.now(timezone.utc) + timedelta(days=4)).date()
    assert card.next_review_date == expected_date 