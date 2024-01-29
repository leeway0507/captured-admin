from typing import Dict
from fastapi import APIRouter
from shop_scrap.page.main import ShopPageMain
from components.env import get_path
from db.dev_db import admin_session_local

# /api/shop/page/
shop_page = APIRouter()

ShopPage = ShopPageMain(get_path("shop_page"), admin_session_local)


@shop_page.get("/scrap")
async def scrap(searchType: str, value: str, numProcess: int):
    report_name = await ShopPage.execute(searchType, value, numProcess)
    return {"scrap_status": "success", "report_name": report_name}


@shop_page.post("/sync_db/{scrap_time}")
async def sync_db(scrap_time: str):
    return await ShopPage.sync(scrap_time)


@shop_page.get("/sub_scraper_list")
def sub_scraper_list():
    return ShopPage.main_scraper_factory.pw_sub_scraper_list()


@shop_page.get("/sub_scraper_brand/{shop_name}")
def sub_scraper_brand(shop_name: str):
    return ShopPage.main_scraper_factory.pw_sub_scraper_brand(shop_name)


@shop_page.get("/report/list")
def report_list():
    return ShopPage.Report.get_report_list()


@shop_page.get("/report/item/{name}")
def report_item(name: str):
    ShopPage.Report.report_file_name = name
    return ShopPage.Report.get_report()
