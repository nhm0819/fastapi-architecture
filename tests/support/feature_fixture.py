import numpy as np

from app.domain.personalization.entity.feature import UserFeature


def make_user_feature(
    id: int | None = None,
    user_id: int | None = None,
    bvector: bytes | None = None,
):
    return UserFeature(id=id, user_id=user_id, bvector=bvector)


user_features = {
    1: {
        "id": 1,
        "user_id": 1,
        "bvector": np.random.normal(0, 1, (1, 2048)).astype(np.float16).tobytes(),
    }
}
