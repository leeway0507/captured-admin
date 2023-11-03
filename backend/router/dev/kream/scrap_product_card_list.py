import asyncio
from datetime import datetime
from time import sleep
import os

from playwright.async_api import Page, ElementHandle
from bs4 import BeautifulSoup
import pandas as pd

from model.scraping_brand_model import KreamScrapingBrandSchema
from .utils import load_page

async def scrap_product_card_list(
    page: Page, brand_name: str, max_scroll: int, min_volume: int, min_wish: int
):
    """브랜드별 상품 스크롤"""

    search_url = f"https://kream.co.kr/search?keyword={brand_name}&sort=wish"
    await load_page(page, search_url)

    await _scroll_page(page, max_scroll)

    product_card_list = await page.query_selector_all(".product_card")

    path = f"router/dev/kream/data/brand/{brand_name}"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    test_dir = f"test/playwright/scraping_raw/{brand_name}_raw.parquet"
    pd.DataFrame([await card.inner_html() for card in product_card_list]).to_parquet(test_dir)

    # data validation & filtering
    product_card_list = [
        KreamScrapingBrandSchema(**await _extract_info(card)) for card in product_card_list
    ]
    product_card_list = list(
        filter(lambda x: x.trading_volume >= min_volume and x.wish >= min_wish, product_card_list)
    )

    file_name = datetime.now().strftime("%y%m%d-%H%M%S")

    # saving data
    product_card_list = [product_card.model_dump() for product_card in product_card_list]
    return pd.DataFrame(product_card_list).to_parquet(
        f"{path}/{file_name}-product_card_list.parquet.gzip", compression="gzip"
    )


async def _scroll_page(page: Page, max_scroll: int):
    scroll_distance = 1000
    delay = 1
    i = 0

    while i < max_scroll:
        i += 1
        await page.evaluate(f"(async () => {{ window.scrollTo(0, {scroll_distance}); }})();")
        scroll_distance += scroll_distance
        sleep(delay)


async def _extract_info(element: ElementHandle):
    html = await element.inner_html()

    soup = BeautifulSoup(html, "html.parser")

    kream_id = soup.find("a", class_="item_inner")["href"].split("/")[-1]  # type: ignore
    kream_product_img_url = soup.find("img", class_="image full_width")["src"]  # type: ignore
    kream_product_name = soup.find("p", class_="name").get_text(strip=True).lower()  # type: ignore
    brand_name = soup.find("p", class_="product_info_brand").get_text(strip=True).lower()  # type: ignore

    updated_at = datetime.now().replace(microsecond=0)

    trading_volume = soup.find("div", class_="status_value")
    if trading_volume is None:
        trading_volume = 0
    else:
        trading_volume = _convert_str_to_int(trading_volume.get_text(strip=True))

    wish = soup.find("span", class_="wish_figure")
    if wish is None:
        wish = 0
    else:
        wish = _convert_str_to_int(wish.get_text(strip=True))

    review = soup.find("span", class_="review_figure")
    if review is None:
        review = 0
    else:
        review = _convert_str_to_int(review.get_text(strip=True))

    return {
        "kream_id": kream_id,
        "kream_product_img_url": kream_product_img_url,
        "kream_product_name": kream_product_name,
        "brand_name": brand_name,
        "trading_volume": trading_volume,
        "wish": wish,
        "review": review,
        "updated_at": updated_at,
    }


def _convert_str_to_int(value: str) -> int:
    """문자열을 숫자로 변환"""

    if "거래" in value:
        value = value.replace("거래", "").replace(" ", "")

    if "만" in value:
        value = value.replace("만", "")
        return int(float(value) * 10000)

    value = value.replace(",", "")
    return int(value)
