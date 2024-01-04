from typing import AsyncGenerator, List
import os
import pytest
from datetime import date, timedelta

from playwright.async_api import async_playwright
from bs4 import Tag, BeautifulSoup

from components.dev.utils.browser_controller import PwPageController
from components.dev.platform.page.sub_scraper import PwKreamPageSubScraper


path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/page"
html_path = os.path.join(path, "html")
test_min_volume = 50
test_min_wish = 50
test_brand_name = "Adidas"

html_path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/page/html/"
product_detail_path = f"file://{os.path.join(html_path,'product_detail.html')}"
buy_and_sell_path = f"file://{os.path.join(html_path,'buy.html')}"
trading_volume_path = f"file://{os.path.join(html_path,'trading_volume.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def sub_scraper() -> AsyncGenerator:
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000)
    page = await browser.new_page()
    pw_page = PwPageController(page)
    scraper = PwKreamPageSubScraper()
    scraper.late_binding(pw_page)
    scraper.allocate_job(96970)
    yield scraper


@pytest.fixture(scope="module")
async def product_detail_scraper(sub_scraper: PwKreamPageSubScraper):
    await sub_scraper.page_controller.go_to(product_detail_path)
    yield sub_scraper


@pytest.fixture(scope="module")
async def buy_and_sell_scraper(sub_scraper: PwKreamPageSubScraper):
    await sub_scraper.page_controller.go_to(buy_and_sell_path)
    yield sub_scraper


@pytest.fixture(scope="module")
async def trading_volume_scraper(sub_scraper: PwKreamPageSubScraper):
    await sub_scraper.page_controller.go_to(trading_volume_path)
    yield sub_scraper


@pytest.mark.anyio
async def test_go_to_card_page(sub_scraper: PwKreamPageSubScraper):
    # When
    await sub_scraper.go_to_card_page()

    # Then
    assert sub_scraper.page.url == sub_scraper.get_url()


@pytest.mark.anyio
async def test_product_detail_scrap_product_title(
    product_detail_scraper: PwKreamPageSubScraper,
):
    # When
    title: str = await product_detail_scraper._scrap_product_title()

    # Then
    assert title.strip() == "Adidas Tobacco Phantone Mesa"


@pytest.mark.anyio
async def test_product_detail_scrap_details(
    product_detail_scraper: PwKreamPageSubScraper,
):
    # When
    details = await product_detail_scraper._scrap_product_details()

    # Then
    test_details = [
        ["발매가", "€110 (약 157,100원)"],
        ["모델번호", "GY7396"],
        ["출시일", "-"],
        ["대표 색상", "phantone/mesa/gum 4"],
    ]

    assert details == test_details


@pytest.mark.anyio
async def test_product_detail_scrap_review(
    product_detail_scraper: PwKreamPageSubScraper,
):
    # When
    review = await product_detail_scraper._scrap_review()

    # Then
    assert review == 74


@pytest.mark.anyio
async def test_product_detail_scrap_product_img(
    product_detail_scraper: PwKreamPageSubScraper,
):
    # When
    kream_product_img_url = await product_detail_scraper._scrap_product_img_url()

    # Then
    assert "https://kream-phinf.pstatic.net" in kream_product_img_url


@pytest.mark.anyio
async def test_product_detail_scrap_brand(
    product_detail_scraper: PwKreamPageSubScraper,
):
    # When
    brand = await product_detail_scraper._scrap_brand()

    # Then
    assert brand == test_brand_name


@pytest.mark.anyio
async def test_product_detail_scrap_wish(
    product_detail_scraper: PwKreamPageSubScraper,
):
    # When
    wish = await product_detail_scraper._scrap_wish()

    # Then
    assert wish == "1.3만"


@pytest.mark.anyio
async def test_buy_and_sell_scrap_buy_and_sell_page(
    buy_and_sell_scraper: PwKreamPageSubScraper,
):
    sell_list = await buy_and_sell_scraper._scrap_buy_and_sell_page("sell")

    test_sell_list = {
        "220": "0",
        "225": "0",
        "230": "420000",
        "235": "399000",
        "240": "349000",
        "245": "310000",
        "250": "294000",
        "255": "310000",
        "260": "379000",
        "265": "308000",
        "270": "271000",
        "275": "250000",
        "280": "232000",
        "285": "269000",
        "290": "208000",
        "295": "210000",
        "300": "299000",
        "305": "0",
        "310": "0",
        "315": "0",
        "320": "0",
    }

    assert sell_list == test_sell_list


