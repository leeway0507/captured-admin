import os
import pytest
from shop_scrap.list.main import ShopListMain

current_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def ShopList():
    yield ShopListMain(current_path)


@pytest.mark.anyio
async def test_PlatformList(ShopList: ShopListMain):
    await ShopList.execute("consortium", target_list=["a.p.c."], num_processor=1)
