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


def remove_test_folder(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)


@pytest.fixture(scope="module")
async def scraper() -> AsyncGenerator:
    browser = await PwKreamBrowserController.start()
    sub_scraper = PwKreamPageSubScraper()
    scraper = PlatformPageScraper(path, 1, browser, sub_scraper, "kream")

    # necessary for test
    scraper.target_list = ["74749"]
    scraper.scrap_folder_name = "real_scrap_result"
    scraper.set_scrap_time()

    yield scraper


@pytest.mark.anyio
async def test_necessary_property(scraper: PlatformPageScraper):
    scraper.check_necessary_property()


@pytest.mark.anyio
async def test_is_login(scraper: PlatformPageScraper):
    await scraper.browser.login()

    assert await scraper.browser.is_login() == True


@pytest.mark.anyio
async def test_execute_sub_processor(scraper: PlatformPageScraper):
    temp_path = scraper.TempFile.path
    remove_test_folder(temp_path)

    await scraper.execute_sub_processors()

    assert os.path.exists(temp_path) == True


@pytest.mark.anyio
async def test_create_scrap_report(scraper: PlatformPageScraper):
    # Given
    report_path = scraper.Report.report_path
    remove_test_folder(report_path)

    await scraper.create_scrap_report()

    assert os.path.exists(report_path) == True


@pytest.mark.anyio
async def test_save_scrap_data(scraper: PlatformPageScraper):
    data_path = os.path.join(path, "real_scrap_result")
    remove_test_folder(data_path)

    await scraper.save_scrap_data()

    assert os.path.exists(data_path) == True


# @pytest.mark.anyio
# async def test_all_scrap(scraper: PlatformPageScraper):
#     await scraper.scrap()
