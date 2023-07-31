from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger

from . import Base

if TYPE_CHECKING:
    from .user import User


class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement='auto')
    chat_id: Mapped[int] = mapped_column(BigInteger)
    type: Mapped[str]
    full_name: Mapped[str]
    user_rating: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship(back_populates="channels")
