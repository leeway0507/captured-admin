import os
import pytest
from shop_scrap.shop_list.endclothing import PwEndClothingListSubScraper
from playwright.async_api import async_playwright
from components.browser_handler import PwPageHandler

curr_path = __file__.rsplit("/", 1)[0]


@pytest.fixture(scope="module")
async def sub_scraper():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(timeout=5000, headless=False)
    page = await browser.new_page()
    await page.set_viewport_size({"width": 1280, "height": 1440})
    pw_page = PwPageHandler(page)
    sub_scraper = PwEndClothingListSubScraper()
    sub_scraper.late_binding(pw_page, "endclothing")
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_handler.go_to(
        "https://www.endclothing.com/kr/brands/alexander-mcqueen"
    )
    yield sub_scraper


@pytest.mark.anyio
async def test_extractable(sub_scraper: PwEndClothingListSubScraper):
    success, card_list = await sub_scraper.scrap_data()

    print(card_list[0])
    print("len(card_list)")
    print("len(card_list)")
    print(len(card_list))
