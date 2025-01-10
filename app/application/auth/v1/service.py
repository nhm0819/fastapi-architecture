from app.application.auth.v1.exception import DecodeTokenException
from app.application.auth.v1.schema.response import RefreshTokenResponseDTO
from app.core.helpers.token import DecodeTokenException as JwtDecodeTokenException
from app.core.helpers.token import ExpiredTokenException as JwtExpiredTokenException
from app.core.helpers.token import TokenHelper
from app.domain.auth.usecase.jwt import JwtUseCase


class JwtService(JwtUseCase):
    async def verify_token(self, token: str) -> None:
        try:
            TokenHelper.decode(token=token)
        except (JwtDecodeTokenException, JwtExpiredTokenException):
            raise DecodeTokenException

    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        decoede_created_token = TokenHelper.decode(token=token)
        decoded_refresh_token = TokenHelper.decode(token=refresh_token)
        if decoded_refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        return RefreshTokenResponseDTO(
            token=TokenHelper.encode(
                payload={"user_id": decoede_created_token.get("user_id")}
            ),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )


async def get_jwt_service():
    return JwtService()
