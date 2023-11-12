"""dev Router"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from dotenv import dotenv_values

from db.dev_db import get_dev_db

from .components.scrap_product_card_list import *
from .components.update_to_db import (
    update_scrap_product_card_list_to_db,
    update_scrap_product_card_detail_to_db,
    update_scrap_trading_volume_to_db,
    update_scrap_buy_and_sell_to_db,
    update_scrap_kream_product_bridge_to_db,
)
from .components.create_log import update_scrap_result

kream_db_router = APIRouter()

kream_dict = {}

config = dotenv_values(".env.dev")


@kream_db_router.get("/update-all-detail-kream-to-db")
async def updat_all(
    scrapName: str,
    db: AsyncSession = Depends(get_dev_db),
):
    detail_scrap_date, brand = scrapName.rsplit("-", 1)

    await update_scrap_product_card_detail_to_db(db, brand, detail_scrap_date)
    await update_scrap_trading_volume_to_db(db, brand, detail_scrap_date)
    await update_scrap_buy_and_sell_to_db(db, brand, detail_scrap_date)
    await update_scrap_kream_product_bridge_to_db(db, brand, detail_scrap_date)

    update_scrap_result(scrapName, "db_update", True)

    return {"message": "success"}


@kream_db_router.get("/update-last-scrap-kream-product-card-list")
async def update_kream_product_card_list_to_db(
    brand: str,
    listScrapAt: Optional[str] = None,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    return await update_scrap_product_card_list_to_db(db, brand, listScrapAt)


@kream_db_router.get("/update-last-scrap-kream-product-card-detail")
async def update_kream_product_card_detail_to_db(
    brand: str,
    scrapAt: Optional[str] = None,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    return await update_scrap_product_card_detail_to_db(db, brand, scrapAt)


@kream_db_router.get("/update-last-scrap-kream-trading-volume")
async def update_scrap_kream_trading_volume(
    brand: str,
    scrapAt: Optional[str] = None,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_trading_volume_table 업데이트"""
    return await update_scrap_trading_volume_to_db(db, brand, scrapAt)


@kream_db_router.get("/update-last-scrap-kream-buy-and-sell")
async def update_scrap_kream_buy_and_sell(
    brand: str,
    scrapAt: Optional[str] = None,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_buy_and_sell_table 업데이트"""
    return await update_scrap_buy_and_sell_to_db(db, brand, scrapAt)


@kream_db_router.get("/update-last-scrap-kream-product-bridge")
async def update_scrap_kream_product_bridge(
    brand: str,
    scrapAt: Optional[str] = None,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_bridge_table 업데이트"""
    return await update_scrap_kream_product_bridge_to_db(db, brand, scrapAt)
