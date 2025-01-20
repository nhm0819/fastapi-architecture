from fastapi import APIRouter, Depends, Query

from app.application.personalization.v1.schema.request import CreateUserFeatureRequest
from app.application.personalization.v1.schema.response import CreateUserFeatureResponse
from app.application.personalization.v1.service import get_personalization_service
from app.core.fastapi.dependencies import IsAuthenticated, IsOwnID, PermissionDependency
from app.domain.personalization.usecase.personalization import PersonalizationUseCase

personalization_router = APIRouter(prefix="/api/v1/personalization")


@personalization_router.get(
    "/user/{user_id}",
    response_model=CreateUserFeatureResponse,
    dependencies=[Depends(PermissionDependency([IsOwnID]))],
)
async def get_user_feature(
    user_id: int,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> CreateUserFeatureResponse:
    response_model = await usecase.get_user_feature(user_Id=user_id)
    return response_model


@personalization_router.post(
    "/user/{user_id}",
    response_model=CreateUserFeatureResponse,
    dependencies=[Depends(PermissionDependency([IsOwnID]))],
)
async def create_user_feature(
    user_id: int,
    # command: CreateUserFeatureRequest,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> CreateUserFeatureResponse:
    response_model = await usecase.get_user_feature(user_id=user_id)
    return response_model


@personalization_router.post(
    "/user/{user_id}/update",
    response_model=CreateUserFeatureResponse,
    dependencies=[Depends(PermissionDependency([IsOwnID]))],
)
async def update_user_feature(
    user_id: int,
    command: CreateUserFeatureRequest,
    usecase: PersonalizationUseCase = Depends(get_personalization_service),
) -> CreateUserFeatureResponse:
    response_model = await usecase.update_user_feature(command=command)
    return response_model
