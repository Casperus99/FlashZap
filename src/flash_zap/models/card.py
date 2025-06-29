from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from flash_zap.models.base import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    front: Mapped[str] = mapped_column(String(200))
    back: Mapped[str] = mapped_column(String(200))

    def __init__(self, front: str, back: str):
        self.front = front
        self.back = back

    def __repr__(self) -> str:
        return f"Card(id={self.id!r}, front={self.front!r}, back={self.back!r})" 