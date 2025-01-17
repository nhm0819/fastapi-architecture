from pydantic import BaseModel, Field


class RefreshTokenDTO(BaseModel):
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh token")
