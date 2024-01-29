from typing import AsyncGenerator, List
import os
import json
from datetime import date, timedelta
import shutil
import pytest

from components.dev.platform.platform_browser_controller import (
    PwKreamBrowserController,
)
from components.dev.platform.page import PlatformPageScraper
from components.dev.platform.page.sub_scraper import PwKreamPageSubScraper

path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/page/"
scrap_result_path = os.path.join(path, "test_scrap_result.json")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def mock_scraper() -> AsyncGenerator:
    browser = await PwKreamBrowserController.start()
    sub_scraper = PwKreamPageSubScraper()
    scraper = PlatformPageScraper(path, 1, browser, sub_scraper, "kream")
    yield scraper


@pytest.fixture(scope="module")
async def scrap_result():
    with open(scrap_result_path, "r") as f:
        data = json.load(f)
    yield data


@pytest.mark.anyio
async def test_save_data_to_temp(mock_scraper: PlatformPageScraper, scrap_result):
    # Given
    shutil.rmtree(os.path.join(path, "_temp"))

    # When
    data = scrap_result["data"]
    await mock_scraper.save_data_to_temp(data)

    # Then
    assert os.path.exists(os.path.join(path, "_temp"))


@pytest.mark.anyio
async def test_handle_scrap_error(mock_scraper: PlatformPageScraper):
    err_status = "Test Exception Error"
    err = await mock_scraper.handle_scrap_error("test", Exception(err_status))
    assert err == f"failed: {err_status}"


def test_set_scrap_status_temp_template(
    mock_scraper: PlatformPageScraper, scrap_result
):
    template = mock_scraper.set_scrap_status_temp_template(
        "test", scrap_result["status"]
    )
    assert template.model_dump() == {
        "job": "test",
        "status": scrap_result["status"],
    }


@pytest.mark.anyio
async def test_save_scrap_status_to_temp(
    mock_scraper: PlatformPageScraper, scrap_result
):
    for i in range(1, 6):
        template = mock_scraper.set_scrap_status_temp_template(
            str(i), scrap_result["status"]
        )
        await mock_scraper.save_scrap_status_to_temp(template)

    assert os.path.exists(os.path.join(path, "_temp", "scrap_status.json"))


@pytest.mark.anyio
async def test_get_params_list(mock_scraper: PlatformPageScraper):
    temp_scrap_status = await mock_scraper.TempFile.load_temp_file("scrap_status")

    params_list = mock_scraper._get_params_list(temp_scrap_status)

    assert params_list == ["1", "2", "3", "4", "5"]


@pytest.mark.anyio
async def test_get_product_detail_list(mock_scraper: PlatformPageScraper):
    temp_scrap_status = await mock_scraper.TempFile.load_temp_file("scrap_status")

    product_detail = mock_scraper._get_product_detail(temp_scrap_status)

    assert product_detail == ["success", "success", "success", "success", "success"]


@pytest.mark.anyio
async def test_get_trading_volume_list(mock_scraper: PlatformPageScraper):
    temp_scrap_status = await mock_scraper.TempFile.load_temp_file("scrap_status")

    trading_volume = mock_scraper._get_trading_volume(temp_scrap_status)

    assert trading_volume == ["success", "success", "success", "success", "success"]


@pytest.mark.anyio
async def test_get_buy_and_sell_list(mock_scraper: PlatformPageScraper):
    temp_scrap_status = await mock_scraper.TempFile.load_temp_file("scrap_status")

    buy_and_sell = mock_scraper._get_buy_and_sell(temp_scrap_status)

    assert buy_and_sell == ["success", "success", "success", "success", "success"]


@pytest.mark.anyio
async def test_create_report_template(mock_scraper: PlatformPageScraper):
    temp_scrap_status = await mock_scraper.TempFile.load_temp_file("scrap_status")
    mock_scraper.set_scrap_time()

    report_template = mock_scraper.create_report_template(temp_scrap_status)

    assert report_template.model_dump() == {
        "scrap_time": mock_scraper.scrap_time,
        "num_of_plan": 5,
        "num_processor": 1,
        "job": ["1", "2", "3", "4", "5"],
        "product_detail": ["success", "success", "success", "success", "success"],
        "trading_volume": ["success", "success", "success", "success", "success"],
        "buy_and_sell": ["success", "success", "success", "success", "success"],
        "platform_type": "kream",
        "db_update": False,
    }


@pytest.mark.anyio
async def test_create_scrap_report(mock_scraper: PlatformPageScraper):
    # Given
    mock_scraper.set_scrap_time()

    # When
    await mock_scraper.create_scrap_report()

    # Then
    assert os.path.exists(os.path.join(path, "_report"))