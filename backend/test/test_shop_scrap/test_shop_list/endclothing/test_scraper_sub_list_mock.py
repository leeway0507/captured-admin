import os
import pytest
from shop_scrap.shop_list.endclothing import PwEndClothingListSubScraper
from playwright.async_api import async_playwright
from components.browser_handler import PwPageHandler
from random import randint

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
    sub_scraper = PwEndClothingListSubScraper()
    sub_scraper.late_binding(pw_page, "endclthing")
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_handler.go_to(html("list"))
    yield sub_scraper


# @pytest.mark.anyio
# async def test_extract(sub_scraper_mock: PwEndClothingListSubScraper):
#     # When
#     # await sub_scraper.page_handler.go_to(html("seven_store"))
#     raw_html = await sub_scraper_mock._extract()

#     assert len(raw_html) == 120


@pytest.mark.anyio
async def test_extract_info(sub_scraper_mock: PwEndClothingListSubScraper):
    # When
    card_list = await sub_scraper_mock.extract_card_html()

    if not card_list:
        raise (ValueError("No None"))
    card_info_list = sub_scraper_mock.extract_info(card_list[0])
    print(card_info_list)

    x = [sub_scraper_mock.extract_info(c) for c in card_list]
    print(x[randint(0, len(x))])
    assert isinstance(card_info_list, dict)


@pytest.mark.anyio
async def test_has_next_page(sub_scraper_mock: PwEndClothingListSubScraper):
    # When
    page = await sub_scraper_mock.has_next_page(0)

    assert page == True
