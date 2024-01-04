import os
import pytest
from components.dev.shop.shop_list.consortium import PwConsortiumListSubScraper
from playwright.async_api import async_playwright
from components.dev.utils.browser_controller import PwPageController

html_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/dev/shop/shop_list/consortium"
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
    sub_scraper = PwConsortiumListSubScraper()
    sub_scraper.late_binding(pw_page)
    sub_scraper.allocate_job("adidas")
    await sub_scraper.page_controller.go_to(test_html)
    yield sub_scraper


@pytest.fixture(scope="module")
async def list_result(sub_scraper: PwConsortiumListSubScraper):
    cards = await sub_scraper.extract_card_html()
    yield cards


@pytest.mark.anyio
async def test_extract_card_html(sub_scraper: PwConsortiumListSubScraper):
    # When
    cards = await sub_scraper.extract_card_html()

    # Then
    assert len(cards) == 50  # type: ignore


@pytest.mark.anyio
async def test_extradct_info(sub_scraper: PwConsortiumListSubScraper, list_result):
    preprocessed_data = sub_scraper.extract_info(list_result[0])

    test_data = {
        "shop_name": "consortium",
        "brand_name": "adidas",
        "shop_product_name": "adidas-spezial-gazelle-spzl-dark-green-footwear-white-off-white-if5787",
        "shop_product_img_url": "https://www.consortium.co.uk/media/catalog/product/cache/1/small_image/600x600/9df78eab33525d08d6e5fb8d27136e95/a/d/adidas-spezial-gazelle-spzl-dark-green-footwear-white-off-white-if5787_0000_cat.jpg",
        "product_url": "https://www.consortium.co.uk/adidas-spezial-gazelle-spzl-dark-green-footwear-white-off-white-if5787.html",
        "product_id": "if5787",
        "price": "£109.99",
    }

    assert preprocessed_data.model_dump() == test_data

    # scraper 테스트용 데이터 저장
    # import json

    # with open(os.path.join(html_path, "shop_product_list.json"), "w") as f:
    #     l = list(map(lambda x: sub_scraper.extract_info(x).model_dump(), list_result))
    #     f.write(json.dumps(l, indent=4, ensure_ascii=False))
