from typing import AsyncGenerator, List
import os
import pytest

from playwright.async_api import async_playwright
from bs4 import Tag, BeautifulSoup

from components.dev.utils.browser_controller import PwPageController
from components.dev.platform.list.sub_scraper import PwKreamListSubScraper


path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/list"
test_min_volume = 50
test_min_wish = 50
test_brand_name = "the north face"

card_data = {
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
async def mock_sub_scraper() -> AsyncGenerator:
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageController(page)
    scraper = PwKreamListSubScraper()
    scraper.late_binding(pw_page, test_min_volume, test_min_wish)
    yield scraper


@pytest.mark.anyio
async def test_get_kream_id(mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    kream_id = mock_sub_scraper._get_kream_id(raw_tag)

    # Then
    assert kream_id == card_data["kream_id"]


@pytest.mark.anyio
async def test_get_kream_product_img_url(
    mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag
):
    # When
    kream_product_img_url = mock_sub_scraper._get_kream_product_img_url(raw_tag)

    # Then
    assert kream_product_img_url == card_data["kream_product_img_url"]


@pytest.mark.anyio
async def test_get_kream_product_name(
    mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag
):
    # When
    kream_product_name = mock_sub_scraper._get_kream_product_name(raw_tag)

    # Then
    assert kream_product_name == card_data["kream_product_name"]


@pytest.mark.anyio
async def test_get_brand_name(mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    brand_name = mock_sub_scraper._get_brand_name(raw_tag)

    # Then
    assert brand_name == card_data["brand_name"]


@pytest.mark.anyio
async def test_get_trading_volume(
    mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag
):
    # When
    trading_volume = mock_sub_scraper._get_trading_volume(raw_tag)

    # Then
    assert trading_volume == card_data["trading_volume"]


@pytest.mark.anyio
async def test_get_review_count(mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    review_count = mock_sub_scraper._get_review_count(raw_tag)

    # Then
    assert review_count == card_data["review"]


@pytest.mark.anyio
async def test_get_wish_count(mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    wish_count = mock_sub_scraper._get_wish_count(raw_tag)

    # Then
    assert wish_count == card_data["wish"]


@pytest.mark.anyio
async def test_extract_info(mock_sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    info = mock_sub_scraper._extract_info(raw_tag)

    # Then
    info_data = info.model_dump()
    info_data.pop("updated_at")

    assert info_data == card_data
