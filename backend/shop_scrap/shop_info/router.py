from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.dev_db import get_dev_db
from model.shop_model import RequestShopInfo
from model.db_model_shop import ShopInfoSchema

from . import shop_info_db as shop

## /api/shop_info
shop_info = APIRouter()


@shop_info.get("/get-shop-info")
async def get_shop_info(
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    result = await shop.get_shop_info_from_db(db)
    return [ShopInfoSchema(**row).model_dump(by_alias=True) for row in result]


@shop_info.post("/upsert-shop-info")
async def create_shop_info(
    data: RequestShopInfo,
    db: AsyncSession = Depends(get_dev_db),
):
    """camel : upsertShopInfo"""
    await shop.create_shop_info_to_db(db, data)
    return {"message": "success"}