def test_trading_volume_extract_target_date(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # When
    trading_volume_scraper._set_target_date(10)

    # Then
    assert trading_volume_scraper.target_date == date.today() - timedelta(days=10)


@pytest.mark.anyio
async def test_trading_volume_scrap_date_is_today(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # Given
    trading_volume_scraper._set_target_date(10)

    # When
    result = trading_volume_scraper._scrap_date_is_today()

    # Then
    assert result == False


@pytest.mark.anyio
async def test_trading_volume_is_trading_volume_loaded(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # When
    result = await trading_volume_scraper._is_trading_volume_loaded()

    # Then
    assert result == True


@pytest.mark.anyio
async def test_trading_volume_scroll_until(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # Given
    trading_volume_scraper._set_target_date(10)

    # When
    scrap_result = await trading_volume_scraper._scroll_until()

    # Then
    last_data = scrap_result["last_date"]
    assert last_data.strftime("%Y-%m-%d") == "2023-09-18"


@pytest.mark.anyio
async def test_trading_volume_get_transaction_count(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # When
    trading_volum_count = await trading_volume_scraper._get_trading_volume_count()

    # Then
    assert trading_volum_count == 150


@pytest.mark.anyio
async def test_trading_volume_get_last_date_trading_volume(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # When
    last_scrap_date = await trading_volume_scraper._get_last_date_trading_volume()

    # Then
    assert last_scrap_date.strftime("%Y-%m-%d") == "2023-09-18"


@pytest.mark.anyio
async def test_trading_volume_extract_volume_data_from(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    volumes = await trading_volume_scraper.get_soup_all(".body_list")
    data = trading_volume_scraper._extract_volume_data_from(volumes)

    assert len(data) == 150


@pytest.mark.anyio
async def test_trading_volume_scrap_trading_volume_data(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # Given
    volumes = await trading_volume_scraper.get_soup_all(".body_list")
    data = trading_volume_scraper._extract_volume_data_from(volumes)

    # When
    scrap_data = trading_volume_scraper._scrap_trading_volume_data(data)

    # Then
    assert len(scrap_data) == 150


@pytest.mark.anyio
async def test_trading_volume_filter_trading_volume_data(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # Given
    volumes = await trading_volume_scraper.get_soup_all(".body_list")
    data = trading_volume_scraper._extract_volume_data_from(volumes)
    scrap_data = trading_volume_scraper._scrap_trading_volume_data(data)

    # When
    filter_data = trading_volume_scraper._filter_trading_volume_data(scrap_data)

    # Then
    assert len(filter_data) == 14


@pytest.mark.anyio
async def test_trading_volume_extract_trading_volume(
    trading_volume_scraper: PwKreamPageSubScraper,
):
    # Given
    trading_volume_scraper._set_target_date(10)

    # When
    scrap_result = await trading_volume_scraper._extract_trading_volume()

    # Then
    assert scrap_result[0] == "success"


# @pytest.mark.anyio
# async def test_trading_volume(
#     trading_volume_scraper: PwKreamPageSubScraper,
# ):


# ### PageScraper 용 데이터 생성
# import json

# buy_path = f"file://{os.path.join(html_path,'buy.html')}"
# sell_path = f"file://{os.path.join(html_path,'sell.html')}"


# @pytest.mark.anyio
# async def test_execute_sub_process_job(sub_scraper: PwKreamPageSubScraper):
#     await sub_scraper.page_controller.go_to(product_detail_path)
#     (
#         product_detail_status,
#         product_detail_data,
#     ) = await sub_scraper.scrap_product_detail()

#     # Json Serialize 때문에 어쩔 수 없이 넣음
#     strf_time = product_detail_data["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
#     product_detail_data.update({"updated_at": strf_time})

#     await sub_scraper.page_controller.go_to(buy_path)
#     buy_data = await sub_scraper._scrap_buy_and_sell_page("buy")

#     await sub_scraper.page_controller.go_to(sell_path)
#     sell_data = await sub_scraper._scrap_buy_and_sell_page("sell")

#     await sub_scraper.page_controller.go_to(trading_volume_path)
#     sub_scraper._set_target_date()
#     (
#         trading_volume_status,
#         trading_volume_data,
#     ) = await sub_scraper._extract_trading_volume()

#     data = {
#         "status": {
#             "product_detail": "success",
#             "buy_and_sell": "success",
#             "trading_volume": trading_volume_status,
#         },
#         "data": {
#             "product_detail": product_detail_data,
#             "buy_and_sell": {"sell": sell_data, "buy": buy_data},
#             "trading_volume": trading_volume_data,
#         },
#     }

#     with open("test_scrap_result.json", "w") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
