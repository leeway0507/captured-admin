import os
import pytest
from shop_scrap.shop_list.ssense import PwSsenseListSubScraper
from playwright.async_api import async_playwright
from components.browser_handler import PwPageHandler

curr_path = __file__.rsplit("/", 1)[0]


@pytest.fixture(scope="module")
async def sub_scraper():
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000, headless=False)
    page = await browser.new_page()

    pw_page = PwPageHandler(page)
    sub_scraper = PwSsenseListSubScraper()
    sub_scraper.late_binding(pw_page, "ssense")
    sub_scraper.allocate_job("adidas originals")
    await sub_scraper.page_handler.go_to(
        "https://www.ssense.com/en-kr/women/product/vivienne-westwood/black-half-moon-card-holder/13404761"
    )
    await sub_scraper.page.wait_for_timeout(1000000)
    yield sub_scraper


@pytest.mark.anyio
async def test_extract(sub_scraper: PwSsenseListSubScraper):
    # When
    # await sub_scraper.page_handler.go_to(html("seven_store"))
    # success, card_list = await sub_scraper.execute()

    card_list = [0]

    print("Card List Length", len(card_list))
    print("Card List Length", len(card_list))
    print("Card List Length", len(card_list))
    print("Card List Length", len(card_list))
    print("Card List Length", len(card_list))
