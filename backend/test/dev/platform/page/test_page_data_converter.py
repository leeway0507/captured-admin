import os

import pytest

from components.dev.platform.page.platform_page_data_converter import (
    PlatformPageDataConverter,
    PlatformPageStrategyFactory as fac,
)

from components.dev.utils.file_manager import ScrapTempFile


path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/page/"
file_name = "test"
brand_name = "adidas"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def data_converter():
    return PlatformPageDataConverter(path, brand_name, file_name)


@pytest.mark.anyio
async def test_load_temp_product_detail(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.product_detail()

    # When
    data = await data_converter.load_temp_file_data()

    # Then
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_load_temp_trading_volume(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.trading_volume()

    # When
    data = await data_converter.load_temp_file_data()

    # Then
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_load_temp_buy_and_sell(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.buy_and_sell()

    # When
    data = await data_converter.load_temp_file_data()

    # Then
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_product_detail_strategy(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.product_detail()
    data = await data_converter.load_temp_file_data()

    # When
    df = data_converter.strategy.preprocess(data)


def test_create_folder(data_converter: PlatformPageDataConverter):
    page_path = os.path.join(path, brand_name)
    data_converter.TempFile.create_folder(page_path)

    assert os.path.exists(page_path)


@pytest.mark.anyio
async def test_save_product_detail(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.product_detail()
    await data_converter.save_data()

    file_path = os.path.join(path, brand_name, "test-product_detail.parquet.gzip")
    assert os.path.exists(file_path)


@pytest.mark.anyio
async def test_save_product_bridge(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.product_bridge()
    await data_converter.save_data()

    file_path = os.path.join(path, brand_name, "test-product_bridge.parquet.gzip")
    assert os.path.exists(file_path)


@pytest.mark.anyio
async def test_save_trading_volume(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.trading_volume()
    await data_converter.save_data()

    file_path = os.path.join(path, brand_name, "test-trading_volume.parquet.gzip")
    assert os.path.exists(file_path)


@pytest.mark.anyio
async def test_save_buy_and_sell(data_converter: PlatformPageDataConverter):
    # Given
    data_converter.strategy = fac.buy_and_sell()
    await data_converter.save_data()

    file_path = os.path.join(path, brand_name, "test-buy_and_sell.parquet.gzip")
    assert os.path.exists(file_path)
