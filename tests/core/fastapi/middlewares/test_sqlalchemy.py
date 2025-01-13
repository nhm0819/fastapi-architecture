from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_scoped_session
from starlette.types import Receive, Scope, Send

from app.core.fastapi.middlewares import SQLAlchemyMiddleware, sqlalchemy


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    await receive()
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"Content-Type", b"application/json")],
        },
    )
    await send({"type": "http.response.body", "body": b"test"})


async def exception_app(scope: Scope, receive: Receive, send: Send) -> None:
    await receive()
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"Content-Type", b"application/json")],
        },
    )
    await send({"type": "http.response.body", "body": b"test"})
    raise Exception


@pytest.mark.asyncio
@patch.object(sqlalchemy, "session", spec=async_scoped_session)
async def test_sqlalchemy_middleware(session_mock):
    # Given
    test_app = SQLAlchemyMiddleware(app=app)

    # When, Then
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://127.0.0.1"
    ) as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert session_mock.remove.called


@pytest.mark.asyncio
@patch.object(sqlalchemy, "session", spec=async_scoped_session)
async def test_sqlalchemy_middleware_exception(session_mock):
    # Given
    test_app = SQLAlchemyMiddleware(app=exception_app)

    # When, Then
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://127.0.0.1"
    ) as client:
        with pytest.raises(Exception):
            response = await client.get("/")
            assert response.status_code == 200
            assert session_mock.remove.called
