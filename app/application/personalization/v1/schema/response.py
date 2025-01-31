from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class UserEmbeddingResponse(BaseModel):
    user_vector: List[List[float]] = Field(..., description="Vector[n, dims]")


class GetUserEmbeddingResponse(UserEmbeddingResponse):
    user_vector: Optional[List[List[float]]] = Field(..., description="Vector[n, dims]")
    bvector: bytes = Field(..., description="bytes vector")


class GetUserFeatureResponse(BaseModel):
    size: int = Field(default=2048, description="Vector size : (1, size)")
    dtype: Literal["float16", "float32", "float64"] = Field(
        default="float16", description="Vector Data Type (float16, float32, float64)"
    )
    user_vector: List[List[float]] = Field(default=None, description="Vector[n, dims]")


class GetUserFeatureBinaryResponse(BaseModel):
    bvector: bytes = Field(..., description="bytes vector")


class DeleteUserFeatureResponse(BaseModel):
    id: int = Field(..., description="User Feature ID")
    user_id: int = Field(..., description="User ID")
    size: int = Field(default=2048, description="Vector size : (1, size)")
    dtype: Literal["float16", "float32", "float64"] = Field(
        default="float16", description="Vector Data Type (float16, float32, float64)"
    )
