import os
import pytest
from components.dev.shop.shop_list.consortium import PwConsortiumPageSubScraper
from playwright.async_api import async_playwright
from components.dev.utils.browser_controller import PwPageController

html_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/dev/shop/shop_page/consortium"
)
test_html = f"file://{os.path.join(html_path,'test.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def sub_scraper():
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageController(page)
    sub_scraper = PwConsortiumPageSubScraper()
    sub_scraper.late_binding(pw_page)
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_controller.go_to(test_html)
    yield sub_scraper


@pytest.mark.anyio
async def test_scrap_size(sub_scraper: PwConsortiumPageSubScraper):
    # When
    cards = await sub_scraper.scrap_size_from_html()

    # Then
    assert cards == [
        "UK 3.5",
        "UK 4",
        "UK 4.5",
        "UK 5",
        "UK 5.5",
        "UK 6",
        "UK 6.5",
        "UK 7",
        "UK 8.5",
        "UK 9",
        "UK 9.5",
        "UK 10",
        "UK 10.5",
        "UK 11",
        "UK 11.5",
        "UK 12",
        "UK 12.5",
        "UK 13",
        "UK 13.5",
    ]


@pytest.mark.anyio
async def test_get_size_info(sub_scraper: PwConsortiumPageSubScraper):
    # When
    size_info = await sub_scraper.get_size()

    # Then
    assert size_info[0] == {"shop_product_size": "UK 3.5", "kor_product_size": "UK 3.5"}


@pytest.mark.anyio
async def test_scrap_product_id(sub_scraper: PwConsortiumPageSubScraper):
    # When
    product_id = await sub_scraper.scrap_product_id_from_html()

    # Then
    assert isinstance(product_id, str)


@pytest.mark.anyio
async def test_get_product_id(sub_scraper: PwConsortiumPageSubScraper):
    # When
    product_id = await sub_scraper.get_product_id()

    # Then
    assert product_id == "B75806"


# ## scraper 테스트용 데이터 저장
# @pytest.mark.anyio
# async def test_execute_job(sub_scraper: PwConsortiumPageSubScraper):
#     #
#     # When
#     product_id = await sub_scraper.get_product_id()
#     size = await sub_scraper.get_size()
#     shop_product_card_id = "12345"

#     ## scraper 테스트용 데이터 저장
#     import json

#     with open(os.path.join(html_path, "shop_product_page.json"), "w") as f:
#         l = [
#             "success",
#             {
#                 "product_id": product_id,
#                 "size": size,
#                 "shop_product_card_id": shop_product_card_id,
#             },
#         ]
#         f.write(json.dumps(l, indent=4, ensure_ascii=False))
