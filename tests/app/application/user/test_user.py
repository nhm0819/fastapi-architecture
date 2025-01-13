import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.user.v1.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.domain.user.repository.user import UserRepository
from app.main import app
from tests.support.token import USER_ID_1_ACCESS_TOKEN
from tests.support.user_fixture import make_user

HEADERS = {"Authorization": f"Bearer {USER_ID_1_ACCESS_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="hongmin@id.e",
        nickname="hongma",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/user", headers=HEADERS)

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {"id": 1, "email": "hongmin@id.e", "nickname": "hongma"}


@pytest.mark.asyncio
async def test_create_user_password_does_not_match(session: AsyncSession):
    # Given
    body = {
        "email": "hongmin@id.e",
        "password1": "password",
        "password2": "password2",
        "nickname": "hongma",
        "lat": 37.123,
        "lng": 127.123,
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
    user = make_user(
        id=1,
        password="password",
        email="hongmin@id.e",
        nickname="hongma",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    body = {
        "email": "hongmin@id.e",
        "password1": "password",
        "password2": "password",
        "nickname": "hongma",
        "lat": 37.123,
        "lng": 127.123,
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
    email = "hongmin@id.e"
    nickname = "hongma"
    body = {
        "email": email,
        "password1": "password",
        "password2": "password",
        "nickname": nickname,
        "lat": 37.123,
        "lng": 127.123,
    }

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {"email": email, "nickname": nickname}

    user_repo = UserRepository()
    sut = await user_repo.get_user_by_email_or_nickname(nickname=nickname, email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_login_user_not_found(session: AsyncSession):
    # Given
    email = "hongmin@id.e"
    password = "password"
    body = {"email": email, "password": password}
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
    email = "hongmin@id.e"
    password = "password"
    user = make_user(
        id=1,
        password=password,
        email=email,
        nickname="hongma",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    body = {"email": email, "password": password}

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/user/login", headers=HEADERS, json=body)

    # Then
    sut = response.json()

    assert "access_token" in sut
    assert "refresh_token" in sut
