from app.domain.user.dto.vo import Location
from app.domain.user.entity.user import User


def make_user(
    id: int | None = None,
    password: str = "password",
    email: str = "hongmin@id.e",
    nickname: str = "hongma",
    is_admin: bool = False,
    lat: float | None = None,
    lng: float | None = None,
):
    return User(
        id=id,
        password=password,
        email=email,
        nickname=nickname,
        is_admin=is_admin,
        location=Location(lat=lat, lng=lng),
    )
