import logging
from datetime import datetime, timedelta, timezone
from math import floor
from typing import List

from flash_zap.models.card import Card
from flash_zap.config import settings


def calculate_interval_days(mastery_level: int, learning_rate: float = 0.1) -> float:
    """
    Calculate the number of days until the next review based on mastery level.
    Uses a recursive algorithm with exponential growth.
    
    Args:
        mastery_level: The current mastery level of the card
        learning_rate: The learning rate parameter that controls growth speed (default: 0.1)
    """
    if mastery_level == 0:
        interval_days = 0
    elif mastery_level == 1:
        interval_days = 1
    elif mastery_level > 1:
        interval_days = (1+learning_rate)**(mastery_level-1) + calculate_interval_days(mastery_level-1, learning_rate)
    else:
        interval_days = 0  # Handle negative values
    
    return interval_days


class SRSEngine:
    """Handles the Spaced Repetition System (SRS) logic."""

    def promote_card(self, card: Card):
        """
        Promotes a card to the next mastery level and sets the next review date.
        """
        logging.info(f"Promoting card id {card.id}. Current mastery level: {card.mastery_level}")
        card.mastery_level += 1

        interval_days = floor(calculate_interval_days(card.mastery_level, settings.SRS_LEARNING_RATE))
        card.next_review_date = (datetime.now(timezone.utc) + timedelta(days=interval_days)).date()
        logging.info(f"Card id {card.id} promoted to mastery level {card.mastery_level}. Next review in {interval_days} days.")

    def demote_card(self, card: Card):
        """
        Demotes a card to the previous mastery level and sets the next review date.

        A card's mastery level will not be demoted below level 0.
        """
        logging.info(f"Demoting card id {card.id}. Current mastery level: {card.mastery_level}")
        if card.mastery_level > 0:
            card.mastery_level -= 1

        interval_days = floor(calculate_interval_days(card.mastery_level, settings.SRS_LEARNING_RATE))
        card.next_review_date = (datetime.now(timezone.utc) + timedelta(days=interval_days)).date()
        logging.info(f"Card id {card.id} demoted to mastery level {card.mastery_level}. Next review in {interval_days} days.")



