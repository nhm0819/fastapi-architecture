from abc import ABC, abstractmethod

from app.domain.personalization.dto.feature import (
    CreateUserFeatureDTO,
    GetUserFeatureDTO,
)


class PersonalizationUseCase(ABC):
    @abstractmethod
    async def get_user_feature(
        self,
        *,
        user_id: int | str,
    ) -> GetUserFeatureDTO:
        """Get User Feature"""

    @abstractmethod
    async def get_user_feature_binary(
        self,
        *,
        user_id: int | str,
    ) -> bytes:
        """Get User Feature"""

    @abstractmethod
    async def create_user_feature(
        self,
        *,
        user_id: int | str,
        command: CreateUserFeatureDTO,
    ) -> GetUserFeatureDTO:
        """Create User Feature"""

    @abstractmethod
    async def update_user_feature(
        self,
        *,
        user_id: int | str,
        command: CreateUserFeatureDTO,
    ) -> GetUserFeatureDTO:
        """Update User Feature"""

    @abstractmethod
    async def delete_user_feature(
        self,
        *,
        user_id: int | str,
    ) -> GetUserFeatureDTO:
        """Delete User Feature"""
