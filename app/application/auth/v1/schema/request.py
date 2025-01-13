from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class VerifyTokenRequest(BaseModel):
    token: str = Field(..., description="Token")
