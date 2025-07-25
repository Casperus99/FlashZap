from datetime import date, datetime, timezone
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
from typing import Set, Tuple, List
import logging
import random

from flash_zap.models.card import Card
from flash_zap.services import ai_grader
from flash_zap.services.srs_engine import SRSEngine
from flash_zap import config


class ReviewSession:
    def __init__(self, db_session: Session, shuffle: bool = True):
        self._db = db_session
        self._srs_engine = SRSEngine()
        self._review_deck: List[Card] = self._get_due_cards(shuffle)

    def _get_due_cards(self, shuffle: bool = True) -> List[Card]:
        today = datetime.now(timezone.utc).date()
        due_cards = self._db.query(Card).filter(
            or_(Card.next_review_date <= today, Card.next_review_date == None)
        ).all()
        if shuffle:
            random.shuffle(due_cards)
        return due_cards

    @property
    def remaining_cards_count(self) -> int:
        return len(self._review_deck)

    def get_next_card(self) -> Card | None:
        if not self._review_deck:
            return None
        return self._review_deck[0]

    def process_answer(self, card: Card, user_answer: str) -> Tuple[str, str]:
        return ai_grader.grade_answer(
            question=card.front,
            user_answer=user_answer,
            correct_answer=card.back,
        )

    def grade_and_update_card(self, card: Card, user_answer: str) -> Tuple[str, str, int, int]:
        grade, feedback = self.process_answer(card, user_answer)
        logging.info(f"AI graded card id {card.id} as '{grade}'.")

        old_mastery_level = card.mastery_level

        if grade == "Correct":
            self._srs_engine.promote_card(card)
            # Remove card from the front of the deck
            self._review_deck.pop(0)
        else:
            self._srs_engine.demote_card(card)
            # If mastery level drops to 0, it needs immediate re-review in this session.
            if card.mastery_level == 0:
                # Move card to the back of the deck to be reviewed again.
                card_to_review_again = self._review_deck.pop(0)
                self._review_deck.append(card_to_review_again)
            else:
                # Otherwise, remove from session and it will be reviewed on its next scheduled date.
                self._review_deck.pop(0)
        
        self._db.commit()
        # Refresh the card to get the latest state from database
        self._db.refresh(card)
        new_mastery_level = card.mastery_level
        

        
        return grade, feedback, old_mastery_level, new_mastery_level 