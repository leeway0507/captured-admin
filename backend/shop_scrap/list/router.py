from fastapi import APIRouter
from shop_scrap.list.main import ShopListMain
from components.env import get_path

# /api/shop/list/
shop_list = APIRouter()

ShopList = ShopListMain(get_path("shop_list"))


@shop_list.get("scrap")
async def scrap(shopName: str, brandName: str, numProcess: int):
    target_list = brandName.split(",")
    report_name = await ShopList.execute(shopName, target_list, numProcess)
    return {"scrap_status": "success", "report_name": report_name}
