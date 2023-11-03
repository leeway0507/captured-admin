from .connection import conn_engine,get_secret
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