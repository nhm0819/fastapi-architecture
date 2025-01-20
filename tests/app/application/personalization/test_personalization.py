from copy import deepcopy
from unittest.mock import AsyncMock, patch

import numpy as np
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

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
async def test_create_user_feature_http(session: AsyncSession):

    # Given
    user = make_user(**users[1])
    user_feature = make_user_feature(**user_features[1])

    # Given
    session.add(user)
    await session.commit()
    # session.add(user_feature)
    # await session.commit()

    user_id = user_feature.user_id
    body = {
        "user_id": user_id,
        "protocol": "http",
        "size": 2048,
        "dtype": "float16",
    }

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            f"/api/v1/personalization/user/{user_id}", headers=HEADERS, json=body
        )

    # Then
    sut = response.json()
