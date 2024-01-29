from typing import AsyncGenerator
import pytest

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from model.kream_scraping import KreamScrapingBrandSchema
from components.browser_handler import PwPageHandler
from platform_scrap.list.scraper_sub import PwKreamListSubScraper


curr_path = __file__.rsplit("/", 1)[0]
test_max_scroll = 2
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
    pw_page = PwPageHandler(page)
    scraper = PwKreamListSubScraper()
    scraper.late_binding(pw_page, test_max_scroll, test_min_volume, test_min_wish)
    scraper.allocate_job(test_brand_name)
    yield scraper


@pytest.mark.anyio
async def test_go_to_list_page(sub_scraper: PwKreamListSubScraper):
    # When
    await sub_scraper._go_to_page()

    # Then
    page_url = sub_scraper.page.url
    assert page_url == "https://kream.co.kr/search?keyword=the%20north%20face&sort=wish"


@pytest.mark.anyio
async def test_extract_card_list_from_page(sub_scraper: PwKreamListSubScraper):
    # When
    raw_card = await sub_scraper._extract_card_list_from_page()

    print(raw_card)

    assert type(raw_card[0]) == BeautifulSoup  # type:ignore


@pytest.mark.anyio
async def test_execute_job(
    sub_scraper: PwKreamListSubScraper,
):
    card_data = await sub_scraper.execute()
    print(f"scrap count: {len(card_data[1])}")
    assert type(card_data[1][0]) == KreamScrapingBrandSchema
