from copy import deepcopy
from unittest.mock import AsyncMock

import pytest

from app.application.personalization.v1.service import (
    PersonalizationService,
    get_personalization_service,
)
from app.application.user.v1.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.application.user.v1.service import UserService
from app.core.helpers.token import TokenHelper
from app.domain.personalization.dto.feature import CreateUserFeatureDTO
from app.domain.personalization.repository.feature import UserFeatureRepository
from app.domain.user.dto.user import CreateUserDTO, UserRead
from app.domain.user.entity.user import User
from app.domain.user.repository.user import UserRepository
from tests.app.domain.user.test_domain_user import user_service
from tests.support.feature_fixture import make_user_feature, user_features
from tests.support.user_fixture import make_user, users

user_feature_repository_mock = AsyncMock(spec=UserFeatureRepository)
user_service_mock = AsyncMock(spec=UserService)
personalization_service = PersonalizationService(
    user_feature_repository=user_feature_repository_mock,
    user_service=user_service_mock,
)


@pytest.mark.asyncio
async def test_create_user_feature_http():

    # Given
    user = make_user(**users[2])
    # user_feature = make_user_feature(**user_features[1])

    # user_create_command = CreateUserDTO(
    #     email=user.email,
    #     password1=user.password,
    #     password2=user.password,
    #     nickname=user.nickname,
    #     favorite=user.favorite,
    #     lat=user.location.lat,
    #     lng=user.location.lng,
    # )
    # await user_service.create_user(user_create_command)

    command = CreateUserFeatureDTO(
        user_id=user.id,
        protocol="http",
        dtype="float16",
    )

    user_service_mock.get_user.return_value = user
    user_feature_repository_mock.get_feature_by_user_id.return_value = None

    personalization_service.user_feature_repository = user_feature_repository_mock
    personalization_service.user_service = user_service_mock

    # When
    await personalization_service.create_user_feature(command=command)

    # Then
    # user_feature_repository_mock.update_by_id.assert_awaited_once()
    user_feature_repository_mock.save.assert_awaited_once()
