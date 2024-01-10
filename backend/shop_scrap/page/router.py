from fastapi import APIRouter
from shop_scrap.page.main import ShopPageMain
from components.env import get_path
from db.dev_db import session_local

# /api/shop/list/
shop_page = APIRouter()

ShopPage = ShopPageMain(get_path("shop_page"), session_local)


@shop_page.get("scrap")
async def scrap(searchType: str, value: str, numProcess: int):
    report_name = await ShopPage.execute(searchType, value, numProcess)
    return {"scrap_status": "success", "report_name": report_name}
