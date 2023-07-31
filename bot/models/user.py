from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger
from . import Base

if TYPE_CHECKING:
    from .channels import Channel


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    full_name: Mapped[str]
    username: Mapped[str | None]
    is_premium: Mapped[bool | None]

    channels: Mapped[list["Channel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"User(user_id={self.user_id!r}, full_name={self.full_name!r})"

    def __repr__(self) -> str:
        return str(self)
