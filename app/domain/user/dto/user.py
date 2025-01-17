from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="USER ID")
    email: str = Field(..., title="Email")
    nickname: str = Field(..., title="Nickname")


class GetUserListDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class CreateUserDTO(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    nickname: str = Field(..., description="Nickname")
    favorite: str = Field(default=None, description="Favorite")
    lat: Optional[float] = Field(default=None, description="Lat")
    lng: Optional[float] = Field(default=None, description="Lng")

    model_config = ConfigDict(from_attributes=True)
