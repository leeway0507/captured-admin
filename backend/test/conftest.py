import os
import sys
from os.path import dirname, abspath

import pytest

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


root_dir = dirname(dirname(abspath(__file__)))

sys.path.append(root_dir)

# default Root
os.chdir(root_dir)


def conn_engine(username: str, password: str, host: str, db_name: str, **_kwargs):
    db_url = f"mysql+aiomysql://{username}:{password}@{host}:3306/{db_name}"
    return create_async_engine(db_url)


# Fixture to create and configure a test database engine (session-scoped)
@pytest.fixture(scope="session")
def test_engine():
    db_engine = conn_engine(
        username="root", password="", host="localhost", db_name="captured_test"
    )
    yield db_engine


# Fixture to create a session for the test database
@pytest.fixture(scope="module")
async def test_session(test_engine: AsyncEngine):
    session = sessionmaker(bind=test_engine, class_=AsyncSession)  # type: ignore
    yield session
