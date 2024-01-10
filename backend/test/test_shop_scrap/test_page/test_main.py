import os
import pytest
from shop_scrap.page.main import ShopPageMain

current_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def ShopPage():
    yield ShopPageMain(current_path)


@pytest.mark.anyio
async def test_ShopPage(ShopPage: ShopPageMain):
    await ShopPage.execute("shop_product_card", "116", num_processor=1)
