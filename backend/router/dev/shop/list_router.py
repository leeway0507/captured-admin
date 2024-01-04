"""shop Router"""
import os
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException


from db.dev_db import get_dev_db
from components.dev.utils.browser_controller import PwBrowserController
from components.dev.utils.scrap_report import ScrapReport

from components.dev.shop.update_to_db import get_shop_name_from_db
from components.dev.shop.list import ShopListMain
from backend.components.dev.shop.list.sub_scraper_factory import (
    PwShopListModuleFactory,
)
from components.dev.shop.scrapable_list import (
    get_scrapable_list_module_list,
    get_brand_name,
)


from components.dev.shop.update_to_db import (
    get_shop_info_by_name,
    get_shop_product_list,
    load_scraped_brand_name,
    get_shop_product_list_for_cost_table,
    get_currency_from_local,
)

list_router = APIRouter()

scrap_report = ScrapReport("shop_list")


@list_router.get("/get-brand-name")
def get_brand_name_api(shopName: str):
    return get_brand_name(shopName)


@list_router.get("/get-scraped-brand-name")
async def get_scraped_brand_name(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    return await load_scraped_brand_name(db, shopName)


@list_router.get("/get-shop-name")
def get_shop_name():
    return get_scrapable_list_module_list()


@list_router.get("/init-shop-product-card-list")
async def scrap_shop_product_card_list(
    shopName: str,
    brandName: str,
    numProcess: int,
):
    scraper_type = "playwright"

    if scraper_type == "playwright":
        module_factory = PwShopListModuleFactory()
        browser_controller = PwBrowserController()

    else:
        # TODO: selenium 추가하면 selenium으로 변경하기
        module_factory = PwShopListModuleFactory()
        browser_controller = PwBrowserController()
    browser_controller = await browser_controller.create()
    ListMain = ShopListMain(numProcess, browser_controller, module_factory, shopName)

    result = await ListMain.main(brandName)

    return result


@list_router.get("/get-scrap-list")
def get_shop_scrap_list():
    """scrap 목록 조회"""
    return scrap_report.get_report_list()


@list_router.get("/get-product-list-result")
def get_product_list_result_api(scrapName: str):
    """scrap 결과 조회"""
    return scrap_report.get_report(scrapName)


@list_router.delete("/delete-product-list-result")
def delete_product_list_result_api(scrapName: str):
    """scrap 결과 삭제"""
    return scrap_report.delete_report(scrapName)


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
    value = value.replace("c%27", "'")

    return await get_shop_product_list_for_cost_table(db, searchType, value)


@list_router.get("/get-shop-info")
async def get_shop_info_api(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    """shop product list 조회"""

    return await get_shop_info_by_name(db, shopName)


@list_router.get("/get-buying-currency")
def get_buying_currency():
    """구매 환율 조회"""
    return get_currency_from_local()
