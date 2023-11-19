import os
import asyncio
from itertools import chain
from traceback import format_exception

from typing import Optional, List, Dict, Any, Union, Tuple
from datetime import date, datetime, timedelta

from playwright.async_api import Page
from bs4 import BeautifulSoup
import bs4
import pandas as pd
import aiofiles
import json

from dotenv import dotenv_values

from ...custom_playwright.page import KreamPage
from .utils import load_page, load_cookies, convert_str_to_int
from model.db_model_kream import KreamBuyAndSellSchema, KreamTradingVolumeSchema
from model.kream_scraping import KreamProductDetailSchema
from .create_log import create_last_update_kream_detail_log


config = dotenv_values(".env.dev")


async def scrap_product_detail_main(
    kream_page: KreamPage,
    brand: str,
    target_kream_ids: Optional[str] = None,
    num_process: int = 1,
):
    """브랜드별 상품 스크롤"""
    none_init_error = "kream_page가 None입니다. init 메서드를 먼저 실행해주세요."
    none_context_error = "context가 None입니다. init 메서드를 먼저 실행해주세요."

    assert kream_page.init_page, none_init_error
    assert kream_page.context, none_context_error

    init_tempfiles()
    n_p = num_process - 1
    p_list = [await kream_page.context.new_page() for _ in range(n_p)]
    p_list.append(kream_page.init_page)

    if target_kream_ids:
        k_list = target_kream_ids.split(",")
    else:
        k_list = load_kream_id_list(brand)

    print(f"scrap len : {len(k_list)}")

    split_k_list = split_size(k_list, num_process)
    co_list = [
        scrap_product_sub_process(p_list[i], split_k_list[i])
        for i in range(num_process)
    ]
    result = await asyncio.gather(*co_list)
    merged_result = {k: v.replace("=", "") for d in result for k, v in d.items()}

    path = config["KREAM_DETAILS_TEMP_DIR"]
    assert path, "Env KREAM_DETAILS_TEMP_DIR does not exist"
    path += "process_result.json"
    if target_kream_ids:
        ref_product_card = target_kream_ids
    else:
        ref_product_card = get_last_update_product_card_name(brand)[1]

    with open(path, "w") as f:
        meta = {
            "num_process": num_process,
            "ref_product_card": ref_product_card,
            "db_update": False,
            "scrap_result": merged_result,
        }
        f.write(json.dumps(meta, ensure_ascii=False))

    scrap_name = None
    try:
        scrap_name = await save_scrap_files(brand)  # type:ignore
        create_last_update_kream_detail_log(scrap_name)

    except Exception as e:
        print("scrap_product_detail_main")
        print("".join(format_exception(None, e, e.__traceback__)))
        return {
            "scrap_status": "fail",
            "scrap_name": None,
            "scrap_result": merged_result,
            "error": str(e),
        }

    return {"scrap_status": "success", "scrap_name": scrap_name}


async def scrap_product_sub_process(page: Page, kream_id_list: List[int]):
    """브랜드별 상품 스크롤"""
    # load_cookies
    # await asyncio.sleep(2)
    # await load_cookies(page)
    # await asyncio.sleep(2)

    lst = {k: "not_scrap" for k in kream_id_list}
    kream_id_list_list = [[k, 0] for k in kream_id_list]
    for i, kream_id in enumerate(kream_id_list_list):
        print(f"{i+1}/{len(kream_id_list_list)}")

        kream_id, iter_count = kream_id

        try:
            url = f"https://kream.co.kr/products/{kream_id}"
            await load_page(page, url)

            p_detail = await get_product_detail(page, kream_id)
            await _save_temp_files("product_detail", p_detail)

            await asyncio.sleep(2)
            buy_and_sell = await get_buy_and_sell(page, kream_id)
            await _save_temp_files("buy_and_sell", buy_and_sell)

            await asyncio.sleep(2)
            result, trading_volume = await get_product_volume(page, kream_id)
            await _save_temp_files("trading_volume", trading_volume)

            # success,no_trading_volume,failed
            if result == "success":
                lst[kream_id] = "success"

            elif result == "no_trading_volume":
                lst[kream_id] = "success:no_trading_volume"

            else:
                lst[kream_id] = "failed:can't scrap trading_volume"

        except Exception as e:
            if iter_count == 0:
                print(f"{kream_id} 실패 :")
                print("".join(format_exception(None, e, e.__traceback__)))
                kream_id_list_list.append([kream_id, iter_count + 1])

            else:
                print("scrap_product_sub_process")
                print("".join(format_exception(None, e, e.__traceback__)))
                lst[kream_id] = str(e)

            await page.close()
            page = await page.context.new_page()
            continue

    await page.close()
    return lst


