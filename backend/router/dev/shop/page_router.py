"""shop Router"""
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from db.dev_db import get_dev_db
from ..utils.browser_controller import PwBrowserController

from .components.shop_product_card_page import ShopPageMain
from .components.shop_product_card_page.candidate_extractor import (
    RDBCandidateExtractor as RDB_Extractor,
)

from .components.scrapable_list import get_scrapable_page_module_list
from .components.shop_product_card_page.page_module_factory import (
    PwShopPageModuleFactory,
)
from ..utils.scrap_report import ScrapReport


page_router = APIRouter()

scrap_report = ScrapReport("shop_page")


@page_router.get("/init-shop-product-card-page")
async def scrap_shop_product_card_page(
    searchType: str,
    numProcess: int,
    content: str,
    db: AsyncSession = Depends(get_dev_db),
):
    """shop product card page scrap"""

    scraper_type = "playwright"

    if scraper_type == "playwright":
        module_factory = PwShopPageModuleFactory()
        browser_controller = await PwBrowserController.create()

    else:
        # TODO: selenium 추가하면 selenium으로 변경하기
        module_factory = PwShopPageModuleFactory()
        browser_controller = await PwBrowserController.create()

    extractor = RDB_Extractor()
    PageMain = ShopPageMain(numProcess, browser_controller, module_factory, extractor)

    result = await PageMain.main(search_type=searchType, value=content)

    return result


# @page_router.get("/test")
# async def test(searchType: str, content: str):
#     return await get_track_size_list(searchType, content)


# @page_router.get("/test2")
# async def test2():
#     raw_data = await load_product_card_page_json()
#     size_schema = [ShopProductSizeSchema(**row).model_dump() for row in raw_data]

#     product_id_Schema = {}
#     for row in raw_data:
#         key = row["shop_product_card_id"]
#         value = row["product_id"]
#         if value not in product_id_Schema.values():
#             product_id_Schema[key] = value

#     product_id_Schema_list = [
#         {
#             "shop_product_card_id": k,
#             "product_id": v,
#         }
#         for k, v in product_id_Schema.items()
#     ]

#     return {"a": size_schema, "b": product_id_Schema_list}


@page_router.get("/get-shop-product-page")
def get_scrapable_shop_list_api():
    return get_scrapable_page_module_list()


@page_router.get("/get-product-page-result")
def get_product_page_result_api(scrapName: str):
    """scrap 결과 조회"""

    return scrap_report.get_report(scrapName)


@page_router.get("/get-scrap-page-list")
def get_shop_scrap_page():
    """scrap 결과 조회"""
    return scrap_report.get_report_list()
