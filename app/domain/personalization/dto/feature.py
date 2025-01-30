from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateUserFeatureDTO(BaseModel):
    protocol: Literal["http", "http-octet", "grpc"] = Field(
        default="http", description="http, http-octet or grpc"
    )
    size: int = Field(default=2048, description="Vector size : (1, size)")
    dtype: Literal["float16", "float32", "float64"] = Field(
        default="float16", description="Vector Data Type (float16, float32, float64)"
    )


class GetUserFeatureDTO(BaseModel):
    user_vector: List[List[float]] = Field(default=None, description="Vector[n, dims]")
    size: int = Field(default=2048, description="Vector size : (1, size)")
    dtype: Literal["float16", "float32", "float64"] = Field(
        default="float16", description="Vector Data Type (float16, float32, float64)"
    )


class DeleteUserFeatureDTO(BaseModel):
    id: int = Field(..., description="User Feature ID")
    user_id: int = Field(..., description="User ID")
    size: int = Field(default=2048, description="Vector size : (1, size)")
    dtype: Literal["float16", "float32", "float64"] = Field(
        default="float16", description="Vector Data Type (float16, float32, float64)"
    )
