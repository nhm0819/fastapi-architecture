from app.application.user.v1.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.core.db.transactional import Transactional
from app.core.helpers.token import TokenHelper
from app.domain.user.dto.login import LoginResponseDTO
from app.domain.user.dto.user import CreateUserDTO, UserRead
from app.domain.user.dto.vo import Location
from app.domain.user.entity.user import User
from app.domain.user.repository.user import UserRepository
from app.domain.user.usecase.user import UserUseCase


class UserService(UserUseCase):
    def __init__(self, *, repository: UserRepository):
        self.repository = repository

    async def get_user(
        self,
        *,
        user_id: int,
    ):
        return await self.repository.get_by_id(id=user_id)

    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        return await self.repository.get_users(limit=limit, prev=prev)

    @Transactional()
    async def create_user(self, *, command: CreateUserDTO) -> None:
        if command.password1 != command.password2:
            raise PasswordDoesNotMatchException

        is_exist = await self.repository.get_user_by_email_or_nickname(
            email=command.email,
            nickname=command.nickname,
        )
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User.create(
            email=command.email,
            password=command.password1,
            nickname=command.nickname,
            favorite=command.favorite,
            location=Location(lat=command.lat, lng=command.lng),
        )
        await self.repository.save(user=user)

    async def is_admin(self, *, user_id: int) -> bool:
        user = await self.repository.get_by_id(id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def login(
        self,
        *,
        email: str,
        password: str,
        access_expire_period: int = 60 * 30,
        refresh_expire_period: int = 60 * 60 * 2,
    ) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email_and_password(
            email=email,
            password=password,
        )
        if not user:
            raise UserNotFoundException

        response = LoginResponseDTO(
            access_token=TokenHelper.encode(
                payload={"user_id": user.id}, expire_period=access_expire_period
            ),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
            expire_period=refresh_expire_period,
        )
        return response


def get_user_service():
    return UserService(repository=UserRepository(User))
