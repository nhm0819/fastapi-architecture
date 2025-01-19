from typing import Union

import httpx
import numpy as np

from app.application.personalization.v1.exception import (
    EmbeddingException,
    UserFeatureAlreadyExistException,
    UserFeatureNotFoundException,
)
from app.application.personalization.v1.schema.request import UserEmbeddingRequestDTO
from app.application.personalization.v1.schema.response import (
    GetUserEmbeddingResponseDTO,
    UserEmbeddingResponseDTO,
)
from app.application.user.v1.exception import UserNotFoundException
from app.application.user.v1.service import UserService, get_user_service
from app.core.configs import config
from app.core.db.transactional import Transactional
from app.domain.personalization.dto.feature import (
    CreateUserFeatureDTO,
    GetUserFeatureDTO,
)
from app.domain.personalization.entity.feature import UserFeature
from app.domain.personalization.repository.feature import UserFeatureRepository
from app.domain.personalization.usecase.personalization import PersonalizationUseCase
from app.domain.user.entity.user import User
from app.domain.user.repository.user import UserRepository


async def get_embedding(
    user_id: Union[int, str],
    protocol: str,
    command: UserEmbeddingRequestDTO,
) -> GetUserEmbeddingResponseDTO:
    params = command.model_dump()

    if protocol == "http":
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.EMBEDDING_URL}/v1/embedding/user/{user_id}",
                json=params,
            )
            if response.status_code != 200:
                raise EmbeddingException(message=response.text)
            response_json = UserEmbeddingResponseDTO.model_validate(response.json())
            user_vector = response_json.user_vector
            bvector = np.array(user_vector, dtype=getattr(np, command.dtype)).tobytes()

    elif protocol == "http-octet":
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{config.EMBEDDING_URL}/v1/embedding/user/{user_id}/octet",
                json=params,
            )
            if resp.status_code != 200:
                raise EmbeddingException(message=resp.text)
            bvector = resp.content
            np_vector = np.expand_dims(
                np.frombuffer(bvector, dtype=getattr(np, command.dtype)), axis=0
            )
            user_vector = np_vector.astype(np.float64).tolist()

    else:
        # TODO : grpc embedding
        np_vector = None
        raise "Not yet grpc"

    return GetUserEmbeddingResponseDTO(
        bvector=bvector,
        user_vector=user_vector,
        # np_vector=np_vector,
    )


class PersonalizationService(PersonalizationUseCase):
    def __init__(
        self,
        user_feature_repository: UserFeatureRepository,
        user_service: UserService = get_user_service(),
    ):
        self.user_service = user_service
        self.user_feature_repository = user_feature_repository

    async def get_user_feature(self, *, user_id: int | str) -> GetUserFeatureDTO:
        user_id = user_id

        # user = await self.user_service.get_user(user_id=user_id)
        # if not user:
        #     raise UserNotFoundException

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if is_exist:
            np_vector = np.expand_dims(
                np.frombuffer(is_exist.bvector, dtype=getattr(np, is_exist.dtype)),
                axis=0,
            )
            user_vector = np_vector.astype(np.float64).tolist()
            return GetUserFeatureDTO(
                user_id=user_id,
                user_vector=user_vector,
            )
        else:
            raise UserFeatureNotFoundException

    @Transactional()
    async def create_user_feature(
        self,
        *,
        command: CreateUserFeatureDTO,
    ) -> GetUserFeatureDTO:
        user_id = command.user_id
        size = command.size
        protocol = command.protocol
        dtype = command.dtype

        user = await self.user_service.get_user(user_id=user_id)
        if not user:
            raise UserNotFoundException

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if is_exist:
            raise UserFeatureAlreadyExistException

        embedding_command = UserEmbeddingRequestDTO(
            size=size,
            dtype=dtype,
            email=user.email,
            nickname=user.nickname,
            favorite=user.favorite,
            lat=user.location.lat,
            lng=user.location.lng,
        )

        embedding_result = await get_embedding(
            user_id=user_id,
            protocol=protocol,
            command=embedding_command,
        )

        await self.user_feature_repository.save(
            user_feature=UserFeature.create(
                user_id=user_id,
                bvector=embedding_result.bvector,
                dtype=dtype,
            )
        )

        return GetUserFeatureDTO(
            user_id=user_id,
            user_vector=embedding_result.user_vector,
        )

    @Transactional()
    async def update_user_feature(
        self,
        *,
        command: CreateUserFeatureDTO,
    ) -> GetUserFeatureDTO:
        user_id = command.user_id
        size = command.size
        protocol = command.protocol
        dtype = command.dtype

        user = await self.user_service.get_user(user_id=user_id)
        if not user:
            raise UserNotFoundException

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if not is_exist:
            raise UserFeatureNotFoundException

        embedding_command = UserEmbeddingRequestDTO(
            size=size,
            dtype=dtype,
            email=user.email,
            nickname=user.nickname,
            favorite=user.favorite,
            lat=user.location.lat,
            lng=user.location.lng,
        )

        embedding_result = await get_embedding(
            user_id=user_id,
            protocol=protocol,
            command=embedding_command,
        )

        await self.user_feature_repository.update_by_id(
            id=is_exist.id,
            params={"bvector": embedding_result.bvector},
        )

        return GetUserFeatureDTO(
            user_id=user_id,
            user_vector=embedding_result.user_vector,
        )


def get_personalization_service():
    return PersonalizationService(
        user_feature_repository=UserFeatureRepository(UserFeature),
        user_service=get_user_service(),
    )
