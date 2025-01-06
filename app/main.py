from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

import app.exceptions as exceptions


def init_routers(app_: FastAPI) -> None:
    pass


def init_listeners(app_: FastAPI) -> None:
    # add exception handlers
    app_.add_exception_handler(Exception, exceptions.exception_handler)
    app_.add_exception_handler(HTTPException, exceptions.http_exception_handler)
    app_.add_exception_handler(
        RequestValidationError, exceptions.validation_exception_handler
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
