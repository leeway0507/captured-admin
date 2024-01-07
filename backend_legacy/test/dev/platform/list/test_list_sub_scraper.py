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


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def sub_scraper() -> AsyncGenerator:
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(headless=False, timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageController(page)
    scraper = PwKreamListSubScraper()
    scraper.late_binding(pw_page, test_min_volume, test_min_wish)
    scraper.allocate_job(test_brand_name)
    yield scraper


@pytest.mark.anyio
async def test_go_to_list_page(sub_scraper: PwKreamListSubScraper):
    # When
    await sub_scraper._goto_list_page()

    # Then
    page_url = sub_scraper.page_controller.page.url
    assert page_url == "https://kream.co.kr/search?keyword=the%20north%20face&sort=wish"


@pytest.mark.anyio
async def test_extract_card_list_from_page(sub_scraper: PwKreamListSubScraper):
    # When
    raw_card = await sub_scraper._extract_card_list_from_page()

    assert type(raw_card[0]) == BeautifulSoup


@pytest.mark.anyio
async def test_execute_job(
    sub_scraper: PwKreamListSubScraper,
):
    card_data = await sub_scraper.execute(max_scroll=5)
    print(f"scrap count: {len(card_data[1])}")
    assert type(card_data[1][0]) == KreamScrapingBrandSchema
