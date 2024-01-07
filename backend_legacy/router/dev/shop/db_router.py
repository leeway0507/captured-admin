"""dev Router"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException


from db.dev_db import get_dev_db
from env import get_path
from model.shop_model import RequestShopInfo, updateShopProductCardSchema
from model.db_model_shop import ShopInfoSchema

from components.dev.shop.update_to_db import (
    update_scrap_product_card_list_to_db,
    get_shop_info_from_db,
    create_shop_info_to_db,
    get_shop_name_from_db,
    update_candidate_status,
    update_shop_product_card_table,
    upsert_shop_product_size_table,
    get_shop_product_size_table_data,
)

from components.dev.utils import ScrapReport


platform_list_path = get_path("platform_list")
platform_page_path = get_path("platform_page")


platform_list_report = ScrapReport(platform_list_path)
platform_page_report = ScrapReport(platform_page_path)


shop_db_router = APIRouter()


@shop_db_router.get("/update-last-scrap-shop-product-card-list")
async def update_shop_product_card_list_to_db(
    scrapName: str,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_card_table 업데이트"""
    detail_scrap_date, shop_name = scrapName.rsplit("-", 1)

    await update_scrap_product_card_list_to_db(db, shop_name, detail_scrap_date)

    platform_list_report.report_file_name = detail_scrap_date
    platform_list_report.update_report({"db_update": True})

    return {"message": "success"}


@shop_db_router.put("/update-shop-product-card-for-cost-table")
async def update_shop_product_card_table_api(
    updateShopProductCard: updateShopProductCardSchema,
    db: AsyncSession = Depends(get_dev_db),
):
    """camel : updateShopProductCardTable"""

    shop_product_card_id = updateShopProductCard.shop_product_card_id
    value = updateShopProductCard.value

    await update_shop_product_card_table(db, shop_product_card_id, value)
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
    """camel : upsertShopInfo"""
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
    return await update_candidate_status(db, shopProductCardId, candidate)


@shop_db_router.get("/upsert-shop-product-size-table")
async def upsert_size_table_api(
    scrapDate: str,
    db: AsyncSession = Depends(get_dev_db),
):
    await upsert_shop_product_size_table(db, scrapDate)

    platform_list_report.report_file_name = scrapDate
    platform_list_report.update_report({"db_update": True})

    return {"message": "success"}


@shop_db_router.get("/get-shop-product-size-table-data")
async def get_shop_product_size_table_data_api(
    productId: str,
    db: AsyncSession = Depends(get_dev_db),
):
    return await get_shop_product_size_table_data(db, productId)
