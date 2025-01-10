from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from app.application.auth.v1.schema.request import (
    RefreshTokenRequest,
    VerifyTokenRequest,
)
from app.application.auth.v1.schema.response import RefreshTokenResponseDTO
from app.application.auth.v1.service import JwtService, get_jwt_service
from app.domain.auth.dto.jwt import RefreshTokenDTO
from app.domain.auth.usecase.jwt import JwtUseCase

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponseDTO,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    usecase: JwtUseCase = Depends(get_jwt_service),
):
    token = await usecase.create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post("/verify")
@inject
async def verify_token(
    request: VerifyTokenRequest,
    usecase: JwtUseCase = Depends(get_jwt_service),
):
    await usecase.verify_token(token=request.token)
    return Response(status_code=200)
