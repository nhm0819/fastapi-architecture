from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

import app.core.exceptions as exceptions
from app.application import auth_router_v1, personalization_router_v1, user_router_v1
from app.application.personalization.v1.proto.client import get_embedding_channel_stub
from app.core.configs import config
from app.core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    PyInstrumentMiddleWare,
    SQLAlchemyMiddleware,
)
from app.core.helpers.cache import Cache, CustomKeyMaker, RedisBackend
from app.core.helpers.cache.base import BaseBackend, BaseKeyMaker


def init_routers(app_: FastAPI) -> None:
    app_.include_router(user_router_v1, tags=["user"])
    app_.include_router(auth_router_v1, tags=["auth"])
    app_.include_router(personalization_router_v1, tags=["personalization"])


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


def init_cache(backend: BaseBackend, key_maker: BaseKeyMaker) -> None:
    Cache.init(backend=backend, key_maker=key_maker)


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
    if config.PROFILING:
        middleware.insert(
            0,
            Middleware(
                PyInstrumentMiddleWare,
            ),
        )
    return middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔗 Opening gRPC channel...")
    embedding_channel, embedding_stub = get_embedding_channel_stub()

    # grpc channel, stub 저장
    app.state.embedding_channel = embedding_channel
    app.state.embedding_stub = embedding_stub

    yield

    print("🔌 Closing gRPC channel...")
    await embedding_channel.close()


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="FastAPI Architecture",
        description="FastAPI Architecture",
        version="0.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        middleware=make_middleware(),
    )

    # routers
    init_routers(app_=app_)

    # listeners
    init_listeners(app_=app_)

    # init cache server (redis)
    init_cache(backend=RedisBackend(), key_maker=CustomKeyMaker())

    return app_


app = create_app()


@app.get("/", response_class=JSONResponse)
async def root():
    """ping"""
    return {"status": "healthy"}
