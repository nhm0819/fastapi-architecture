from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, composite, mapped_column, relationship

from app.core.db.model import Base
from app.core.db.timestamp_mixin import TimestampMixin
from app.domain.personalization.entity.feature import UserFeature
from app.domain.user.dto.vo import Location


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False, deferred=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    favorite: Mapped[str] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    location: Mapped[Location] = composite(
        mapped_column("lat", nullable=True), mapped_column("lng", nullable=True)
    )
    feature: Mapped["UserFeature"] = relationship(back_populates="user")

    @classmethod
    def create(
        cls,
        *,
        email: str,
        password: str,
        nickname: str,
        favorite: str | None = None,
        is_admin: bool | None = False,
        location: Location | None = None,
        lat: float | None = None,
        lng: float | None = None,
    ) -> "User":
        if not location:
            location = location(lat=lat, lng=lng)
        return cls(
            email=email,
            password=password,
            nickname=nickname,
            favorite=favorite,
            is_admin=is_admin,
            location=location,
        )
