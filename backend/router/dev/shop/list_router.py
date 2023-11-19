"""shop Router"""
import os
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from dotenv import dotenv_values

from db.dev_db import get_dev_db
from .components.update_to_db import get_shop_name_from_db
from ..custom_playwright.page import customPage
from ..custom_playwright.access_page import get_custom_page, close_custom_page

from .components.shop_product_card_list import (
    load_brand_name,
    scrap_shop_product_card_main,
)
from .components.shop_product_card_list.create_log import get_scrap_result

from .components.update_to_db import (
    get_shop_info_by_name,
    get_shop_product_list,
    load_scraped_brand_name,
    get_shop_product_list_for_cost_table,
    get_currency_from_local,
)

list_router = APIRouter()

config = dotenv_values(".env.dev")


@list_router.get("/close-custom-page")
async def close_custom_page_api():
    return await close_custom_page()


@list_router.get("/get-brand-name")
def get_brand_name(shopName: str):
    return load_brand_name(shopName)


@list_router.get("/get-scraped-brand-name")
async def get_scraped_brand_name(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    return await load_scraped_brand_name(db, shopName)


@list_router.get("/get-shop-name")
async def get_shop_name(db: AsyncSession = Depends(get_dev_db)):
    return await get_shop_name_from_db(db)


@list_router.get("/init-shop-product-card-list")
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


@list_router.get("/get-scrap-list")
def get_shop_scrap_list():
    """scrap 결과 조회"""

    path = config["SHOP_PRODUCT_LIST_DIR"]
    assert path, "SHOP_PRODUCT_LIST_DIR is not defined in .env"
    result_path = path + "_scrap-result/"

    file_list = os.listdir(result_path)
    file_list = [x.split(".json")[0] for x in file_list]
    file_list.sort(reverse=True)
    return file_list


@list_router.get("/get-product-list-result")
def get_product_list_result_api(scrapName: str):
    """scrap 결과 조회"""

    return get_scrap_result(scrapName)


@list_router.get("/get-shop-product-list")
async def get_shop_product_list_api(
    shopName: str, brandName: str, db: AsyncSession = Depends(get_dev_db)
):
    """shop product list 조회"""

    return await get_shop_product_list(db, shopName, brandName)


@list_router.get("/get-shop-product-list-for-cost-table")
async def get_shop_product_list_for_cost_table_api(
    searchType: str, value: str, db: AsyncSession = Depends(get_dev_db)
):
    """shop product list 조회"""

    return await get_shop_product_list_for_cost_table(db, searchType, value)


@list_router.get("/get-shop-info")
async def get_shop_info_api(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    """shop product list 조회"""

    return await get_shop_info_by_name(db, shopName)


@list_router.get("/get-buying-currency")
def get_buying_currency():
    """구매 환율 조회"""
    return get_currency_from_local()
