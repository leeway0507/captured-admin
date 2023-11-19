from lib2to3.pytree import convert
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
from ..size_converter import convert_size

from .access_db import get_track_size_list
from .create_log import create_last_update_shop_detail_log


config = dotenv_values(".env.dev")

shop_product_page_dict = {
    "consortium": get_consortium_page,
    # "a_few_store": get_a_few_store_page,
    # "seven_store": get_seven_store_page,
}


def get_shop_product_page():
    return list(shop_product_page_dict.keys())


async def scrap_shop_product_page_main(
    custom_page: customPage, searchType: str, content: str, num_process: int
):
    none_init_error = "page가 None입니다. init 메서드를 먼저 실행해주세요."
    none_context_error = "context가 None입니다. init 메서드를 먼저 실행해주세요."

    assert custom_page.init_page, none_init_error
    assert custom_page.context, none_context_error

    init_tempfiles()

    n_p = num_process - 1
    p_list = [await custom_page.context.new_page() for _ in range(n_p)]
    p_list.append(custom_page.init_page)

    track_list = await get_track_size_list(searchType, content)
    if track_list == []:
        raise ValueError(f"track_list is Empty : {track_list}")

    split_b_list = split_size(track_list, num_process)
    co_list = [
        scrap_shop_product_page_sub_process(p_list[i], split_b_list[i])
        for i in range(num_process)
    ]
    result = await asyncio.gather(*co_list)
    merged_result = list(chain(*result))

    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    temp_path = path + "_temp/"

    with open(temp_path + "scrap_page_result.json", "w") as f:
        meta = {
            "num_of_plan": len(track_list),
            "num_process": num_process,
            "scrap_result": merged_result,
            "db_update": False,
        }
        f.write(json.dumps(meta, ensure_ascii=False))

    scrap_name = None
    try:
        file_time = await save_scrap_result_to_parquet()
        create_last_update_shop_detail_log(file_time)
        scrap_name = f"{file_time}"

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


async def scrap_shop_product_page_sub_process(
    page: Page, page_list: List[ShopProductCardSchema]
) -> list[Dict]:
    lst = []

    for page_info in page_list:
        url = page_info.product_url
        shop_name = page_info.shop_name
        brand_name = page_info.brand_name
        shop_product_card_id = page_info.shop_product_card_id

        page_callback = shop_product_page_dict.get(shop_name)
        assert page_callback, f"{shop_name} does not exist in shop_product_page_dict"

        for i in range(3):
            try:
                scrap_data = await page_callback(page, shop_name, url)

                preprocessed_data = []
                for data in scrap_data["size_info"]:
                    data["shop_product_card_id"] = shop_product_card_id
                    data["updated_at"] = datetime.now().replace(microsecond=0)
                    data["available"] = True
                    data["kor_product_size"] = convert_size(data["kor_product_size"])
                    data["product_id"] = scrap_data["product_id"]
                    preprocessed_data.append(data)

                await _save_temp_files("product_card_page", preprocessed_data)
                lst.append(
                    {
                        "shop_product_card_id": shop_product_card_id,
                        "shop_name": shop_name,
                        "brand_name": brand_name,
                        "url": url,
                        "product_id": page_info.product_id,
                        "status": "success",
                    }
                )
                break
            except Exception as e:
                print(f"scrap_error: {shop_name}-{brand_name}-{i+1} 실패")
                print("".join(format_exception(None, e, e.__traceback__)))
                if i == 2:
                    lst.append(
                        {
                            "shop_product_card_id": shop_product_card_id,
                            "shop_name": shop_name,
                            "brand_name": brand_name,
                            "url": url,
                            "status": str(e),
                        }
                    )
                continue

    await page.close()
    return lst


def _save_to_parquet(scrap_data: list[Dict]):
    path = config.get("SHOP_PRODUCT_PAGE_DIR")
    assert path, "SHOP_PRODUCT_PAGE_DIR is None"

    file_time = datetime.now().strftime("%y%m%d-%H%M%S")
    file_path = f"{path}/{file_time}.parquet.gzip"

    pd.DataFrame(scrap_data).drop_duplicates().to_parquet(
        path=file_path, compression="gzip"
    )
    return file_time


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


async def _save_temp_files(file_name: str, data: List | Dict):
    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    temp_path = path + "_temp/"

    n = f"{file_name}.json"
    async with aiofiles.open(temp_path + n, "a") as f:
        await f.write(json.dumps(data, ensure_ascii=False, default=str) + ",")
    return True


async def save_scrap_result_to_parquet():
    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    temp_path = path + "_temp/"

    async with aiofiles.open(
        temp_path + "product_card_page.json", "r", encoding="utf-8"
    ) as f:
        v = await f.read()
        v = v.replace("null", "None").replace("true", "True").replace("false", "False")
        v = eval(v)
        raw_data = list(chain(*v))

    return _save_to_parquet(raw_data)


def init_tempfiles():
    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    temp_path = path + "_temp/"

    file_list = os.listdir(temp_path)
    for file in file_list:
        with open(temp_path + file, "w") as f:
            f.write("")
