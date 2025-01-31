from abc import ABC, abstractmethod

from sqlalchemy import and_, delete, or_, select

from app.core.db.session import session, session_factory
from app.core.helpers.cache import Cache, CacheTag
from app.core.repository import BaseRepo
from app.domain.personalization.entity.feature import UserFeature


class UserFeatureRepository(BaseRepo[UserFeature]):
    def __init__(self, model: UserFeature = UserFeature):
        super().__init__(model=model)

    async def get_user_features(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserFeature]:
        query = select(UserFeature)

        if prev:
            query = query.where(UserFeature.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        async with session_factory() as read_session:
            result = await read_session.execute(query)

        return result.scalars().all()

    async def get_feature_by_user_id(self, *, user_id: int) -> UserFeature | None:
        cached_user_feature = await Cache.backend.get(
            key=f"get_feature_by_user_id:user_id:{str(user_id)}"
        )
        if cached_user_feature:
            return cached_user_feature

        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(UserFeature).where(UserFeature.user_id == user_id)
            )
            user_feature = stmt.scalars().first()

        await Cache.backend.set(
            response=user_feature, key=f"get_feature_by_user_id:user_id:{str(user_id)}"
        )
        return user_feature

    async def save(self, *, user_feature: UserFeature) -> UserFeature:
        session.add(user_feature)

    async def delete_feature_by_user_id(self, *, user_id: int) -> UserFeature | None:
        query = delete(self.model).where(self.model.user_id == user_id)
        return await session.execute(query)
