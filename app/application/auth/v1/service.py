from app.application.auth.v1.schema.response import RefreshTokenResponseDTO
from app.core.helpers.token import (
    DecodeTokenException,
    ExpiredTokenException,
    TokenHelper,
)
from app.domain.auth.usecase.jwt import JwtUseCase


class JwtService(JwtUseCase):
    async def verify_token(self, token: str) -> None:
        try:
            TokenHelper.decode(token=token)
        except:
            raise

    async def create_refresh_token(
        self,
        access_token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        decoded_created_token = TokenHelper.decode(token=access_token)
        decoded_refresh_token = TokenHelper.decode(token=refresh_token)
        if decoded_refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        return RefreshTokenResponseDTO(
            access_token=TokenHelper.encode(
                payload={"user_id": decoded_created_token.get("user_id")}
            ),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )


def get_jwt_service():
    return JwtService()
