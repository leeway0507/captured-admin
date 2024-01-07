import os
import pytest

from platform_scrap.page.data_save import PlatformPageDataSave

from platform_scrap.page.platform_page_data_converter import (
    PlatformPageDataConverter,
    PlatformPageStrategyFactory as fac,
)

current_path = __file__.rsplit("/", 1)[0]

folder_name = "adidas"

scrap_time = "scrap_time"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def DataSave():
    data_save = PlatformPageDataSave(current_path)
    data_save.folder_name = folder_name
    yield data_save


@pytest.mark.anyio
async def test_init_config(DataSave: PlatformPageDataSave):
    await DataSave.init_config()
    assert DataSave.platform_type == "kream"


@pytest.fixture(scope="session")
def DataConverter():
    yield PlatformPageDataConverter(current_path, folder_name, scrap_time)


@pytest.mark.anyio
async def test_product_detail(DataConverter: PlatformPageDataConverter):
    DataConverter.strategy = fac.product_detail()

    data = await DataConverter.load_temp_file_data()

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_product_bridge(DataConverter: PlatformPageDataConverter):
    DataConverter.strategy = fac.product_bridge()

    data = await DataConverter.load_temp_file_data()

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_buy_and_sell(DataConverter: PlatformPageDataConverter):
    DataConverter.strategy = fac.buy_and_sell()

    data = await DataConverter.load_temp_file_data()

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_trading_volume(DataConverter: PlatformPageDataConverter):
    DataConverter.strategy = fac.trading_volume()

    data = await DataConverter.load_temp_file_data()

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_save_data(DataSave: PlatformPageDataSave):
    await DataSave.save_scrap_data()
