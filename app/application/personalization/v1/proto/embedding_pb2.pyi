from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EmbeddingUserRequest(_message.Message):
    __slots__ = ("dtype", "size", "email", "nickname", "favorite", "lat", "lng")
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LNG_FIELD_NUMBER: _ClassVar[int]
    dtype: str
    size: int
    email: str
    nickname: str
    favorite: str
    lat: float
    lng: float
    def __init__(self, dtype: _Optional[str] = ..., size: _Optional[int] = ..., email: _Optional[str] = ..., nickname: _Optional[str] = ..., favorite: _Optional[str] = ..., lat: _Optional[float] = ..., lng: _Optional[float] = ...) -> None: ...

class EmbeddingUserResponse(_message.Message):
    __slots__ = ("bvector",)
    BVECTOR_FIELD_NUMBER: _ClassVar[int]
    bvector: bytes
    def __init__(self, bvector: _Optional[bytes] = ...) -> None: ...
