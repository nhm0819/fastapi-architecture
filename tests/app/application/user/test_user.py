from copy import deepcopy

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.user.v1.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.domain.user.entity.user import User
from app.domain.user.repository.user import UserRepository
from app.main import app
from tests.support.token import USER_ID_1_ACCESS_TOKEN
from tests.support.user_fixture import make_user, users

HEADERS = {"Authorization": f"Bearer {USER_ID_1_ACCESS_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_user_list(session: AsyncSession):
    # Given
    user = make_user(**users[1])
    session.add(user)
    await session.commit()

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/user/list", headers=HEADERS)

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {"id": user.id, "email": user.email, "nickname": user.nickname}


@pytest.mark.asyncio
async def test_create_user_password_does_not_match(session: AsyncSession):
    # Given
    user = make_user(**users[1])
    body = {
        "email": user.email,
        "password1": user.password,
        "password2": user.password + "2",
        "nickname": user.nickname,
        "favorite": user.favorite,
        "lat": user.location.lat,
        "lng": user.location.lng,
    }
    exc = PasswordDoesNotMatchException

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user_duplicated_user(session: AsyncSession):
    # Given
    user = make_user(**users[1])
    session.add(user)
    await session.commit()

    body = {
        "email": user.email,
        "password1": user.password,
        "password2": user.password,
        "nickname": user.nickname,
        "favorite": user.favorite,
        "lat": user.location.lat,
        "lng": user.location.lng,
    }
    exc = DuplicateEmailOrNicknameException

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    # Given
    user = make_user(**users[1])
    body = {
        "email": user.email,
        "password1": user.password,
        "password2": user.password,
        "nickname": user.nickname,
        "favorite": user.favorite,
        "lat": user.location.lat,
        "lng": user.location.lng,
    }

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {"email": user.email, "nickname": user.nickname}

    user_repo = UserRepository(User)
    sut = await user_repo.get_user_by_email_or_nickname(
        nickname=user.nickname, email=user.email
    )
    assert sut is not None
    assert sut.email == user.email
    assert sut.nickname == user.nickname


@pytest.mark.asyncio
async def test_login_user_not_found(session: AsyncSession):
    # Given
    user = make_user(**users[1])
    body = {"email": user.email, "password": user.password}
    exc = UserNotFoundException

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/user/login", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_login(session: AsyncSession):
    # Given
    user = make_user(**users[1])
    session.add(user)
    await session.commit()

    body = {"email": user.email, "password": user.password}

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/user/login", headers=HEADERS, json=body)

    # Then
    sut = response.json()

    assert "access_token" in sut
    assert "refresh_token" in sut
