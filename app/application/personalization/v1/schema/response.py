from typing import List, Optional

import numpy as np
from pydantic import BaseModel, Field


class UserEmbeddingResponseDTO(BaseModel):
    user_vector: List[List[float]] = Field(..., description="Vector[n, dims]")


class GetUserEmbeddingResponseDTO(UserEmbeddingResponseDTO):
    bvector: bytes = Field(..., description="bytes vector")
    # np_vector: Optional[np.array] = Field(default=None, description="numpy vector")


class CreateUserFeatureResponse(BaseModel):
    user_id: int = Field(..., description="User ID")
    user_vector: List[List[float]] = Field(default=None, description="Vector[n, dims]")
