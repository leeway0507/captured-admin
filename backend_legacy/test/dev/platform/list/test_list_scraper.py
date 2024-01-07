from typing import AsyncGenerator, List
import os
import shutil
import pytest
from datetime import datetime

from playwright.async_api import async_playwright
from bs4 import Tag, BeautifulSoup
from components.dev.utils.browser_controller import PwPageController
from components.dev.platform.platform_browser_controller import (
    PwKreamBrowserController,
)
from components.dev.platform.list import PlatformListScraper, PlatformScrapStatus
from components.dev.platform.list.sub_scraper import (
    PwKreamListSubScraper,
)

path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/list"
test_min_volume = 50
test_min_wish = 50
test_brand_name = "the north face"


def remove_test_folder(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def scraper() -> AsyncGenerator:
    browser = await PwKreamBrowserController.start()
    sub_scraper = PwKreamListSubScraper()
    scraper = PlatformListScraper(
        path,
        1,
        browser,
        sub_scraper,
        "kream",
        test_min_volume,
        test_min_wish,
    )
    # necessary for test
    scraper.target_list = [test_brand_name]
    scraper.scrap_folder_name = "real_scrap_result"
    scraper.set_scrap_time()

    yield scraper


@pytest.mark.anyio
async def test(scraper: PlatformListScraper):
    scraper.check_necessary_property()


@pytest.mark.anyio
async def test_kream_login(scraper: PlatformListScraper):
    await scraper.browser_login()
    assert scraper.browser.is_login


@pytest.mark.anyio
async def test_execute_sub_processor(scraper: PlatformListScraper):
    temp_path = scraper.TempFile.path
    remove_test_folder(temp_path)

    await scraper.execute_sub_processors()

    assert os.path.exists(temp_path) == True


@pytest.mark.anyio
async def test_create_scrap_report(scraper: PlatformListScraper):
    # Given
    report_path = scraper.Report.report_path
    remove_test_folder(report_path)

    await scraper.create_scrap_report()

    assert os.path.exists(report_path) == True


@pytest.mark.anyio
async def test_save_scrap_data(scraper: PlatformListScraper):
    # Given
    data_path = os.path.join(path, scraper.platform_type, "real_scrap_result")
    remove_test_folder(data_path)

    await scraper.save_scrap_data()

    assert os.path.exists(data_path) == True
