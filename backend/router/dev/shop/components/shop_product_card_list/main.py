import os
import json
import asyncio
from itertools import chain
from datetime import datetime
from typing import Dict, List, Callable
from traceback import format_exception

import pandas as pd
import aiofiles
from dotenv import dotenv_values

from model.db_model_shop import ShopProductCardSchema
from ..shop_list import *
from playwright.async_api import Page
from ....custom_playwright.page import customPage
from ..currency import Currency
from .create_log import create_last_update_shop_detail_log

currency = Currency()


# TODO: brand_url 변수 없애고 brand_url용 dict 만들기


config = dotenv_values(".env.dev")

shop_product_list_dict = {
    "consortium": get_consortium_list,
    "a_few_store": get_a_few_store_list,
    "seven_store": get_seven_store_list,
}


def get_shop_product_list():
    return list(shop_product_list_dict.keys())


async def scrap_shop_product_card_main(
    custom_page: customPage, shop_name: str, brand_name: str, num_process: int
):
    path = config.get("SHOP_PRODUCT_LIST_DIR")
    assert path, "SHOP_PRODUCT_LIST_DIR is None"

    none_init_error = "page가 None입니다. init 메서드를 먼저 실행해주세요."
    none_context_error = "context가 None입니다. init 메서드를 먼저 실행해주세요."

    assert custom_page.init_page, none_init_error
    assert custom_page.context, none_context_error

    init_tempfiles()

    n_p = num_process - 1
    p_list = [await custom_page.context.new_page() for _ in range(n_p)]
    p_list.append(custom_page.init_page)

    b_list = brand_name.split(",")
    print(f"scrap len : {len(b_list)}")

    scrap_callback = shop_product_list_dict.get(shop_name)
    assert scrap_callback, f"{shop_name} is None"

    split_b_list = split_size(b_list, num_process)
    co_list = [
        scrap_shop_product_sub_process(
            p_list[i], split_b_list[i], shop_name, scrap_callback
        )
        for i in range(num_process)
    ]
    result = await asyncio.gather(*co_list)
    merged_result = {k: v.replace("=", "") for d in result for k, v in d.items()}

    path = config["SHOP_PRODUCT_LIST_DIR"]
    assert path, "Env SHOP_PRODUCT_LIST_DIR does not exist"
    temp_path = path + "_temp/"

    with open(temp_path + "process_result.json", "w") as f:
        meta = {
            "num_process": num_process,
            "brand_list": b_list,
            "scrap_result": merged_result,
            "db_update": False,
        }
        f.write(json.dumps(meta, ensure_ascii=False))

    scrap_name = None
    try:
        shop_name, file_time = await save_scrap_result_to_parquet(shop_name)
        create_last_update_shop_detail_log(shop_name, file_time)
        scrap_name = f"{file_time}-{shop_name}"

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


async def scrap_shop_product_sub_process(
    page: Page, brand_list: List, shop_name: str, shop_callback: Callable
):
    lst = {k: "not_scrap" for k in brand_list}

    for brand_name in brand_list:
        brand_url = load_brand_url(shop_name, brand_name)
        for i in range(3):
            try:
                scrap_data = await shop_callback(page, brand_name, brand_url)
                await _save_temp_files("product_card_list", scrap_data)
                lst[brand_name] = "success"
                break
            except Exception as e:
                print(f"scrap_error: {shop_name}-{brand_name}-{i+1} 실패")
                print("".join(format_exception(None, e, e.__traceback__)))
                if i == 2:
                    lst[brand_name] = str(e)
                continue

    await page.close()
    return lst


def load_brand_url(shop_name: str, brand_name: str):
    brand_dict = _load_brand(shop_name)

    data = brand_dict.get("data")
    assert isinstance(data, list), f"{shop_name}'s data is None"

    df = pd.DataFrame(data)

    df = df[df["brand_name"] == brand_name]

    return df["brand_url"].tolist()[0]


def load_brand_name(shop_name: str) -> List:
    brand_dict = _load_brand(shop_name)
    brand_list = brand_dict.get("brand_list")
    assert isinstance(brand_list, list), f"{shop_name}'s brand_list is None"
    return brand_list


def _load_brand(shop_name: str) -> Dict:
    path = config.get("SHOP_LIST_DIR")
    assert path, "SHOP_LIST_DIR is None"
    file_path = f"{path+shop_name}/brand_list.json"

    # TODO: shop 별 브랜드 리스트를 만들어야함.
    with open(file_path, "r") as f:
        brand_dict = json.load(f)
    return brand_dict


def _save_to_parquet(shop_name: str, scrap_data: list[ShopProductCardSchema]):
    path = config.get("SHOP_PRODUCT_LIST_DIR")
    assert path, "SHOP_PRODUCT_LIST_DIR is None"

    file_time = datetime.now().strftime("%y%m%d-%H%M%S")
    file_path = f"{path+shop_name}/{file_time}.parquet.gzip"

    if not os.path.exists(path + shop_name):
        os.makedirs(path + shop_name, exist_ok=True)

    raw_data = [row.model_dump() for row in scrap_data]
    pd.DataFrame(raw_data).drop_duplicates().to_parquet(
        path=file_path, compression="gzip"
    )
    return shop_name, file_time


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


def preprocess_data(cards_info: List[Dict]) -> List[ShopProductCardSchema]:
    # currency

    lst = []
    for card in cards_info:
        original_price: str = card.get("original_price", None)

        if original_price is None:
            raise ValueError("original_price is None")

        _, curr_name, origin_price = currency.get_price_info(original_price)

        (_, _, us_price) = currency.change_currency_to_custom_usd(original_price)

        (_, _, kor_price) = currency.change_currency_to_buying_won(original_price)

        card["original_price_currency"] = curr_name
        card["original_price"] = origin_price
        card["us_price"] = us_price
        card["kor_price"] = int(round(kor_price, -3))
        card["updated_at"] = datetime.now().replace(microsecond=0)
        lst.append(ShopProductCardSchema(**card))

    return lst


async def _save_temp_files(file_name: str, data: List | Dict):
    path = config["SHOP_PRODUCT_LIST_DIR"]
    assert path, "SHOP_PRODUCT_LIST_DIR is not defined in .env"
    temp_path = path + "_temp/"

    n = f"{file_name}.json"
    async with aiofiles.open(temp_path + n, "a") as f:
        await f.write(json.dumps(data, ensure_ascii=False, default=str) + ",")
    return True


async def save_scrap_result_to_parquet(shop_name):
    path = config["SHOP_PRODUCT_LIST_DIR"]
    assert path, "SHOP_PRODUCT_LIST_DIR is not defined in .env"
    temp_path = path + "_temp/"

    async with aiofiles.open(
        temp_path + "product_card_list.json", "r", encoding="utf-8"
    ) as f:
        v = await f.read()
        v = v.replace("null", "None").replace("true", "True").replace("false", "False")
        v = eval(v)
        raw_data = list(chain(*v))

    scrap_data = preprocess_data(raw_data)
    return _save_to_parquet(shop_name, scrap_data)


def init_tempfiles():
    path = config["SHOP_PRODUCT_LIST_DIR"]
    assert path, "SHOP_PRODUCT_LIST_DIR is not defined in .env"
    temp_path = path + "_temp/"

    file_list = os.listdir(temp_path)
    for file in file_list:
        with open(temp_path + file, "w") as f:
            f.write("")
