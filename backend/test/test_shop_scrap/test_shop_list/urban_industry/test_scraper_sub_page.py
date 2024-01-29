import os
import pytest
from shop_scrap.shop_list.urban_industry import PwUrbanIndustryPageSubScraper
from playwright.async_api import async_playwright
from components.browser_handler import PwPageHandler

curr_path = __file__.rsplit("/", 1)[0]


def html(name: str):
    return f"file://{os.path.join(curr_path,name+'.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def sub_scraper():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageHandler(page)
    sub_scraper = PwUrbanIndustryPageSubScraper()
    sub_scraper.late_binding(pw_page)
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_handler.go_to(html("page2"))
    yield sub_scraper


@pytest.mark.anyio
async def test_seven_store_get_card_info(sub_scraper: PwUrbanIndustryPageSubScraper):
    card_info = await sub_scraper.get_card_info()

    # Then
    assert list(card_info.keys()) == ["product_id", "original_price"]


@pytest.mark.anyio
async def test_seven_store_get_size_info(sub_scraper: PwUrbanIndustryPageSubScraper):
    # When
    size_info = await sub_scraper.get_size()
    print(size_info)

    # Then
    assert size_info[0] == {"shop_product_size": "M", "kor_product_size": "M"}


@pytest.mark.anyio
async def test_seven_store_scrap_product_id(sub_scraper: PwUrbanIndustryPageSubScraper):
    # When
    product_id = await sub_scraper.get_product_id()
    print(product_id)

    # Then
    assert isinstance(product_id, str)
