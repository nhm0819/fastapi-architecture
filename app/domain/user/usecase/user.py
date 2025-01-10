from abc import ABC, abstractmethod

from app.domain.user.dto.login import LoginResponseDTO
from app.domain.user.dto.user import CreateUserDTO
from app.domain.user.entity.user import User


class UserUseCase(ABC):
    @abstractmethod
    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def create_user(self, *, command: CreateUserDTO) -> None:
        """Create User"""

    @abstractmethod
    async def is_admin(self, *, user_id: int) -> bool:
        """Is admin"""

    @abstractmethod
    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        """Login"""
