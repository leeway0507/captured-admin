"""admin Router"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from model.db_model_production import ProductInfoSchema, ProductInfoDBSchema

from db.production_db import get_production_db
from .utils import *

production_router = APIRouter()


@production_router.get("/get-order-history")
async def get_order_history_list(db: AsyncSession = Depends(get_production_db)):
    """order_history 조회"""
    return await get_order_history(db)


@production_router.get("/get-order-row")
async def get_order_rows(db: AsyncSession = Depends(get_production_db)):
    """order_row 조회"""
    return await get_order_row(db)


@production_router.get("/get-category")
async def get_item_list(db: AsyncSession = Depends(get_production_db)):
    """리스트 불러오기"""
    return await get_category(db)


@production_router.post("/create-product")
async def create(
    product: ProductInfoSchema, db: AsyncSession = Depends(get_production_db)
):
    """제품 생성"""
    product.sku = await create_new_sku(db)
    search_info = product.brand + " " + product.product_name + " " + product.product_id
    price = product.price
    sku = product.sku
    price_desc_cursor = str(price).zfill(7) + str(sku).zfill(5)
    price_asc_cursor = str(100000000000 - int(price_desc_cursor))

    product_info_db = ProductInfoDBSchema(
        search_info=search_info,
        price_desc_cursor=price_desc_cursor,
        price_asc_cursor=price_asc_cursor,
        **product.model_dump(),
    )

    if await create_product(db, product_info_db):
        return {"message": "success", "sku": product.sku}
    else:
        raise HTTPException(status_code=406, detail="제품 등록 실패. 다시 시도해주세요.")


@production_router.post("/update-product")
async def update(
    product_in_db: ProductInfoDBSchema, db: AsyncSession = Depends(get_production_db)
):
    """제품 수정"""

    if await update_product(db, product_in_db):
        return {"message": "success"}
    else:
        raise HTTPException(status_code=406, detail="제품 업데이트에 실패했습니다. 다시 시도해주세요.")


@production_router.post("/delete-product")
async def delete(
    product: ProductInfoSchema, db: AsyncSession = Depends(get_production_db)
):
    """제품 삭제"""

    if product.sku == None:
        raise HTTPException(status_code=406, detail="제품정보에 SKU가 존재하지 않아 삭제할 수 없습니다.")

    if await delete_product(db, product.sku):
        return {"message": "success"}
    else:
        raise HTTPException(status_code=406, detail="제품 삭제에 실패했습니다. 다시 시도해주세요.")


@production_router.get("/get-product-info-for-cost-product")
async def get_product_info_for_cost_product(
    db: AsyncSession = Depends(get_production_db),
):
    """product_unique_id 조회"""

    return await get_product_info_for_cost_table(db)


@production_router.get("/update-product-deploy-status")
async def update_product_deploy_status_api(
    sku: int,
    status: int,
    db: AsyncSession = Depends(get_production_db),
):
    """update product_info deploy"""

    return await update_product_deploy_status(db, sku, status)
