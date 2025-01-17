from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")


class CreateUserRequest(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    nickname: str = Field(..., description="Nickname")
    favorite: str = Field(default=None, description="Favorite")
    lat: Optional[float] = Field(default=None, description="Lat")
    lng: Optional[float] = Field(default=None, description="Lng")
