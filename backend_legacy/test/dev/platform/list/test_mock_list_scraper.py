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
    KreamScrapingBrandSchema,
)

from .utils import KreamLogin

path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/list"
test_min_volume = 50
test_min_wish = 50
test_brand_name = "the north face"

test_card_data = {
    "kream_id": 93545,
    "kream_product_img_url": "https://kream-phinf.pstatic.net/MjAyMzAxMDVfMTgy/MDAxNjcyODk5Mjc1OTgw.yXEXH3igWJ4-N-Y06kN0D1vg0OzDaeRZR_y9-94sDPIg.R1y0HFw0_MoHmxRJbUsEMiOQ4FiOPmh3prb3X_a4kAEg.JPEG/a_3757826722ac4b00877f3c6588932b37.jpg?type=m",
    "kream_product_name": "the north face 1996 retro nuptse jacket dark oak",
    "brand_name": "the north face",
    "trading_volume": 2027,
    "wish": 7645,
    "review": 119,
}


@pytest.fixture(scope="session")
def raw_tag():
    html = open_html()
    soup = BeautifulSoup(html, "html.parser")
    card_list = extract_card_list(soup)
    yield card_list[0]


def open_html():
    html_path = os.path.join(path, "test.html")
    with open(html_path, "r") as f:
        r = f.read()
    return r


def extract_card_list(soup: Tag):
    return soup.find_all(class_="product_card")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def mock_scraper() -> AsyncGenerator:
    browser = await PwKreamBrowserController.start()
    sub_scraper = PwKreamListSubScraper()
    mock_scraper = PlatformListScraper(
        path,
        1,
        browser,
        sub_scraper,
        "kream",
        test_min_volume,
        test_min_wish,
    )
    yield mock_scraper


# @pytest.mark.anyio
# async def test_kream_login(mock_scraper: PlatformListScraper):
#     await mock_scraper.browser_login()
#     assert mock_scraper.browser.is_login


@pytest.mark.anyio
async def test_extract_target_list(
    mock_scraper: PlatformListScraper,
):
    mock_scraper.target_list = [test_brand_name]
    assert mock_scraper.target_list == [test_brand_name]


@pytest.mark.anyio
async def test_save_data_to_temp(mock_scraper: PlatformListScraper):
    # Given
    os.remove(os.path.join(path, "_temp", "product_card_list.json"))

    mock_card_data = [
        KreamScrapingBrandSchema(
            updated_at=datetime.now().replace(microsecond=0),
            **test_card_data,
        )
    ]

    # When
    await mock_scraper._save_data_to_temp(mock_card_data)

    # Then
    assert os.path.exists(os.path.join(path, "_temp", "product_card_list.json"))


@pytest.mark.anyio
async def test_save_scrap_status_to_temp(mock_scraper: PlatformListScraper):
    # Given
    os.remove(os.path.join(path, "_temp", "scrap_status.json"))

    # When
    for _ in range(3):
        status = f"success : 1 개"
        template = PlatformScrapStatus(
            platform_type="kream", job="the north face", status=status
        )
        await mock_scraper.save_scrap_status_to_temp(template)

    # Then
    assert os.path.exists(os.path.join(path, "_temp", "scrap_status.json"))


@pytest.mark.anyio
async def test_create_report_data(mock_scraper: PlatformListScraper):
    # Given
    mock_scraper.set_scrap_time()
    data = await mock_scraper.load_temp_scrap_data()

    # When
    report_data = mock_scraper.create_report_template(data)

    # Then
    assert report_data.db_update == False


@pytest.mark.anyio
async def test_create_scrap_report(mock_scraper: PlatformListScraper):
    # Given
    shutil.rmtree(os.path.join(path, "_report"))

    # When
    await mock_scraper.create_scrap_report()

    # Then
    assert os.path.exists(os.path.join(path, "_report"))


@pytest.mark.anyio
async def test_generate_file_path(mock_scraper: PlatformListScraper):
    # Given
    scrap_time = mock_scraper.set_scrap_time()
    print(scrap_time)
    file_name = scrap_time + "-product_card_list" + ".parquet.gzip"
    test_file_path = os.path.join(path, "kream", file_name)

    file_path = mock_scraper.generate_file_path()

    assert file_path == test_file_path


@pytest.mark.anyio
async def test_load_scrap_data(mock_scraper: PlatformListScraper):
    # When
    data = await mock_scraper.load_scrap_data()

    # Then
    assert data[0]["kream_id"] == 93545


@pytest.mark.anyio
async def test_save_scrap_data(mock_scraper: PlatformListScraper):
    # Given
    scrap_time = mock_scraper.set_scrap_time()

    # When
    await mock_scraper.save_scrap_data()

    # Then
    assert os.path.exists(os.path.join(path, "kream"))
