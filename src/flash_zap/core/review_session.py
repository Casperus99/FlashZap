from sqlalchemy.orm import Session
from typing import Set, Tuple

from flash_zap.models.card import Card
from flash_zap.services import ai_grader


class ReviewSession:
    def __init__(self, db_session: Session):
        self._db = db_session
        self._seen_card_ids: Set[int] = set()

    def get_next_card(self) -> Card | None:
        card = (
            self._db.query(Card)
            .filter(Card.id.notin_(self._seen_card_ids))
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