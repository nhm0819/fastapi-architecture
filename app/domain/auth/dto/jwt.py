from pydantic import BaseModel, Field


class RefreshTokenDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
