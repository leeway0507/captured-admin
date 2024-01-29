import os
import pytest
from shop_scrap.shop_list.urban_industry import PwUrbanIndustryListSubScraper
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
async def sub_scraper_mock():
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageHandler(page)
    sub_scraper = PwUrbanIndustryListSubScraper()
    sub_scraper.late_binding(pw_page, "urban_industry")
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_handler.go_to(html("list"))
    yield sub_scraper


@pytest.mark.anyio
async def test_extract(sub_scraper_mock: PwUrbanIndustryListSubScraper):
    # When
    # await sub_scraper.page_handler.go_to(html("seven_store"))
    raw_html = await sub_scraper_mock._extract()

    assert len(raw_html) == 41


@pytest.mark.anyio
async def test_convert(sub_scraper_mock: PwUrbanIndustryListSubScraper):
    # When
    # await sub_scraper.page_handler.go_to(html("seven_store"))
    card_info = await sub_scraper_mock._extract()
    card_info = sub_scraper_mock._convert(card_info)

    assert len(card_info) == 41


@pytest.mark.anyio
async def test_extract_info(sub_scraper_mock: PwUrbanIndustryListSubScraper):
    # When
    # await sub_scraper.page_handler.go_to(html("seven_store"))
    card_list = await sub_scraper_mock.extract_card_html()

    # card_info_list = [sub_scraper.extract_info(c) for c in card_list]

    card_info_list = []
    for c in card_list:  # type:ignore
        try:
            card_info_list.append(sub_scraper_mock.extract_info(c))
        except:
            print(c)

    print(card_info_list[26])
    assert len(card_info_list) == 41
