import pytest
from db.production_db import ProdDB, tunnel
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db.tables_production import ProductInfoTable
from sqlalchemy.ext.asyncio import AsyncSession


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_prod_db_connection():
    db = ProdDB()

    r = await db.execute(select(ProductInfoTable))
    print(r)

    tunnel.close()
