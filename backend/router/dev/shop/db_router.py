"""dev Router"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException


from db.dev_db import get_dev_db
from model.shop_model import RequestShopInfo, updateShopProductCardSchema
from model.db_model_shop import ShopInfoSchema

from .components.update_to_db import (
    update_scrap_product_card_list_to_db,
    get_shop_info_from_db,
    create_shop_info_to_db,
    get_shop_name_from_db,
    update_candidate_to_db,
    update_shop_product_card_list_for_cost_table,
    upsert_shop_product_size_table,
    get_shop_product_size_table_data,
)
from ..utils.scrap_report import ScrapReport


shop_db_router = APIRouter()


@shop_db_router.get("/update-last-scrap-shop-product-card-list")
async def update_shop_product_card_list_to_db(
    scrapName: str,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    detail_scrap_date, shop_name = scrapName.rsplit("-", 1)
    print(detail_scrap_date, shop_name)
    await update_scrap_product_card_list_to_db(db, shop_name, detail_scrap_date)
    ScrapReport("shop_list").update_report(scrapName, "db_update", True)
    return {"message": "success"}


@shop_db_router.post("/update-shop-product-card-for-cost-table")
async def update_shop_product_card_list_for_cost_table_api(
    updateShopProductCard: updateShopProductCardSchema,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""

    shop_product_card_id = updateShopProductCard.shop_product_card_id
    value = updateShopProductCard.value

    await update_shop_product_card_list_for_cost_table(db, shop_product_card_id, value)
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


@shop_db_router.get("/update-candidate-status")
async def update_candidate_status_api(
    shopProductCardId: int,
    candidate: int,
    db: AsyncSession = Depends(get_dev_db),
):
    return await update_candidate_to_db(db, shopProductCardId, candidate)


# @shop_db_router.post("/post-product-info-draft-to-production-level")
# async def post_product_info_draft_to_production_level(
#     data: productInfoDraftSchema,
#     db: AsyncSession = Depends(get_dev_db),
# ):
#     return await get_product_unique_id(db)


@shop_db_router.get("/upsert-shop-product-size-table")
async def upsert_size_table_api(
    scrapDate: str,
    db: AsyncSession = Depends(get_dev_db),
):
    await upsert_shop_product_size_table(db, scrapDate)
    ScrapReport("shop_list").update_report(scrapDate, "db_update", True)
    return {"message": "success"}


@shop_db_router.get("/get-shop-product-size-table-data")
async def get_shop_product_size_table_data_api(
    productId: str,
    db: AsyncSession = Depends(get_dev_db),
):
    return await get_shop_product_size_table_data(db, productId)
