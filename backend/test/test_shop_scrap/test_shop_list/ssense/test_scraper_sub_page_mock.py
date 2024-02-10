import os
import pytest
from shop_scrap.shop_list.ssense import PwSsensePageSubScraper
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
    sub_scraper = PwSsensePageSubScraper()
    sub_scraper.late_binding(pw_page)
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_handler.go_to(html("page1"))
    yield sub_scraper


# @pytest.mark.anyio
# async def test_extract_result(sub_scraper: PwSsensePageSubScraper):
#     await sub_scraper.extract_soup()
#     elem = sub_scraper.soup.find("script", attrs={"type": "application/ld+json"})

#     assert elem


# @pytest.mark.anyio
# async def test_get_card_info(sub_scraper: PwSsensePageSubScraper):
#     await sub_scraper.extract_soup()
#     card_info = sub_scraper.get_card_info()

#     # Then
#     assert list(card_info.keys()) == ["product_id", "original_price"]


# @pytest.mark.anyio
# async def test_get_size_info(sub_scraper: PwSsensePageSubScraper):
#     # When
#     await sub_scraper.extract_soup()
#     size_info = await sub_scraper.get_size()
#     print(size_info)

#     # Then
#     assert size_info[-1] == {"shop_product_size": "XL", "kor_product_size": "XL"}


@pytest.mark.anyio
async def test_captcha(sub_scraper: PwSsensePageSubScraper):
    await sub_scraper.page_handler.go_to(html("page1"))
    await sub_scraper.check_failed()

    await sub_scraper.page_handler.go_to(html("captcha"))
    with pytest.raises(RuntimeError):
        await sub_scraper.check_failed()
