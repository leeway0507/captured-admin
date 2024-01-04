# """dev Router"""

# from typing import Optional
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import APIRouter, Depends, HTTPException

# from db.dev_db import get_dev_db

# from components.dev.platform.platform_db import (
#     update_scrap_product_card_list_to_db,
#     update_scrap_product_card_detail_to_db,
#     update_scrap_trading_volume_to_db,
#     update_scrap_buy_and_sell_to_db,
#     update_scrap_kream_product_bridge_to_db,
# )


# kream_db_router = APIRouter()

# kream_dict = {}

# platform_page_report = ScrapReport("platform_page")
# platform_list_report = ScrapReport("platform_list")


# @kream_db_router.get("/update-all-detail-kream-to-db")
# async def update_all(
#     searchValue: str,
#     scrapTime: str,
#     db: AsyncSession = Depends(get_dev_db),
# ):
#     await update_scrap_product_card_detail_to_db(db, searchValue, scrapTime)
#     await update_scrap_trading_volume_to_db(db, searchValue, scrapTime)
#     await update_scrap_buy_and_sell_to_db(db, searchValue, scrapTime)
#     await update_scrap_kream_product_bridge_to_db(db, searchValue, scrapTime)

#     platform_page_report.update_report(scrapTime + "-kream", "db_update", True)

#     return {"message": "success"}


# @kream_db_router.get("/update-scrap-kream-product-card-list")
# async def update_kream_product_card_list_to_db(
#     platformType: str,
#     scrapTime: str,
#     db: AsyncSession = Depends(get_dev_db),
# ):
#     """camel : insertListScrapToDB"""
#     platform_list_report.update_report(scrapTime + "-kream", "db_update", True)
#     return await update_scrap_product_card_list_to_db(
#         db,
#         platformType,
#         scrapTime,
#     )


# @kream_db_router.get("/update-last-scrap-kream-product-card-detail")
# async def update_kream_product_card_detail_to_db(
#     brand: str,
#     scrapAt: Optional[str] = None,
#     db: AsyncSession = Depends(get_dev_db),
# ):
#     """kream_product_card_table 업데이트"""
#     return await update_scrap_product_card_detail_to_db(db, brand, scrapAt)


# @kream_db_router.get("/update-last-scrap-kream-trading-volume")
# async def update_scrap_kream_trading_volume(
#     brand: str,
#     scrapAt: Optional[str] = None,
#     db: AsyncSession = Depends(get_dev_db),
# ):
#     """kream_trading_volume_table 업데이트"""
#     return await update_scrap_trading_volume_to_db(db, brand, scrapAt)


# @kream_db_router.get("/update-last-scrap-kream-buy-and-sell")
# async def update_scrap_kream_buy_and_sell(
#     brand: str,
#     scrapAt: Optional[str] = None,
#     db: AsyncSession = Depends(get_dev_db),
# ):
#     """kream_buy_and_sell_table 업데이트"""
#     return await update_scrap_buy_and_sell_to_db(db, brand, scrapAt)


# @kream_db_router.get("/update-last-scrap-kream-product-bridge")
# async def update_scrap_kream_product_bridge(
#     brand: str,
#     scrapAt: Optional[str] = None,
#     db: AsyncSession = Depends(get_dev_db),
# ):
#     """kream_product_bridge_table 업데이트"""
#     return await update_scrap_kream_product_bridge_to_db(db, brand, scrapAt)
