import logging
from datetime import datetime, timedelta, timezone
from typing import List

from flash_zap.models.card import Card


class SRSEngine:
    """Handles the Spaced Repetition System (SRS) logic."""

    def __init__(self, srs_intervals: List[int]):
        """
        Initializes the SRSEngine with the configured intervals.

        Args:
            srs_intervals: A list of integers representing the review intervals
                           in days for each mastery level.
        """
        self._srs_intervals = srs_intervals 

    def promote_card(self, card: Card):
        """
        Promotes a card to the next mastery level and sets the next review date.

        If the card is already at the maximum level, it remains at the maximum
        level, but the review date is still pushed out.
        """
        logging.info(f"Promoting card id {card.id}. Current mastery level: {card.mastery_level}")
        current_level = card.mastery_level
        max_level = len(self._srs_intervals)

        if current_level < max_level:
            card.mastery_level += 1

        interval_index = min(current_level, max_level - 1)
        interval_days = self._srs_intervals[interval_index]

        card.next_review_date = datetime.now(timezone.utc) + timedelta(days=interval_days)
        logging.info(f"Card id {card.id} promoted to mastery level {card.mastery_level}. Next review in {interval_days} days.")

    def demote_card(self, card: Card):
        """
        Demotes a card to the previous mastery level and sets the next review date.

        A card's mastery level will not be demoted below level 0. If a card is at
        level 0, it remains at its current level, but the review date is reset
        based on the first interval.
        """
        logging.info(f"Demoting card id {card.id}. Current mastery level: {card.mastery_level}")
        current_level = card.mastery_level

        if current_level > 0:
            card.mastery_level -= 1

        # The interval for the *new* level. Level 1's interval is at index 0.
        # We use max(0, ...) to prevent a negative index for level 0.
        interval_index = max(0, card.mastery_level - 1)
        interval_days = self._srs_intervals[interval_index]
        card.next_review_date = datetime.now(timezone.utc) + timedelta(days=interval_days)
        logging.info(f"Card id {card.id} demoted to mastery level {card.mastery_level}. Next review in {interval_days} days.") 