import logging
from typing import Union

import grpc
import httpx
import numpy as np

from app.application.personalization.v1.enums import BigEndian
from app.application.personalization.v1.exception import (
    EmbeddingException,
    EmbeddingGrpcException,
    UserFeatureAlreadyExistException,
    UserFeatureNotFoundException,
)
from app.application.personalization.v1.proto.embedding_pb2 import (
    EmbeddingUserRequest,
    EmbeddingUserResponse,
)
from app.application.personalization.v1.proto.embedding_pb2_grpc import (
    EmbeddingServiceStub,
)
from app.application.personalization.v1.schema.request import (
    CreateUserFeatureRequest,
    UserEmbeddingRequest,
)
from app.application.personalization.v1.schema.response import (
    DeleteUserFeatureResponse,
    GetUserEmbeddingResponse,
    GetUserFeatureResponse,
    UserEmbeddingResponse,
)
from app.application.user.v1.exception import UserNotFoundException
from app.core.configs import config
from app.core.db.transactional import Transactional
from app.domain.personalization.entity.feature import UserFeature
from app.domain.personalization.repository.feature import UserFeatureRepository
from app.domain.personalization.usecase.personalization import PersonalizationUseCase
from app.domain.user.repository.user import UserRepository


class PersonalizationService(PersonalizationUseCase):
    def __init__(
        self,
        user_feature_repository: UserFeatureRepository,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository
        self.user_feature_repository = user_feature_repository

    async def _check_user(self, user_id: int | str):
        user_id = user_id

        user = await self.user_repository.get_by_id(id=user_id)
        if not user:
            raise UserNotFoundException
        return user

    async def get_user_feature_binary(self, *, user_id: int | str) -> bytes:
        user = await self._check_user(user_id=user_id)

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if is_exist:
            return is_exist.bvector
        else:
            raise UserFeatureNotFoundException

    async def get_user_feature(self, *, user_id: int | str) -> GetUserFeatureResponse:
        user = await self._check_user(user_id=user_id)

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if is_exist:
            np_vector = np.expand_dims(
                np.frombuffer(is_exist.bvector, dtype=BigEndian[is_exist.dtype].value),
                axis=0,
            )
            user_vector = np_vector.astype(np.float64).tolist()
            return GetUserFeatureResponse(
                user_vector=user_vector, size=is_exist.size, dtype=is_exist.dtype
            )
        else:
            raise UserFeatureNotFoundException

    @Transactional()
    async def create_user_feature(
        self,
        *,
        user_id: int | str,
        command: CreateUserFeatureRequest,
        stub: EmbeddingServiceStub | None = None,
        return_binary: bool = False,
    ) -> GetUserFeatureResponse | bytes:
        size = command.size
        protocol = command.protocol
        dtype = command.dtype

        user = await self.user_repository.get_by_id(id=user_id)
        if not user:
            raise UserNotFoundException

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if is_exist:
            raise UserFeatureAlreadyExistException

        embedding_command = UserEmbeddingRequest(
            size=size,
            dtype=dtype,
            email=user.email,
            nickname=user.nickname,
            favorite=user.favorite,
            lat=user.location.lat,
            lng=user.location.lng,
        )

        embedding_result = await self._get_embedding(
            user_id=user_id,
            protocol=protocol,
            command=embedding_command,
            stub=stub,
            return_binary=return_binary,
        )

        await self.user_feature_repository.save(
            user_feature=UserFeature.create(
                user_id=user_id,
                bvector=embedding_result.bvector,
                size=size,
                dtype=dtype,
            )
        )

        if return_binary:
            return embedding_result.bvector
        else:
            return GetUserFeatureResponse(
                user_vector=embedding_result.user_vector, size=size, dtype=dtype
            )

    @Transactional()
    async def update_user_feature(
        self,
        *,
        user_id: int | str,
        command: CreateUserFeatureRequest,
        stub: EmbeddingServiceStub | None = None,
        return_binary: bool = False,
    ) -> GetUserFeatureResponse | bytes:
        size = command.size
        protocol = command.protocol
        dtype = command.dtype

        user = await self.user_repository.get_by_id(id=user_id)
        if not user:
            raise UserNotFoundException

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if not is_exist:
            raise UserFeatureNotFoundException

        embedding_command = UserEmbeddingRequest(
            size=size,
            dtype=dtype,
            email=user.email,
            nickname=user.nickname,
            favorite=user.favorite,
            lat=user.location.lat,
            lng=user.location.lng,
        )

        embedding_result = await self._get_embedding(
            user_id=user_id,
            protocol=protocol,
            command=embedding_command,
            stub=stub,
            return_binary=return_binary,
        )

        await self.user_feature_repository.update_by_id(
            id=is_exist.id,
            params={"bvector": embedding_result.bvector},
        )

        if return_binary:
            return embedding_result.bvector
        else:
            return GetUserFeatureResponse(
                user_vector=embedding_result.user_vector, size=size, dtype=dtype
            )

    @Transactional()
    async def delete_user_feature(
        self,
        *,
        user_id: int | str,
    ) -> DeleteUserFeatureResponse:
        user_id = user_id

        user = await self.user_repository.get_by_id(id=user_id)
        if not user:
            raise UserNotFoundException

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        if not is_exist:
            raise UserFeatureNotFoundException

        await self.user_feature_repository.delete_feature_by_user_id(user_id=user_id)

        return DeleteUserFeatureResponse(
            id=is_exist.id,
            user_id=is_exist.user_id,
            size=is_exist.size,
            dtype=is_exist.dtype,
        )

    @staticmethod
    async def _get_embedding(
        user_id: Union[int, str],
        protocol: str,
        command: UserEmbeddingRequest,
        stub: EmbeddingServiceStub | None = None,
        return_binary: bool = False,
    ) -> GetUserEmbeddingResponse:
        params = command.model_dump()

        if protocol == "http":
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{config.EMBEDDING_URL}/v1/embedding/user/{user_id}",
                    json=params,
                )
                if response.status_code != 200:
                    raise EmbeddingException(message=response.text)
                response_json = UserEmbeddingResponse.model_validate(response.json())
                user_vector = response_json.user_vector
                bvector = (
                    np.array(user_vector)
                    .astype(BigEndian[command.dtype].value)
                    .tobytes()
                )

        elif protocol == "http-octet":
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{config.EMBEDDING_URL}/v1/embedding/user/{user_id}/octet",
                    json=params,
                )
                if resp.status_code != 200:
                    raise EmbeddingException(message=resp.text)
                bvector = resp.content
                if return_binary:
                    return GetUserEmbeddingResponse(
                        bvector=bvector,
                        user_vector=None,
                    )

                np_vector = np.expand_dims(
                    np.frombuffer(bvector, dtype=BigEndian[command.dtype].value), axis=0
                )
                user_vector = np_vector.astype(np.float64).tolist()

        elif protocol.lower() == "grpc":
            try:
                request_proto = EmbeddingUserRequest(**params)
                response = await stub.EmbeddingUser(request_proto)
                bvector = response.bvector
            except grpc.aio.AioRpcError as e:
                logging.error(f"gRPC Error: {e.code()} - {e.details()}")
                raise EmbeddingGrpcException(message=e.details())

            if return_binary:
                return GetUserEmbeddingResponse(
                    bvector=bvector,
                    user_vector=None,
                )

            np_vector = np.expand_dims(
                np.frombuffer(bvector, dtype=BigEndian[command.dtype].value), axis=0
            )
            user_vector = np_vector.astype(np.float64).tolist()

        return GetUserEmbeddingResponse(
            bvector=bvector,
            user_vector=user_vector,
        )


def get_personalization_service():
    return PersonalizationService(
        user_feature_repository=UserFeatureRepository(UserFeature),
        user_repository=UserRepository(),
    )
