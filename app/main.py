from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

import app.core.exceptions as exceptions
from app.application.auth.v1.router import auth_router
from app.application.user.v1.router import user_router
from app.core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    SQLAlchemyMiddleware,
)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(user_router)
    app_.include_router(auth_router)


def init_listeners(app_: FastAPI) -> None:
    # add exception handlers
    app_.add_exception_handler(Exception, exceptions.exception_handler)
    app_.add_exception_handler(HTTPException, exceptions.http_exception_handler)
    app_.add_exception_handler(
        RequestValidationError, exceptions.validation_exception_handler
    )
    app_.add_exception_handler(
        exceptions.CustomException, exceptions.custom_exception_handler
    )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, Exception):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="FastAPI Architecture",
        description="FastAPI Architecture",
        version="0.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()


@app.get("/", response_class=JSONResponse)
async def root():
    """ping"""
    return {"status": "healthy"}
