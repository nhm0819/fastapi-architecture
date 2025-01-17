from app.application.auth.v1.router import auth_router as auth_router_v1
from app.application.personalization.v1.router import (
    personalization_router as personalization_router_v1,
)
from app.application.user.v1.router import user_router as user_router_v1

__all__ = [
    "user_router_v1",
    "auth_router_v1",
    "personalization_router_v1",
]
