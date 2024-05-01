"""db connection"""

from typing import Dict

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine
from sshtunnel import SSHTunnelForwarder

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db.tables_production import ProductInfoTable
from sqlalchemy.ext.asyncio import AsyncSession

from components.env import dev_env, prod_env


def conn_engine(
    username: str, password: str, host: str, db_name: str, port: str, **_kwargs
):
    db_url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{db_name}"
    return create_async_engine(db_url)


def sshtunnelInstance():
    # SSH config
    ssh_host = "43.201.98.25"
    ssh_username = "ubuntu"
    ssh_private_key = "/Users/yangwoolee/.ssh/captured.pem"
    db_host = "db-captured.cheoqn0aa7xs.ap-northeast-2.rds.amazonaws.com"

    tunnel = SSHTunnelForwarder(
        ssh_host,
        ssh_username=ssh_username,
        ssh_pkey=ssh_private_key,
        remote_bind_address=(db_host, 3306),
    )
    return tunnel


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


class CustomDB:
    def __init__(self, session: sessionmaker):
        self.session = session

    async def execute_and_commit(self, stmt):
        async with self.session() as db:  # type:ignore
            await db.execute(stmt)
            await db.commit()

    async def execute(self, stmt):
        async with self.session() as db:  # type:ignore
            data = await db.execute(stmt)
        return data.all()
