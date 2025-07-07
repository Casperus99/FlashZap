from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime, timezone
from typing import Optional

from flash_zap.models.base import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    front: Mapped[str] = mapped_column(String(200))
    back: Mapped[str] = mapped_column(String(200))
    mastery_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    next_review_date: Mapped[date] = mapped_column(Date, default=lambda: datetime.now(timezone.utc).date(), nullable=False)

    def __init__(self, front: str, back: str, mastery_level: int = 0, next_review_date: Optional[date] = None):
        self.front = front
        self.back = back
        self.mastery_level = mastery_level
        if next_review_date is None:
            self.next_review_date = datetime.now(timezone.utc).date()
        else:
            self.next_review_date = next_review_date

    def __repr__(self) -> str:
        return (f"Card(id={self.id!r}, front={self.front!r}, back={self.back!r}, "
                f"mastery_level={self.mastery_level!r}, next_review_date={self.next_review_date!r})") 