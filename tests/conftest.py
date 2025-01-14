import asyncio
from uuid import uuid4

import pytest
import pytest_asyncio

from app.core.db.session import reset_session_context
from app.core.db.session import session as db_session
from app.core.db.session import set_session_context
from tests.support.test_db_coordinator import TestDbCoordinator

test_db_coordinator = TestDbCoordinator()


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (
        item for item in items if pytest_asyncio.is_async_test(item)
    )
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="function", autouse=True)
def session_context():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    yield
    reset_session_context(context=context)


@pytest_asyncio.fixture
async def session():
    test_db_coordinator.apply_alembic()
    yield db_session
    await db_session.remove()
    test_db_coordinator.truncate_all()
