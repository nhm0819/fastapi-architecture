import httpx
import numpy as np

from app.application.personalization.v1.exception import EmbeddingException
from app.application.personalization.v1.schema.request import UserEmbeddingRequestDTO
from app.application.personalization.v1.schema.response import UserEmbeddingResponseDTO
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


class PersonalizationService(PersonalizationUseCase):
    def __init__(
        self,
        user_feature_repository: UserFeatureRepository,
        user_service: UserService = get_user_service(),
    ):
        self.user_service = user_service
        self.user_feature_repository = user_feature_repository

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

        params = UserEmbeddingRequestDTO(
            size=size,
            dtype=dtype,
            email=user.email,
            nickname=user.nickname,
            favorite=user.favorite,
            lat=user.location.lat,
            lng=user.location.lng,
        ).model_dump()

        if protocol == "http":
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{config.EMBEDDING_URL}/v1/embedding/user/{user_id}",
                    json=params,
                )
                if resp.status_code != 200:
                    # TODO : custom exception
                    raise EmbeddingException(message=resp.text)
                embedding_result = UserEmbeddingResponseDTO.model_validate(resp.json())
                user_vector = embedding_result.user_vector
                bvector = np.array(user_vector, dtype=getattr(np, dtype)).tobytes()

        elif protocol == "http-octet":
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{config.EMBEDDING_URL}/v1/embedding/user/{user_id}/octet",
                    json=params,
                )
                if resp.status_code != 200:
                    # TODO : custom exception
                    raise "Embedding server error"
                bvector = resp.content
                np_vector = np.expand_dims(
                    np.frombuffer(bvector, dtype=np.float16), axis=0
                )
                user_vector = np_vector.astype(np.float64).tolist()

        else:
            # TODO : grpc embedding
            raise "Not yet grpc"

        is_exist = await self.user_feature_repository.get_feature_by_user_id(
            user_id=user_id,
        )
        user_feature = UserFeature.create(
            user_id=command.user_id,
            bvector=bvector,
        )
        await self.user_feature_repository.save(
            user_feature=user_feature,
        )
        # if is_exist:
        #     await self.user_feature_repository.update_by_id(
        #         id=is_exist.id,
        #         params={"bvector": bvector},
        #     )
        # else:
        #     user_feature = UserFeature.create(
        #         user_id=command.user_id,
        #         bvector=bvector,
        #     )
        #     await self.user_feature_repository.save(
        #         user_feature=user_feature,
        #     )

        return GetUserFeatureDTO(
            user_id=command.user_id,
            user_vector=user_vector,
        )


def get_personalization_service():
    return PersonalizationService(
        user_feature_repository=UserFeatureRepository(UserFeature),
        user_service=get_user_service(),
    )
