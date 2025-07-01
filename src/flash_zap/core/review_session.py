from datetime import datetime, timezone
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Set, Tuple, List

from flash_zap.models.card import Card
from flash_zap.services import ai_grader
from flash_zap.services.srs_engine import SRSEngine
from flash_zap import config


class ReviewSession:
    def __init__(self, db_session: Session):
        self._db = db_session
        self._seen_card_ids: Set[int] = set()
        self._srs_engine = SRSEngine(config.settings.SRS_INTERVALS)

    def get_next_card(self) -> Card | None:
        now = datetime.now(timezone.utc)
        card = (
            self._db.query(Card)
            .filter(
                or_(Card.next_review_date <= now, Card.next_review_date == None),
                Card.id.notin_(self._seen_card_ids),
            )
            .first()
        )
        if card:
            self._seen_card_ids.add(card.id)
        return card

    def process_answer(self, card: Card, user_answer: str) -> Tuple[str, str]:
        return ai_grader.grade_answer(
            user_answer=user_answer,
            correct_answer=card.back,
        )

    def grade_and_update_card(self, card: Card, user_answer: str) -> Tuple[str, str]:
        grade, feedback = self.process_answer(card, user_answer)

        if grade == "Correct":
            self._srs_engine.promote_card(card)
        else:
            self._srs_engine.demote_card(card)
        
        self._db.commit()
        return grade, feedback 