from copy import deepcopy
from unittest.mock import AsyncMock, patch

import numpy as np
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.personalization.v1.enums import BigEndian
from app.application.personalization.v1.service import (
    PersonalizationService,
    get_personalization_service,
)
from app.application.user.v1.service import UserService
from app.domain.personalization.dto.feature import CreateUserFeatureDTO
from app.domain.personalization.repository.feature import UserFeatureRepository
from app.main import app
from tests.support.feature_fixture import make_user_feature, user_features
from tests.support.token import USER_ID_1_ACCESS_TOKEN
from tests.support.user_fixture import make_user, users

HEADERS = {"Authorization": f"Bearer {USER_ID_1_ACCESS_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_personalization_create_user_http(session: AsyncSession):

    # Given
    user = make_user(**users[1])
    user_feature = make_user_feature(**user_features[1])

    # Given
    session.add(user)
    await session.commit()
    # session.add(user_feature)
    # await session.commit()

    user_id = user_feature.user_id
    protocol = "http"
    size = 2048
    dtype = "float16"
    body = {
        "protocol": protocol,
        "size": size,
        "dtype": dtype,
    }

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            f"/api/v1/personalization/user", headers=HEADERS, json=body
        )

    # Then
    sut = response.json()

    np_vector = np.array(sut["user_vector"])
    sut_bvector = np_vector.astype(BigEndian[user_feature.dtype].value).tobytes()

    assert -0.1 < np.mean(np_vector) < 0.1
    assert 0.9 < np.std(np_vector) < 1.1

    assert isinstance(sut["user_vector"], list)
    assert len(sut["user_vector"][0]) == size


@pytest.mark.asyncio
async def test_personalization_update_user_http(session: AsyncSession):

    # Given
    user = make_user(**users[1])
    user_feature = make_user_feature(**user_features[1])
    np_vector = np.expand_dims(
        np.frombuffer(user_feature.bvector, dtype=BigEndian[user_feature.dtype].value),
        axis=0,
    )
    user_vector = np_vector.astype(np.float64).tolist()

    # Given
    session.add(user)
    await session.commit()
    session.add(user_feature)
    await session.commit()

    user_id = user_feature.user_id
    size = 2048
    dtype = "float16"
    body = {
        "size": size,
        "dtype": dtype,
    }

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.patch(
            f"/api/v1/personalization/user", headers=HEADERS, json=body
        )

    # Then
    sut = response.json()

    assert response.status_code == 200
    assert isinstance(sut["user_vector"], list)
    assert len(sut["user_vector"][0]) == size


@pytest.mark.asyncio
async def test_personalization_update_user_grpc(session: AsyncSession):

    # Given
    user = make_user(**users[1])
    user_feature = make_user_feature(**user_features[1])
    np_vector = np.expand_dims(
        np.frombuffer(user_feature.bvector, dtype=BigEndian[user_feature.dtype].value),
        axis=0,
    )
    user_vector = np_vector.astype(np.float64).tolist()

    # Given
    session.add(user)
    await session.commit()
    session.add(user_feature)
    await session.commit()

    user_id = user_feature.user_id
    size = 2048
    dtype = "float16"
    body = {
        "size": size,
        "dtype": dtype,
    }

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.patch(
            f"/api/v1/personalization/user", headers=HEADERS, json=body
        )

    # Then
    sut = response.json()

    assert response.status_code == 200
    assert isinstance(sut["user_vector"], list)
    assert len(sut["user_vector"][0]) == size


@pytest.mark.asyncio
async def test_personalization_get_user_http(session: AsyncSession):

    # Given
    user = make_user(**users[1])
    user_feature = make_user_feature(**user_features[1])

    # Given
    session.add(user)
    session.add(user_feature)
    await session.commit()

    user_id = user_feature.user_id
    protocol = "http"
    size = 2048
    dtype = "float16"

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            f"/api/v1/personalization/user",
            headers=HEADERS,
        )

    # Then
    sut = response.json()

    np_vector = np.array(sut["user_vector"])
    sut_bvector = np_vector.astype(BigEndian[user_feature.dtype].value).tobytes()

    assert -0.1 < np.mean(np_vector) < 0.1
    assert 0.9 < np.std(np_vector) < 1.1

    assert sut_bvector == user_feature.bvector


@pytest.mark.asyncio
async def test_personalization_get_user_http_octet(session: AsyncSession):

    # Given
    user = make_user(**users[1])
    user_feature = make_user_feature(**user_features[1])

    # Given
    session.add(user)
    session.add(user_feature)
    await session.commit()

    user_id = user_feature.user_id
    protocol = "http"
    size = 2048
    dtype = "float16"

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            f"/api/v1/personalization/user/octet",
            headers=HEADERS,
        )

    # Then
    sut = response.content

    np_vector = np.expand_dims(
        np.frombuffer(sut, dtype=BigEndian[user_feature.dtype].value),
        axis=0,
    )

    assert -0.1 < np.mean(np_vector) < 0.1
    assert 0.9 < np.std(np_vector) < 1.1

    assert sut == user_feature.bvector
