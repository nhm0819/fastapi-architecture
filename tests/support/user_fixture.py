from app.domain.user.dto.vo import Location
from app.domain.user.entity.user import User


def make_user(
    id: int | None = None,
    password: str = "password",
    email: str = "hongmin@id.e",
    nickname: str = "hongma",
    favorite: str | None = None,
    is_admin: bool = False,
    lat: float | None = None,
    lng: float | None = None,
):
    return User(
        id=id,
        password=password,
        email=email,
        nickname=nickname,
        favorite=favorite,
        is_admin=is_admin,
        location=Location(lat=lat, lng=lng),
    )


users = {
    1: {
        "id": 1,
        "password": "password",
        "email": "hongmin@id.e",
        "nickname": "hongma",
        "favorite": "coding",
        "is_admin": True,
        "lat": 37.123,
        "lng": 127.123,
    },
    2: {
        "id": 2,
        "password": "password2",
        "email": "hongmin2@id.e",
        "nickname": "hongma2",
        "favorite": "drinking",
        "is_admin": False,
        "lat": None,
        "lng": None,
    },
}
