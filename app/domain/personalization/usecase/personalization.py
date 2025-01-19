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
        command: CreateUserFeatureDTO,
    ) -> GetUserFeatureDTO:
        """Get User Feature"""

    @abstractmethod
    async def create_user_feature(
        self,
        *,
        command: CreateUserFeatureDTO,
    ) -> GetUserFeatureDTO:
        """Create User Feature"""
