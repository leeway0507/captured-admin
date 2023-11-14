"""shop Router"""
import os
import json
from typing import Optional
from urllib.parse import unquote

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from dotenv import dotenv_values

from db.dev_db import get_dev_db
from .components.update_to_db import get_shop_name_from_db
from ..kream.components.main import customPage
from .components.shop_product_card_list import (
    load_brand_name,
    scrap_shop_product_card_main,
)
from .components.update_to_db import (
    get_shop_info_by_name,
    get_shop_product_list,
    load_scraped_brand_name,
    get_shop_product_list_for_cost_table,
)
from .components.shop_product_card_list.create_log import get_scrap_result

shop_router = APIRouter()

config = dotenv_values(".env.dev")

page_dict = {}


async def get_custom_page():
    """kream page 로드"""
    print("""kream page 로드""")
    if page_dict.get("custom_page") is None:
        custom_page = customPage()
        await custom_page.init()
        page_dict.update({"custom_page": custom_page})

    return page_dict.get("custom_page")


@shop_router.get("/get-brand-name")
def get_brand_name(shopName: str):
    return load_brand_name(shopName)


@shop_router.get("/get-scraped-brand-name")
async def get_scraped_brand_name(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    return await load_scraped_brand_name(db, shopName)


@shop_router.get("/get-shop-name")
async def get_shop_name(db: AsyncSession = Depends(get_dev_db)):
    return await get_shop_name_from_db(db)


@shop_router.get("/init-shop-product-card-list")
async def scrap_shop_product_card_list(
    shopName: str,
    brandName: str,
    numProcess: int,
    custom_page: customPage = Depends(get_custom_page),
):
    result = await scrap_shop_product_card_main(
        custom_page, shopName, brandName, numProcess
    )

    return result


@shop_router.get("/get-scrap-list")
def get_shop_scrap_list():
    """scrap 결과 조회"""

    file_list = os.listdir(config["SHOP_SCRAP_RESULT_DIR"])
    file_list = [x.split(".json")[0] for x in file_list]
    file_list.sort(reverse=True)
    return file_list


@shop_router.get("/get-scrap-data")
def get_scrap_data(scrapName: str):
    """scrap 결과 조회"""

    return get_scrap_result(scrapName)


@shop_router.get("/get-shop-product-list")
async def get_shop_product_list_api(
    shopName: str, brandName: str, db: AsyncSession = Depends(get_dev_db)
):
    """shop product list 조회"""

    print(shopName, brandName)

    return await get_shop_product_list(db, shopName, brandName)


@shop_router.get("/get-shop-product-list-for-cost-table")
async def get_shop_product_list_for_cost_table_api(
    searchType: str, value: str, db: AsyncSession = Depends(get_dev_db)
):
    """shop product list 조회"""

    return await get_shop_product_list_for_cost_table(db, searchType, value)


@shop_router.get("/get-shop-info")
async def get_shop_info_api(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    """shop product list 조회"""

    return await get_shop_info_by_name(db, shopName)


@shop_router.get("/get-buying-currency")
def get_buying_currency():
    """구매 환율 조회"""
    path = "router/dev/shop/components/currency/data/buying_currency.json"
    with open(path, "r") as f:
        data = json.load(f)

    return data