# ==========================
# product detail ==========
# ==========================


async def get_product_detail(page: Page, kream_id: int) -> Dict[str, Any]:
    soup_list = await get_soup_all(page, ".detail-box")

    d_list = [soup.get_text(strip=True, separator="|").split("|") for soup in soup_list]

    title = await page.query_selector("p.title")
    assert title, "get_product_detail : p.title is None."
    kream_product_name = await title.inner_text()

    review = await page.query_selector(".product_detail_item_title.reviews")
    assert review, "get_product_detail : review is None"
    review = await review.inner_text()
    review = review.split(" ")
    if len(review) == 1:
        review = "0"
    else:
        review = review[-1].strip()

    img_url = await page.query_selector(".picture.product_img")
    assert img_url, "get_product_detail : img_url is None"
    img_url = BeautifulSoup(await img_url.inner_html(), "html.parser")
    kream_product_img_url = img_url.find("img")["src"]  # type:ignore

    brand = await page.query_selector(
        "div.product-branding-feed-container > div > div > div > span "
    )
    assert brand, "get_product_detail : brand is None"
    brand = await brand.inner_text()

    wish = await page.query_selector(".wish_count_num")
    assert wish, "get_product_detail : wish is None"
    wish = await wish.inner_text()

    return {
        "kream_id": kream_id,
        "kream_product_img_url": kream_product_img_url,
        "kream_product_name": kream_product_name,
        "brand_name": brand,
        "retail_price": d_list[0][1],
        "product_id": d_list[1][1],
        "product_release_date": d_list[2][1],
        "color": d_list[3][1],
        "wish": convert_str_to_int(wish),
        "review": convert_str_to_int(review),
        "updated_at": datetime.now().replace(microsecond=0),
    }


# ==========================
# buy_and_sell ============
# ==========================


async def get_buy_and_sell(page: Page, kream_id: int):
    """sell과 buy 정보를 가져오는 함수"""
    sell = await page.query_selector(
        "//div[contains(@class, 'btn_wrap')]/div/button[1]"
    )
    assert sell, "판매 버튼이 잡히지 않음"
    await sell.click()

    sell_list = await _buy_and_sell(page, f"sell : {kream_id}")

    await page.go_back()
    await page.wait_for_selector("//div[contains(@class, 'btn_wrap')]/div/button[2]")
    await asyncio.sleep(1)

    buy = await page.query_selector("//div[contains(@class, 'btn_wrap')]/div/button[2]")
    assert buy, "구매 버튼이 잡히지 않음"
    await buy.click()
    buy_list = await _buy_and_sell(page, f"buy : {kream_id}")
    await page.go_back()

    return {"kream_id": kream_id, "sell": sell_list, "buy": buy_list}


async def _buy_and_sell(page, info: str):
    await page.wait_for_selector('//li[contains(@class, "select_item")]', timeout=5000)

    select_list = await page.query_selector_all('//li[contains(@class, "select_item")]')
    if not select_list:
        raise Exception(f"ask 또는 bid의 select_list가 잡히지 않음 : {info}")

    select = {}
    for i in select_list:
        s = await i.query_selector('span[class="size"]')
        assert s, "size가 잡히지 않음"
        size = await s.inner_text()
        size = size.replace(" ", "")

        p = await i.query_selector('span[class="price"]')
        assert p, "price가 잡히지 않음"
        price = await p.inner_text()
        price = price.replace(",", "")

        if price == "판매입찰" or price == "구매입찰":
            price = 0
        select.update({size: price})

    return select


# ==========================
# product_volume ===========
# ==========================


async def get_product_volume(
    page: Page, kream_id: int, max_scrap_days: int = 10, **_kwargs
) -> Tuple[str, List[List[str]]]:
    start_date = _get_start_date(kream_id, limit_days=max_scrap_days)
    if date.today() == start_date:
        print("당일 업데이트가 되었음")
        return "success", []

    return await _scrap_trading_volume_from(page, start_date, kream_id)


