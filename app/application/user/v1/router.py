from fastapi import APIRouter, Depends, Query, Request

from app.application.user.v1.schema.request import CreateUserRequest, LoginRequest
from app.application.user.v1.schema.response import (
    CreateUserResponseDTO,
    GetUserResponseDTO,
    LoginResponse,
)
from app.application.user.v1.service import UserService, get_user_service
from app.core.fastapi.dependencies import IsAdmin, IsAuthenticated, PermissionDependency
from app.domain.user.dto.user import CreateUserDTO, GetUserListDTO
from app.domain.user.usecase.user import UserUseCase

user_router = APIRouter(prefix="/api/v1/user")


@user_router.get(
    "/list",
    response_model=list[GetUserListDTO],
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
    usecase: UserUseCase = Depends(get_user_service),
):
    return await usecase.get_user_list(limit=limit, prev=prev)


@user_router.get(
    "/me",
    response_model=GetUserResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_user_me(
    request: Request,
    usecase: UserUseCase = Depends(get_user_service),
):
    scope = request.scope
    user_id = scope["user"]["id"]
    user = await usecase.get_user(user_id=user_id)
    return GetUserResponseDTO.model_validate(user)


# @user_router.get(
#     "/{user_id}",
#     response_model=GetUserResponseDTO,
#     dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
# )
# async def get_user(
#     user_id: int,
#     usecase: UserUseCase = Depends(get_user_service),
# ):
#     user = await usecase.get_user(user_id=user_id)
#     return GetUserResponseDTO.model_validate(user)


@user_router.post(
    "",
    response_model=CreateUserResponseDTO,
)
async def create_user(
    request: CreateUserRequest,
    usecase: UserUseCase = Depends(get_user_service),
):
    command = CreateUserDTO(**request.model_dump())
    await usecase.create_user(command=command)
    return {"email": request.email, "nickname": request.nickname}


@user_router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
    usecase: UserUseCase = Depends(get_user_service),
):
    login_response = await usecase.login(email=request.email, password=request.password)
    return {
        "access_token": login_response.access_token,
        "refresh_token": login_response.refresh_token,
    }
