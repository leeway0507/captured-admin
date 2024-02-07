import os
import pytest
from shop_scrap.shop_list.harresoe import PwHarresoeListSubScraper
from playwright.async_api import async_playwright
from components.browser_handler import PwPageHandler

curr_path = __file__.rsplit("/", 1)[0]


@pytest.fixture(scope="module")
async def sub_scraper():
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000, headless=False)
    page = await browser.new_page()
    pw_page = PwPageHandler(page)
    sub_scraper = PwHarresoeListSubScraper()
    sub_scraper.late_binding(pw_page, "18montrose")
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_handler.go_to(
        "https://harresoe.com/collections/sale#harresoe-adidas-originals"
    )
    await sub_scraper.page_handler.sleep_until(10000)
    yield sub_scraper


@pytest.mark.anyio
async def test_extract(sub_scraper: PwHarresoeListSubScraper):
    # card_list = await sub_scraper.scrap_data()

    await sub_scraper.load_page()

    # print(card_list)
