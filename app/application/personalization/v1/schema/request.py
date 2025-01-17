from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domain.personalization.dto.feature import CreateUserFeatureDTO


class UserEmbeddingRequestDTO(BaseModel):
    size: int = Field(default=2048, description="Vector size : (1, size)")
    dtype: Literal["float16", "float32", "float64"] = Field(
        default="float16", description="Vector Data Type (float16, float32, float64)"
    )
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")
    favorite: str = Field(..., description="Favorite")
    lat: Optional[float] = Field(default=0, description="Lat")
    lng: Optional[float] = Field(default=0, description="Lng")

    model_config = ConfigDict(from_attributes=True)


class CreateUserFeatureRequest(CreateUserFeatureDTO):
    pass
