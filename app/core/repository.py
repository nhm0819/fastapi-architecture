from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, select, update

from app.core.db.model import Base
from app.core.db.session import session, session_factory

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        async with session_factory() as read_session:
            result = await read_session.execute(query)
        return result.scalars().first()

    async def update_by_id(
        self,
        id: int,
        params: dict,
    ) -> None:
        query = update(self.model).where(self.model.id == id).values(**params)
        await session.execute(query)

    async def delete(self, model: ModelType) -> None:
        await session.delete(model)

    async def delete_by_id(
        self,
        id: int,
    ) -> None:
        query = delete(self.model).where(self.model.id == id)
        await session.execute(query)

    async def save(self, model: ModelType) -> ModelType:
        saved = session.add(model)
        # saved = await session.add(model)
        return saved
