import os
import pytest
from shop_scrap.shop_list.seven_store import PwSevenStorePageSubScraper
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
    browser = await pw.firefox.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageHandler(page)
    sub_scraper = PwSevenStorePageSubScraper()
    sub_scraper.late_binding(pw_page)
    sub_scraper.allocate_job("12345")
    await sub_scraper.page_handler.go_to(html("seven_store"))
    yield sub_scraper


@pytest.mark.anyio
async def test_seven_store_get_card_info(sub_scraper: PwSevenStorePageSubScraper):
    # When
    # await sub_scraper.page_handler.go_to(html("seven_store"))
    card_info = await sub_scraper.get_card_info()

    print(card_info)

    # Then
    assert card_info == {
        "product_id": "B500BT17*NORETURNSACCEPTEDONPERSONALCAREUNLESSFAULTY.",
        "original_price": "£31.00",
    }


@pytest.mark.anyio
async def test_seven_store_get_size_info(sub_scraper: PwSevenStorePageSubScraper):
    # When
    size_info = await sub_scraper.get_size()
    print(size_info)

    # Then
    assert size_info[0] == {"shop_product_size": "UK 3.5", "kor_product_size": "UK 3.5"}


@pytest.mark.anyio
async def test_seven_store_scrap_product_id(sub_scraper: PwSevenStorePageSubScraper):
    # When
    product_id = await sub_scraper.get_product_id()
    print(product_id)

    # Then
    assert isinstance(product_id, str)


# ## scraper 테스트용 데이터 저장
# @pytest.mark.anyio
# async def test_execute_job(sub_scraper: PwSevenStorePageSubScraper):
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
