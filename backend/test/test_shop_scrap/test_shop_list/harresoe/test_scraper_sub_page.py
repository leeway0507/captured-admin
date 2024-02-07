import os
import pytest
from shop_scrap.shop_list.harresoe import PwHarresoePageSubScraper
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
async def sub_scraper():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageHandler(page)
    sub_scraper = PwHarresoePageSubScraper()
    sub_scraper.late_binding(pw_page)
    sub_scraper.allocate_job(
        {
            "shop_product_card_id": "9787",
            "product_url": "https://harresoe.com/products/1906r-white-virtual-blue-m1906rcf",
        }
    )
    await sub_scraper.page_handler.go_to(html("page"))
    yield sub_scraper


@pytest.mark.anyio
async def test_get_size_custom(sub_scraper: PwHarresoePageSubScraper):
    size_info = await sub_scraper._extract()

    r = sub_scraper.get_size_custom(size_info[0])
    print(r)

    assert isinstance(r, list)


# @pytest.mark.anyio
# async def test_extract_all_size(sub_scraper: PwHarresoePageSubScraper):
#     size_info = await sub_scraper._extract()

#     l = set()
#     for i in size_info:
#         r = sub_scraper.get_size_custom(i)
#         for s in r:
#             l.add(s["shop_product_size"])
#     print(l)


# @pytest.mark.anyio
# async def test_extract_info(sub_scraper: PwHarresoePageSubScraper):
#     size_info = await sub_scraper._extract()

#     r = sub_scraper.extract_info(size_info[0])
#     print(r)

#     assert isinstance(r, dict)


# @pytest.mark.anyio
# async def test_execute(sub_scraper: PwHarresoePageSubScraper):
#     x = await sub_scraper.execute()

#     print(x)

#     # Then
#     assert isinstance(x, tuple)
