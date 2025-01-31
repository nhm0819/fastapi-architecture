import datetime
from abc import ABC, abstractmethod

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import load_only

from app.core.db.session import session, session_factory
from app.core.helpers.cache import Cache, CacheTag
from app.core.repository import BaseRepo
from app.domain.user.dto.user import UserRead
from app.domain.user.entity.user import User


class UserRepo(ABC):
    @abstractmethod
    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> User | None:
        """Get user by email or nickname"""

    @abstractmethod
    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> User | None:
        """Get user by email and password"""

    @abstractmethod
    async def save(self, *, user: User) -> None:
        """Save user"""


class UserRepository(BaseRepo[User]):
    def __init__(self, model: User = User):
        super().__init__(model=model)

    async def get_by_id(self, id: int) -> User | None:
        cached_user = await Cache.backend.get(key=f"user_id:{str(id)}")
        if cached_user:
            return cached_user
        query = select(self.model).where(self.model.id == id)
        async with session_factory() as read_session:
            result = await read_session.execute(query)
        user = result.scalars().first()

        await Cache.backend.set(response=user, key=f"user_id:{str(id)}")
        return user

    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        async with session_factory() as read_session:
            result = await read_session.execute(query)

        return result.scalars().all()

    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(User).where(or_(User.email == email, User.nickname == nickname)),
            )
            return stmt.scalars().first()

    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(User).where(and_(User.email == email, password == password))
            )
            return stmt.scalars().first()

    async def save(self, *, user: User) -> None:
        session.add(user)
