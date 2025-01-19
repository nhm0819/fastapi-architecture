from __future__ import annotations

from sqlalchemy import VARBINARY, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.model import Base
from app.core.db.timestamp_mixin import TimestampMixin

# from app.domain.user.entity.user import User


class UserFeature(Base, TimestampMixin):
    __tablename__ = "user_feature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    bvector: Mapped[bytes] = mapped_column(VARBINARY(4096), nullable=False)
    dtype: Mapped[str] = mapped_column(String(100), default="float16", nullable=False)
    user: Mapped["User"] = relationship(back_populates="feature")  # type: ignore

    @classmethod
    def create(cls, *, user_id: int, bvector: bytes, dtype: str) -> "UserFeature":
        return cls(
            user_id=user_id,
            bvector=bvector,
            dtype=dtype,
        )
