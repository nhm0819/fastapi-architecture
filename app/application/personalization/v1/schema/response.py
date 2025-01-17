from typing import List

from pydantic import BaseModel, Field


class UserEmbeddingResponseDTO(BaseModel):
    user_vector: List[List[float]] = Field(..., description="Vector[n, dims]")


class CreateUserFeatureResponse(UserEmbeddingResponseDTO):
    user_id: int = Field(..., description="User ID")
    user_vector: List[List[float]] = Field(default=None, description="Vector[n, dims]")
