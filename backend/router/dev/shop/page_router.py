"""shop Router"""
import os
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from dotenv import dotenv_values

from db.dev_db import get_dev_db
from .components.update_to_db import get_shop_name_from_db
from ..custom_playwright.page import customPage
from ..custom_playwright.access_page import get_custom_page

from .components.shop_product_card_page.main import scrap_shop_product_page_main
from .components.shop_product_card_page.access_db import get_track_size_list
from .components.shop_product_card_page.create_log import get_product_page_result


page_router = APIRouter()

config = dotenv_values(".env.dev")

page_dict = {}


@page_router.get("/init-shop-product-card-page")
async def scrap_shop_product_card_page(
    searchType: str,
    numProcess: int,
    content: str,
    custom_page: customPage = Depends(get_custom_page),
):
    """shop product card page scrap"""

    result = await scrap_shop_product_page_main(
        custom_page, searchType, content, numProcess
    )

    return result


@page_router.get("/test")
async def test(searchType: str, content: str):
    return await get_track_size_list(searchType, content)


@page_router.get("/get-product-page-result")
def get_product_page_result_api(scrapName: str):
    """scrap 결과 조회"""

    return get_product_page_result(scrapName)


@page_router.get("/get-scrap-page-list")
def get_shop_scrap_page():
    """scrap 결과 조회"""

    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    result_path = path + "_scrap-result/"

    file_list = os.listdir(result_path)
    file_list = [x.split(".json")[0] for x in file_list]
    file_list.sort(reverse=True)
    return file_list
