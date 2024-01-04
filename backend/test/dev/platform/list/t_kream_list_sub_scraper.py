from typing import AsyncGenerator, List
import os
import pytest

from playwright.async_api import async_playwright
from bs4 import Tag, BeautifulSoup

from components.dev.utils.browser_controller import PwPageController
from components.dev.platform.list.sub_scraper import (
    PwKreamListSubScraper,
    KreamScrapingBrandSchema,
)


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
async def sub_scraper() -> AsyncGenerator:
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageController(page)
    scraper = PwKreamListSubScraper()
    scraper.late_binding(pw_page, test_min_volume, test_min_wish)
    yield scraper


@pytest.mark.anyio
async def test_get_brand_name_error_of_sub_scraper(
    sub_scraper: PwKreamListSubScraper,
):
    with pytest.raises(ValueError):
        brand_name = sub_scraper.brand_name


@pytest.mark.anyio
async def test_set_brand_name_of_sub_scraper(sub_scraper: PwKreamListSubScraper):
    # When
    sub_scraper.brand_name = test_brand_name

    # Then
    assert sub_scraper.brand_name == test_brand_name


@pytest.mark.anyio
async def test_go_to_list_page(sub_scraper: PwKreamListSubScraper):
    # Given
    sub_scraper.brand_name = test_brand_name

    # When
    await sub_scraper._goto_list_page()

    # Then
    page_url = sub_scraper.page.page.url
    assert page_url == "https://kream.co.kr/search?keyword=the%20north%20face&sort=wish"


@pytest.mark.anyio
async def test_extract_card_list_from_page(sub_scraper: PwKreamListSubScraper):
    # When
    raw_card = await sub_scraper._extract_card_list_from_page()

    assert type(raw_card[0]) == BeautifulSoup


def test_get_kream_id(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    kream_id = sub_scraper._get_kream_id(raw_tag)

    # Then
    assert kream_id == card_data["kream_id"]


def test_get_kream_product_img_url(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    kream_product_img_url = sub_scraper._get_kream_product_img_url(raw_tag)

    # Then
    assert kream_product_img_url == card_data["kream_product_img_url"]


def test_get_kream_product_name(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    kream_product_name = sub_scraper._get_kream_product_name(raw_tag)

    # Then
    assert kream_product_name == card_data["kream_product_name"]


def test_get_brand_name(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    brand_name = sub_scraper._get_brand_name(raw_tag)

    # Then
    assert brand_name == card_data["brand_name"]


def test_get_trading_volume(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    trading_volume = sub_scraper._get_trading_volume(raw_tag)

    # Then
    assert trading_volume == card_data["trading_volume"]


def test_get_review_count(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    review_count = sub_scraper._get_review_count(raw_tag)

    # Then
    assert review_count == card_data["review"]


def test_get_wish_count(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    wish_count = sub_scraper._get_wish_count(raw_tag)

    # Then
    assert wish_count == card_data["wish"]


def test_extract_info(sub_scraper: PwKreamListSubScraper, raw_tag: Tag):
    # When
    info = sub_scraper._extract_info(raw_tag)

    # Then
    info_data = info.model_dump()
    info_data.pop("updated_at")

    assert info_data == card_data


@pytest.mark.anyio
async def test_execute_job(
    sub_scraper: PwKreamListSubScraper,
):
    sub_scraper.allocate_job(test_brand_name)
    card_data = await sub_scraper.execute(max_scroll=1)
    assert type(card_data[0]) == KreamScrapingBrandSchema
