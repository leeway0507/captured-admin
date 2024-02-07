from .connection import conn_engine, get_secret, CustomDB, sshtunnelInstance
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

## ssh
tunnel = sshtunnelInstance()
tunnel.start()

sec = get_secret("production")
sec.update({"port": tunnel.local_bind_port})
db_engine = conn_engine(**sec)
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