def _get_start_date(kream_id: int, limit_days: int = 10) -> date:
    """
    trading volume에서 마지막 업데이트 된 날짜 추출

    Args:
        kream_id (str): kream_id
        limit_days (int, optional): 최소 업데이트 날짜. Defaults to 10.

    Returns:
        date: 업데이트 날짜(10일 초과 시 오늘로부터 10일 전 날짜 반환)
    """

    today = date.today()

    max_scrap_days = timedelta(days=limit_days)

    last_update = None

    # TODO:DB 업데이트 시 사용하기
    # query = f"""
    #     SELECT trading_date
    #     FROM `kream_trading_volume`
    #     WHERE kream_id = '{kream_id}'
    #     LIMIT 1
    #     """
    # last_update = execute_query(query)

    if last_update:
        last_update_day = datetime.strptime(last_update[0][0], "%y/%m/%d").date()

        if today > last_update_day + max_scrap_days:
            # 당일 기준 최대 10일 전까지 업데이트
            return today - max_scrap_days
        else:
            return last_update_day

    return today - max_scrap_days


async def _scrap_trading_volume_from(
    page: Page, target_date: date, kream_id: int, **_kwargs
) -> Tuple[str, List]:
    volume_btn = "a[class='btn outlinegrey full medium']"
    await page.wait_for_selector(volume_btn, timeout=5000)

    trading_volume_button = await page.query_selector(volume_btn)

    assert trading_volume_button, "trading_volume_button not found"
    await trading_volume_button.click()

    price_btn = "div[class='price_body']"
    try:
        await page.wait_for_selector(price_btn, timeout=5000)
    except Exception as e:
        print(f"{kream_id} : 체결내역 더보기가 없는 제품으로 추정")
        return "failed", []

    modal = await page.query_selector(price_btn)
    assert modal, "modal not found"

    # scroll until target_date
    i = 0
    start = 0
    end = 1
    while start < end and i <= 10:
        i += 1
        start = end
        await asyncio.sleep(1)
        end = await page.evaluate(
            "Array.from(document.querySelectorAll('.list_txt.is_active')).length"
        )
        date_str: str = await page.evaluate(
            f"Array.from(document.querySelectorAll('.list_txt.is_active')).slice(-1)[0].innerText"
        )
        date_str = date_str.replace("빠른배송", "").strip()
        last_date = datetime.strptime(date_str, "%y/%m/%d").date()

        # print(f"kream_id:{kream_id},last_date : {last_date}, target_date : {target_date}, end : {end}")

        if target_date < last_date:
            scroll_eval = "(async () => { document.querySelector('.price_body').scrollBy(0, 3000); })()"
            await page.evaluate(scroll_eval)
        else:
            break

    volumes = await get_soup_all(page, ".body_list")
    body_list = _extract_volume_data_from(volumes)

    df = pd.DataFrame(
        body_list, columns=["kream_product_size", "price", "lightening", "trading_at"]
    )
    df["kream_id"] = kream_id

    target_date_str = target_date.strftime("%y/%m/%d")
    result = df[df["trading_at"] >= target_date_str].to_dict("records")

    if len(df) > 0 and len(result) > 0:
        return "success", result

    if len(df) > 0 and len(result) == 0:
        return "no_trading_volume", []

    return "failed", []


def _extract_volume_data_from(body_list: List) -> List[List]:
    """
    크롤링 결과 리스트에서 거래량 추출

    Args:
        body_list (List): 크롤링 결과 리스트

    Returns:
        List: 크롤링 결과 리스트로 반환
    """

    def preprocess_items(tags) -> List:
        x = []
        for tag in tags.find_all(class_="list_txt"):
            x.append(tag.text.strip())

        if "빠" in x[2]:
            return [x[0], x[1], True, x[2].replace("빠른배송", "").strip()]
        else:
            return [x[0], x[1], False, x[2].strip()]

    return [preprocess_items(tags) for tags in body_list]


def get_last_update_product_card_name(brand_name: str, path=None) -> Tuple[str, str]:
    if path is None:
        path = config["KREAM_PRODUCT_CARD_LIST_DIR"]
        assert path, "Env KREAM_PRODUCT_CARD_LIST_DIR does not exist"
        path += brand_name

    file_list = os.listdir(path)
    file_list.sort()

    file_name = file_list[-1]

    return path, file_name


def load_kream_id_list(brand_name: str, path: Optional[str] = None) -> List[str]:
    path, file_name = get_last_update_product_card_name(brand_name, path)
    print("load : ", file_name)
    df = pd.read_parquet(path + "/" + file_name)
    return df["kream_id"].tolist()


