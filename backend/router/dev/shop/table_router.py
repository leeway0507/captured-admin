"""shop Router"""
import os
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends


from db.dev_db import get_dev_db
from db.production_db import get_production_db
from components.dev.shop.table_data_loader import (
    ShopTableDataLoader,
    SearchType,
    TableType,
)

table_router = APIRouter()


@table_router.get("/get-cost-table-brand-name-data")
async def cost_table_brand_name(
    value: str,
    admin_db: AsyncSession = Depends(get_dev_db),
    prod_db: AsyncSession = Depends(get_production_db),
):
    """camel : getCostTableBrandNameData"""
    value = value.replace("c%27", "'")

    return await ShopTableDataLoader(
        admin_db, prod_db, TableType.COST_TABLE, SearchType.BRAND_NAME
    ).extract_data(value)


@table_router.get("/get-cost-table-shop-name-data")
async def cost_table_shop_name(
    value: str,
    admin_db: AsyncSession = Depends(get_dev_db),
    prod_db: AsyncSession = Depends(get_production_db),
):
    """camel : getCostTableShopNameData"""
    value = value.replace("c%27", "'")

    return await ShopTableDataLoader(
        admin_db, prod_db, TableType.COST_TABLE, SearchType.SHOP_NAME
    ).extract_data(value)


@table_router.get("/get-candidate-table-brand-name-data")
async def candidate_table_brand_name(
    value: str,
    admin_db: AsyncSession = Depends(get_dev_db),
    prod_db: AsyncSession = Depends(get_production_db),
):
    """camel : getCandidateTableBrandNameData"""
    value = value.replace("c%27", "'")

    return await ShopTableDataLoader(
        admin_db, prod_db, TableType.CANDIDATE_TABLE, SearchType.BRAND_NAME
    ).extract_data(value)


@table_router.get("/get-candidate-table-shop-name-data")
async def candidate_table_shop_name(
    value: str,
    admin_db: AsyncSession = Depends(get_dev_db),
    prod_db: AsyncSession = Depends(get_production_db),
):
    """camel : getCandidateTableShopNameData"""
    value = value.replace("c%27", "'")

    return await ShopTableDataLoader(
        admin_db, prod_db, TableType.CANDIDATE_TABLE, SearchType.SHOP_NAME
    ).extract_data(value)
