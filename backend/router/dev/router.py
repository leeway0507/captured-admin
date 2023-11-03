"""dev Router"""
import asyncio
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from model.db_model_production import ProductInfoSchema, ProductInfoDBSchema

from db.dev_db import get_dev_db
from .kream import *

kream_router = APIRouter()

kream_dict = {}


async def get_kream_page():
    """kream page 로드"""
    print("""kream page 로드""")
    if kream_dict.get("kream_page") is None:
        kream_page = KreamPage()
        await kream_page.init()
        kream_dict.update({"kream_page": kream_page})

    return kream_dict.get("kream_page")


@kream_router.get("/reload-kream-page")
async def reload_kream_page():
    """kream page 리로드"""

    if kream_dict.get("kream_page"):
        b = kream_dict.get("kream_page")
        assert isinstance(b, KreamPage), "kream_page is not KreamPage"
        assert b.browser, "browser is not exist"
        await b.close_browser() # type: ignore
        kream_dict.pop("kream_page")

    await get_kream_page()
    return {"result": "success"}
    

@kream_router.get("/init-product-detail")
async def init_product_detail(
    brandName: str,
    numProcess: int,
    kreamIds: Optional[str] = None,
    kream_page: KreamPage = Depends(get_kream_page),
):
    """scrap product_detal """

    # login
    await kream_page.login()

    result = await scrap_product_detail_main(kream_page, brandName, kreamIds, numProcess)

    return result


@kream_router.get("/init-product-card-list")
async def init_scraping_brand(
    brandName: str, maxScroll: int, minWish: int, minVolume: int, kream_page=Depends(get_kream_page)
):
    """order_history 조회"""
    error_log = {}
    page = kream_page.login()
    try:
        await scrap_product_card_list(page, brandName, maxScroll, minWish, minVolume)
    except Exception:
        raise HTTPException(status_code=500, detail="kream scrap error")
    return {"result": "success"}



@kream_router.get("/check-kream-product-card")
def get_kream_product_card_data(brand: str):
    """kream_product_card_table 업데이트 전 조회"""
    return get_kream_product_card(brand)

@kream_router.get("/check-kream-trading-volume")
def get_kream_trading_volume_data(brand: str):
    """kream_trading_volume_table 업데이트 전 조회"""
    return get_kream_trading_volume(brand)

@kream_router.get("/check-kream-buy-and-sell")
def get_kream_buy_and_sell_data(brand:str):
    """kream_buy_and_sell_table 업데이트 전 조회"""
    return get_kream_buy_and_sell(brand)

@kream_router.get("/check-kream-product-bridge")
def get_kream_product_bridge_data(brand:str):
    """kream_product_bridge_table 업데이트 전 조회"""
    return get_kream_product_bridge(brand)

@kream_router.get("/update-scrap-files")
async def update_scrap_files(brand:str):
    """scrap 파일 업데이트"""
    return await save_scrap_files(brand)
