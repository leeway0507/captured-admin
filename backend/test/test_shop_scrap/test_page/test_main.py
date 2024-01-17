import os
import pytest
from shop_scrap.page.main import ShopPageMain
from db.dev_db import admin_session_local

current_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def ShopPage(test_session):
    yield ShopPageMain(current_path, test_session)


@pytest.mark.anyio
async def test_ShopPage(ShopPage: ShopPageMain):
    await ShopPage.execute("shop_product_card", "116", num_processor=1)
