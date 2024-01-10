import os
import pytest

from shop_scrap.page.data_save import ShopPageDataSave

current_path = __file__.rsplit("/", 1)[0]

report_path = os.path.join(current_path, "_report")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def DataSave():
    yield ShopPageDataSave(current_path)


@pytest.mark.anyio
async def test_init_config(DataSave: ShopPageDataSave):
    await DataSave.init_config()

    assert DataSave.scrap_time


@pytest.mark.anyio
async def test_save_data(DataSave: ShopPageDataSave):
    await DataSave.save_scrap_data()
