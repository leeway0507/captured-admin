from .connection import conn_engine, get_secret
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

db_engine = conn_engine(**get_secret("dev"))
session_local = sessionmaker(bind=db_engine, class_=AsyncSession)  # type: ignore


async def get_dev_db():
    db = session_local()
    try:
        yield db
    finally:
        await db.close()  # type: ignore


class AsyncDatabaseConnectionManager:
    def __init__(self):
        self.db_session = session_local()

    async def __aenter__(self):
        # Create and return an asynchronous database session for async with block
        return self.db_session

    async def __aexit__(self, exc_type, exc_value, traceback):
        # Close the asynchronous database session when exiting the context
        await self.db_session.close()  # type: ignore
