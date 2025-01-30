from copy import deepcopy
from unittest.mock import AsyncMock

import pytest

from app.application.user.v1.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.application.user.v1.service import UserService
from app.core.helpers.token import TokenHelper
from app.domain.user.dto.user import CreateUserDTO, UserRead
from app.domain.user.repository.user import UserRepository
from tests.support.user_fixture import make_user, users

repository_mock = AsyncMock(spec=UserRepository)
user_service = UserService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_user_list():
    # Given
    user = make_user(**users[1])
    limit = 10
    prev = 0
    user = UserRead(id=user.id, email=user.email, nickname=user.nickname)
    repository_mock.get_users.return_value = [user]
    user_service.repository = repository_mock

    # When
    sut = await user_service.get_user_list(limit=limit, prev=prev)

    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.id == user.id
    assert result.email == user.email
    assert result.nickname == user.nickname
    user_service.repository.get_users.assert_awaited_once_with(limit=limit, prev=prev)


@pytest.mark.asyncio
async def test_create_user_password_does_not_match():
    # Given
    user = make_user(**users[1])
    command = CreateUserDTO(
        email=user.email,
        password1=user.password,
        password2=user.password + "2",
        nickname=user.nickname,
        lat=user.location.lat,
        lng=user.location.lng,
    )

    # When, Then
    with pytest.raises(PasswordDoesNotMatchException):
        await user_service.create_user(command=command)


@pytest.mark.asyncio
async def test_create_user_duplicated():
    # Given
    user = make_user(**users[1])
    command = CreateUserDTO(
        email=user.email,
        password1=user.password,
        password2=user.password,
        nickname=user.nickname,
        lat=user.location.lat,
        lng=user.location.lng,
    )

    repository_mock.get_user_by_email_or_nickname.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(DuplicateEmailOrNicknameException):
        await user_service.create_user(command=command)


@pytest.mark.asyncio
async def test_create_user():
    user = make_user(**users[1])

    # Given
    command = CreateUserDTO(
        email=user.email,
        password1=user.password,
        password2=user.password,
        nickname=user.nickname,
        favorite=user.favorite,
        lat=user.location.lat,
        lng=user.location.lng,
    )

    repository_mock.get_user_by_email_or_nickname.return_value = None
    user_service.repository = repository_mock

    # When
    await user_service.create_user(command=command)

    # Then
    repository_mock.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_is_admin_user_not_exist():
    # Given
    repository_mock.get_by_id.return_value = None
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=1)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin_user_is_not_admin():
    # Given

    user = make_user(**users[1])
    user.is_admin = False
    repository_mock.get_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin():
    # Given
    user = make_user(**users[1])
    repository_mock.get_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is True


@pytest.mark.asyncio
async def test_login_user_not_exist():
    # Given
    repository_mock.get_user_by_email_and_password.return_value = None
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UserNotFoundException):
        await user_service.login(email="email", password="password")


@pytest.mark.asyncio
async def test_login():
    # Given
    user = make_user(**users[1])
    repository_mock.get_user_by_email_and_password.return_value = user
    user_service.repository = repository_mock
    access_token = TokenHelper.encode(payload={"user_id": user.id})
    refresh_token = TokenHelper.encode(payload={"sub": "refresh"})

    # When
    sut = await user_service.login(email=user.email, password=user.password)

    # Then
    decoded_access_token = TokenHelper.decode(sut.access_token)
    assert user.id == decoded_access_token.get("user_id")
    assert sut.refresh_token == refresh_token
