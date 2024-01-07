import os
import pytest

from shop_scrap.list.data_save import ShopListDataSave

current_path = __file__.rsplit("/", 1)[0]

report_path = os.path.join(current_path, "_report")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def DataSave():
    yield ShopListDataSave(current_path)


@pytest.mark.anyio
async def test_init_config(DataSave: ShopListDataSave):
    await DataSave.init_config()

    assert DataSave.shop_name == "consortium"


@pytest.mark.anyio
async def test_save_data(DataSave: ShopListDataSave):
    await DataSave.save_scrap_data()
