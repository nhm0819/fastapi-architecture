from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh token")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class GetUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")
    favorite: str | None = Field(default=None, description="Favorite")
    lat: Optional[float] = Field(default=None, description="Lat")
    lng: Optional[float] = Field(default=None, description="Lng")

    model_config = ConfigDict(from_attributes=True)
