from copy import deepcopy
from unittest.mock import AsyncMock, patch

import numpy as np
import pytest

from app.application.personalization.v1.service import (
    PersonalizationService,
    get_personalization_service,
)
from app.application.user.v1.service import UserService
from app.domain.personalization.dto.feature import CreateUserFeatureDTO
from app.domain.personalization.repository.feature import UserFeatureRepository
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

    command = CreateUserFeatureDTO(
        user_id=user.id,
        protocol="http",
        dtype="float16",
    )

    user_service_mock.get_user.return_value = user

    user_feature_repository_mock = AsyncMock(spec=UserFeatureRepository)
    user_feature_repository_mock.get_feature_by_user_id.return_value = None

    personalization_service.user_feature_repository = user_feature_repository_mock
    personalization_service.user_service = user_service_mock

    # When
    await personalization_service.create_user_feature(command=command)

    # Then
    user_feature_repository_mock.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user_feature_http_octet():

    # Given
    user = make_user(**users[2])

    command = CreateUserFeatureDTO(
        user_id=user.id,
        protocol="http-octet",
        dtype="float16",
    )
    user_feature_repository_mock = AsyncMock(spec=UserFeatureRepository)

    user_service_mock.get_user.return_value = user
    user_feature_repository_mock.get_feature_by_user_id.return_value = None

    personalization_service.user_feature_repository = user_feature_repository_mock
    personalization_service.user_service = user_service_mock

    # When
    await personalization_service.create_user_feature(command=command)

    # Then
    user_feature_repository_mock.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_feature_http():

    # Given
    user = make_user(**users[2])
    user_feature = make_user_feature(**user_features[2])

    command = CreateUserFeatureDTO(
        user_id=user.id,
        protocol="http",
        dtype="float16",
        regen=True,
    )

    user_service_mock.get_user.return_value = user
    user_feature_repository_mock.get_feature_by_user_id.return_value = user_feature

    personalization_service.user_feature_repository = user_feature_repository_mock
    personalization_service.user_service = user_service_mock

    # When
    await personalization_service.update_user_feature(command=command)

    # Then
    user_feature_repository_mock.update_by_id.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_feature():

    # Given
    user = make_user(**users[2])
    user_feature = make_user_feature(**user_features[2])

    user_service_mock.get_user.return_value = user
    user_feature_repository_mock.get_feature_by_user_id.return_value = user_feature

    personalization_service.user_feature_repository = user_feature_repository_mock
    personalization_service.user_service = user_service_mock

    # When
    result = await personalization_service.get_user_feature(user_id=user.id)

    # Then
    np_vector = np.expand_dims(
        np.frombuffer(user_feature.bvector, dtype=getattr(np, user_feature.dtype)),
        axis=0,
    )
    user_vector = np_vector.astype(np.float64).tolist()
    assert result.user_id == user_feature.user_id
    assert result.user_vector == user_vector
