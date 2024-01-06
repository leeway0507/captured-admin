"""shop Router"""
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends


from db.dev_db import get_dev_db
from env import get_path
from components.dev.shop.scrapable_list import (
    get_scrapable_list_module_list,
    get_scrapable_page_module_list,
    get_brand_name,
)


from components.dev.shop.page import ShopPageScraper
from components.dev.shop.page.candidate_extractor import RDBCandidateExtractor
from components.dev.shop.page.sub_scraper_factory import (
    PwShopPageSubScraperFactory,
)
from components.dev.shop.list import ShopListScraper
from components.dev.shop.list.sub_scraper_factory import (
    PwShopListSubScraperFactory,
)
from components.dev.utils.browser_controller import (
    PwBrowserController,
)
from components.dev.utils import ScrapReport


from components.dev.shop.update_to_db import (
    get_shop_info_by_name,
    get_shop_product_list,
    load_scraped_brand_name,
    get_shop_product_list_for_cost_table,
    get_currency_from_local,
)

shop_router = APIRouter()

platform_list_path = get_path("platform_list")
platform_page_path = get_path("platform_page")


platform_list_report = ScrapReport(platform_list_path)
platform_page_report = ScrapReport(platform_page_path)


list_scraper = ShopListScraper(platform_list_path)
page_scraper = ShopPageScraper(platform_page_path)


@shop_router.get("/scrap-shop-list")
async def scrap_product_list(
    shop_name: str,
    brand_name: str,
    numProcess: int,
):
    """shop list 수집"""
    browser = await PwBrowserController.start()
    sub_scraper = getattr(PwShopListSubScraperFactory(), shop_name)()
    list_scraper.late_binding(browser, sub_scraper, numProcess, "kream")
    list_scraper.target_list = brand_name.split(",")

    return await list_scraper.scrap()


@shop_router.get("/scrap-shop-page")
async def scrap_product_page(
    shop_name: str,
    searchType: Literal["all", "productId", "shopProductCardId", "shopName"],
    value: str,
    numProcess: int,
):
    """shop list 수집"""
    browser = await PwBrowserController.start()
    sub_scraper = getattr(PwShopPageSubScraperFactory(), shop_name)()
    page_scraper.late_binding(browser, sub_scraper, numProcess, "kream")
    page_scraper.target_list = await RDBCandidateExtractor.extract_data(
        searchType, value
    )

    return await page_scraper.scrap()


@shop_router.get("/get-brand-name")
def get_brand_name_api(shopName: str):
    return get_brand_name(shopName)


@shop_router.get("/get-scraped-brand-name")
async def get_scraped_brand_name(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    return await load_scraped_brand_name(db, shopName)


@shop_router.get("/get-shop-name")
def get_shop_name():
    return get_scrapable_list_module_list()


@shop_router.get("/get-report-list")
def get_shop_report_list():
    """scrap 목록 조회"""
    return platform_list_report.get_report_list()


@shop_router.get("/get-shop-list-result")
def get_shop_list_report(scrapName: str):
    """scrap 결과 조회"""
    platform_list_report.report_file_name = scrapName
    return platform_list_report.load_report()


@shop_router.delete("/delete-shop-list-result")
def delete_product_list_result_api(scrapName: str):
    """scrap 결과 삭제"""
    platform_list_report.report_file_name = scrapName
    return platform_list_report.delete_report()


@shop_router.get("/get-shop-shop-list")
async def get_shop_product_list_api(
    shopName: str, brandName: str, db: AsyncSession = Depends(get_dev_db)
):
    """shop list 조회"""

    return await get_shop_product_list(db, shopName, brandName)


@shop_router.get("/get-shop-product-list-for-cost-table")
async def get_shop_product_list_for_cost_table_api(
    searchType: str, value: str, db: AsyncSession = Depends(get_dev_db)
):
    """shop product list 조회"""
    value = value.replace("c%27", "'")

    return await get_shop_product_list_for_cost_table(db, searchType, value)


@shop_router.get("/get-shop-info")
async def get_shop_info_api(shopName: str, db: AsyncSession = Depends(get_dev_db)):
    """shop product list 조회"""

    return await get_shop_info_by_name(db, shopName.split(","))


@shop_router.get("/get-buying-currency")
def get_buying_currency():
    """구매 환율 조회"""
    return get_currency_from_local()


@shop_router.get("/get-shop-product-page")
def get_scrapable_shop_list_api():
    return get_scrapable_page_module_list()


@shop_router.get("/get-product-page-result")
def get_product_page_result_api(scrapName: str):
    """scrap 결과 조회"""

    platform_list_report.report_file_name = scrapName
    return platform_page_report.delete_report()


@shop_router.get("/get-scrap-page-list")
def get_shop_scrap_page():
    """scrap 결과 조회"""
    return platform_page_report.get_report_list()
