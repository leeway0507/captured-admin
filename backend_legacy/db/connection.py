"""db connection"""

from typing import Dict, Callable, Optional

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from env import dev_env, prod_env

from logging import Logger


def connect_db(
    username: str, password: str, host: str, db_name: str, **_kwargs
) -> Session:
    """
    sseion 연결

    Args:
        username (str): db username
        password (str): db password
        host (str): db host
        db_name (str): db name

    Returns:
        sessionmaker : 연결된 db ssesion

    """

    ###############
    # DB Session using Sqlalchemy.orm

    engine = conn_engine(username, password, host, db_name)
    session_local = sessionmaker(bind=engine)
    return session_local()


def conn_engine(username: str, password: str, host: str, db_name: str, **_kwargs):
    db_url = f"mysql+aiomysql://{username}:{password}@{host}:3306/{db_name}"
    return create_async_engine(db_url)


def get_secret(env: str) -> Dict[str, str]:
    if env == "production":
        config = prod_env  # type: ignore
    else:
        config = dev_env  # type: ignore

    return {
        "username": config.DB_USER_NAME,
        "password": config.DB_PASSWORD,
        "host": config.DB_HOST,
        "db_name": config.DB_NAME,
    }


async def commit(db: AsyncSession, query: Callable, error_log: Optional[Logger] = None):
    try:
        query
        await db.commit()
        return True
    except Exception as e:
        if error_log:
            error_log.error(e)
        else:
            print(e)
        await db.rollback()
        print("커밋 실패 후 rollback")
        return False
