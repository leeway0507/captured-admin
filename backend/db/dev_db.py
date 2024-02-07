from .connection import conn_engine, get_secret, CustomDB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from components.env import dev_env

db_engine = conn_engine(**get_secret("dev"), port="3306")

# admin table
admin_session_local = sessionmaker(bind=db_engine, class_=AsyncSession)  # type: ignore

# dev table
dev_session_local = sessionmaker(
    bind=conn_engine(
        dev_env.DB_USER_NAME,
        dev_env.DB_PASSWORD,
        dev_env.DB_HOST,
        dev_env.DEV_DB_NAME,
        "3306",
    ),
    class_=AsyncSession,  # type: ignore
)


async def get_dev_db():
    db = admin_session_local()
    try:
        yield db
    finally:
        await db.close()  # type: ignore


class AdminDB(CustomDB):
    def __init__(self):
        super().__init__(admin_session_local)


class DevDB(CustomDB):
    def __init__(self):
        super().__init__(dev_session_local)
