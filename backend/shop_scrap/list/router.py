from fastapi import APIRouter
from shop_scrap.list.main import ShopListMain
from components.env import get_path

# /api/shop/list/
shop_list = APIRouter()

ShopList = ShopListMain(get_path("shop_list"))


@shop_list.get("/scrap")
async def scrap(shopName: str, brandName: str, numProcess: int):
    target_list = brandName.split(",")
    report_name = await ShopList.execute(shopName, target_list, numProcess)
    return {"scrap_status": "success", "report_name": report_name}


@shop_list.post("/sync_db/{scrap_time}")
async def sync_db(scrap_time: str):
    return await ShopList.sync(scrap_time)


@shop_list.get("/sub_scraper_list")
def sub_scraper_list():
    return ShopList.main_scraper_factory.pw_sub_scraper_list()


@shop_list.get("/sub_scraper_brand/{shop_name}")
def sub_scraper_brand(shop_name: str):
    return ShopList.main_scraper_factory.pw_sub_scraper_brand(shop_name)


@shop_list.get("/report/list")
def report_list():
    return ShopList.Report.get_report_list()


@shop_list.get("/report/item/{name}")
def report_item(name: str):
    ShopList.Report.report_file_name = name
    return ShopList.Report.get_report()
