"""dev Router"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from dotenv import dotenv_values

from db.dev_db import get_dev_db
from model.shop_model import RequestShopInfo
from model.db_model_shop import ShopInfoSchema

from .components.update_to_db import (
    update_scrap_product_card_list_to_db,
    get_shop_info_from_db,
    create_shop_info_to_db,
    get_shop_name_from_db,
)
from .components.shop_product_card_list.create_log import update_scrap_result

shop_db_router = APIRouter()

config = dotenv_values(".env.dev")


@shop_db_router.get("/update-last-scrap-shop-product-card-list")
async def update_shop_product_card_list_to_db(
    scrapName: str,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    detail_scrap_date, shop_name = scrapName.rsplit("-", 1)
    print(detail_scrap_date, shop_name)
    await update_scrap_product_card_list_to_db(db, shop_name, detail_scrap_date)
    update_scrap_result(scrapName, "db_update", True)
    return {"message": "success"}


@shop_db_router.get("/get-shop-info")
async def get_shop_info(
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    result = await get_shop_info_from_db(db)
    return [ShopInfoSchema(**row).model_dump(by_alias=True) for row in result]


@shop_db_router.post("/upsert-shop-info")
async def create_shop_info(
    data: RequestShopInfo,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    await create_shop_info_to_db(db, data)
    return {"message": "success"}


@shop_db_router.get("/get-last-scrap-product-list")
async def get_last_scrap_product_list(
    db: AsyncSession = Depends(get_dev_db),
):
    return await get_shop_name_from_db(db)
