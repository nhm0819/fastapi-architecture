import asyncio
from uuid import uuid4

import pytest
import pytest_asyncio

from app.core.db.session import reset_session_context
from app.core.db.session import session as db_session
from app.core.db.session import set_session_context
from tests.support.test_db_coordinator import TestDbCoordinator

test_db_coordinator = TestDbCoordinator()


import os
from pathlib import Path

import pytest
from pyinstrument import Profiler


@pytest.fixture(autouse=True)
def auto_profile(request):
    ROOT = Path(os.path.dirname(__file__)).parent
    PROFILE_ROOT = ROOT.joinpath("profiling")
    # Turn profiling on
    profiler = Profiler()
    profiler.start()

    yield  # Run test

    profiler.stop()
    PROFILE_ROOT.mkdir(exist_ok=True)
    results_file = PROFILE_ROOT / f"{request.node.name}.html"
    profiler.write_html(results_file)


# def pytest_collection_modifyitems(items):
#     pytest_asyncio_tests = (
#         item for item in items if pytest_asyncio.is_async_test(item)
#     )
#     session_scope_marker = pytest.mark.asyncio(loop_scope="session")
#     for async_test in pytest_asyncio_tests:
#         async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="function", autouse=True)
def session_context():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    yield
    reset_session_context(context=context)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session():
    test_db_coordinator.apply_alembic()
    yield db_session
    await db_session.remove()
    test_db_coordinator.truncate_all()
