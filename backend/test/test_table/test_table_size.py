import pytest
from sqlalchemy import select
from db.dev_db import admin_session_local
from table.table_size import SizeTable
from collections import defaultdict


pytestmark = pytest.mark.asyncio(scope="module")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def Size():
    table = SizeTable()
    yield table


@pytest.mark.anyio
async def test_get_data(Size: SizeTable):
    raw_data = await Size.get_data(["db3021"])
    # print(raw_data)

    meta = Size.get_meta(raw_data)
    print(meta)

    # size_data = Size.size_data(meta, raw_data)
    # print(size_data)


@pytest.mark.anyio
async def test_get(Size: SizeTable):
    result = await Size.get("db3021")
    print(result)
