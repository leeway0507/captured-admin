from .connection import conn_engine, get_secret, CustomDB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

db_engine = conn_engine(**get_secret("production"))
prod_session_local = sessionmaker(bind=db_engine, class_=AsyncSession)  # type: ignore


async def get_production_db():
    db = prod_session_local()
    try:
        yield db
    finally:
        await db.close()  # type: ignore


class ProdDB(CustomDB):
    def __init__(self):
        super().__init__(prod_session_local)