def split_size(l: List, num_list: int) -> List[List]:
    """
    l: list
    n_l : number of list
    """
    q, r = divmod(len(l), num_list)

    if r > 0:
        # ex 10 | 3
        # 4,4,2
        # l_size = list size
        l_size = len(l) // num_list
        l_size += 1

        output = [l[i * l_size : (i + 1) * l_size] for i in range(num_list - 1)]
        output.append(l[(num_list - 1) * l_size :])

    else:
        # ex 9 | 3
        # 3,3,3
        l_size = len(l) // num_list
        output = [l[i : i + q] for i in range(0, len(l), l_size)]

    return output


def init_tempfiles():
    path = config["KREAM_DETAILS_TEMP_DIR"]
    assert path, "Env KREAM_DETAILS_TEMP_DIR does not exist"

    file_list = os.listdir(path)
    for file in file_list:
        with open(path + file, "w") as f:
            f.write("")


async def get_soup(page: Page, value: str) -> BeautifulSoup | None:
    e = await page.query_selector(value)
    if e is None:
        return None
    html = await e.inner_html()
    soup = BeautifulSoup(html, "html.parser")
    return soup


async def get_soup_all(page: Page, value: str) -> List[BeautifulSoup]:
    await asyncio.sleep(2)
    e_list = await page.query_selector_all(value)
    if len(e_list) == 0:
        return []
    soup_list = [BeautifulSoup(await e.inner_html(), "html.parser") for e in e_list]
    return soup_list


async def _save_temp_files(file_name: str, data: Union[List, Dict]):
    path = config["KREAM_DETAILS_TEMP_DIR"]
    assert path, "Env KREAM_DETAILS_TEMP_DIR does not exist"

    n = f"{file_name}.json"
    async with aiofiles.open(path + n, "a") as f:
        await f.write(json.dumps(data, ensure_ascii=False, default=str) + ",")
    return True


async def save_scrap_files(brand_name: str):
    path = f"router/dev/kream/data/detail/{brand_name}/"

    temp_path = config["KREAM_DETAILS_TEMP_DIR"]
    assert temp_path, "Env KREAM_DETAILS_TEMP_DIR does not exist"

    file_time = datetime.now().strftime("%y%m%d-%H%M%S")

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    ######################## product_detail
    temp_file_name = f"product_detail.json"
    async with aiofiles.open(temp_path + temp_file_name, "r", encoding="utf-8") as f:
        v = await f.read()
        x = eval(v)

    iter_df = pd.DataFrame(x)
    df = pd.DataFrame([KreamProductDetailSchema(**row).model_dump() for row in iter_df.to_dict("records")])  # type: ignore

    file_name = f"{file_time}-product_detail.parquet.gzip"
    df.to_parquet(path + file_name, compression="gzip")

    ######################## trading_volume
    temp_file_name = f"trading_volume.json"
    async with aiofiles.open(temp_path + temp_file_name, "r", encoding="utf-8") as f:
        v = await f.read()
        v = v.replace("false", "False").replace("true", "True")
        x = eval(v)

    iter_df = pd.DataFrame(list(chain(*x)))
    df = pd.DataFrame([KreamTradingVolumeSchema(**row).model_dump() for row in iter_df.to_dict("records")])  # type: ignore

    file_name = f"{file_time}-trading_volume.parquet.gzip"
    df.to_parquet(path + file_name, compression="gzip")

    ######################## buy_and_sell
    temp_file_name = f"buy_and_sell.json"
    async with aiofiles.open(temp_path + temp_file_name, "r", encoding="utf-8") as f:
        v = await f.read()
        x = eval(v)

    df_list = [pd.DataFrame(i) for i in x]
    df = pd.concat(df_list)

    # filter
    df = df[(df["sell"] != 0) | (df["buy"] != 0)]

    # columns
    df = df.reset_index()
    df = df.rename(columns={"index": "kream_product_size"})
    df["updated_at"] = datetime.now().replace(microsecond=0)

    df = pd.DataFrame([KreamBuyAndSellSchema(**row).model_dump() for row in df.to_dict("records")])  # type: ignore

    file_name = f"{file_time}-buy_and_sell.parquet.gzip"
    df.to_parquet(path + file_name, compression="gzip")
    return file_time + "-" + brand_name
