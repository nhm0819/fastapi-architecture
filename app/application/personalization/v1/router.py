from fastapi import APIRouter, Depends, Query, Request

from app.application.personalization.v1.schema.request import (
    CreateUserFeatureRequest,
    UpdateUserFeatureRequest,
)
from app.application.personalization.v1.schema.response import (
    GetUserFeatureResponse,
    UserEmbeddingResponse,
)
from app.application.personalization.v1.service import get_personalization_service
from app.core.dto import OctetStreamResponse
from app.core.fastapi.dependencies import IsAdmin, IsAuthenticated, PermissionDependency
from app.domain.personalization.usecase.personalization import PersonalizationUseCase

personalization_router = APIRouter(prefix="/api/v1/personalization")


@personalization_router.get(
    "/user",
    response_model=GetUserFeatureResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_user_feature(
    request: Request,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> GetUserFeatureResponse:
    user_id = request.scope["user"].id
    response_model = await usecase.get_user_feature(user_id=user_id)
    return response_model


@personalization_router.get(
    "/user/octet",
    response_class=OctetStreamResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_user_feature_binary(
    request: Request,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> UserEmbeddingResponse:
    scope = request.scope
    current_user = scope["user"]
    user_id = current_user.id

    bvector = await usecase.get_user_feature_binary(user_id=user_id)
    return OctetStreamResponse(content=bvector)


@personalization_router.post(
    "/user",
    response_model=UserEmbeddingResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def create_user_feature(
    request: Request,
    command: CreateUserFeatureRequest,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> UserEmbeddingResponse:
    scope = request.scope
    current_user = scope["user"]
    user_id = current_user.id
    response_model = await usecase.create_user_feature(
        user_id=user_id,
        command=command,
    )
    return response_model


@personalization_router.patch(
    "/user",
    response_model=UserEmbeddingResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def update_user_feature(
    request: Request,
    command: UpdateUserFeatureRequest,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> UserEmbeddingResponse:
    scope = request.scope
    current_user = scope["user"]
    user_id = current_user.id
    response_model = await usecase.update_user_feature(
        user_id=user_id,
        command=command,
    )
    return response_model


@personalization_router.delete(
    "/user/{user_id}",
    response_model=UserEmbeddingResponse,
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def delete_user_feature(
    user_id: int,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> UserEmbeddingResponse:
    response_model = await usecase.delete_user_feature(user_id=user_id)
    return response_model
