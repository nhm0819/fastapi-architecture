import numpy as np

from app.application.personalization.v1.enums import BigEndian
from app.domain.personalization.entity.feature import UserFeature


def make_user_feature(
    id: int | None = None,
    user_id: int | None = None,
    bvector: bytes | None = None,
    size: int | None = None,
    dtype: str | None = None,
):
    return UserFeature(id=id, user_id=user_id, bvector=bvector, size=size, dtype=dtype)


dtype = "float16"
size = 2048

user_features = {
    1: {
        "id": 1,
        "user_id": 1,
        "bvector": np.random.standard_normal((1, size))
        .astype(BigEndian[dtype].value)
        .tobytes(),
        "size": 2048,
        "dtype": dtype,
    },
    2: {
        "id": 2,
        "user_id": 2,
        "bvector": np.random.standard_normal((1, size))
        .astype(BigEndian[dtype].value)
        .tobytes(),
        "size": 2048,
        "dtype": dtype,
    },
}
