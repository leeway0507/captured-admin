from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from db.tables_kream import (
    KreamProductCardTable,
    KreamTradingVolumeTable,
    KreamBuyAndSellTable,
    KreamProductIdBridgeTable,
)
from .load_scrap_result import *


async def update_scrap_product_card_list_to_db(
    db: AsyncSession,
    brand_name: str,
    list_scrap_at: Optional[str] = None,
):
    if list_scrap_at:
        data = get_kream_product_card_list(brand_name, list_scrap_at, 100000)["data"]
    else:
        data = get_last_scrap_kream_product_card_list(brand_name, 100000)["data"]

    stmt = insert(KreamProductCardTable).values(data)
    stmt = stmt.on_duplicate_key_update(
        trading_volume=stmt.inserted.trading_volume,
        wish=stmt.inserted.wish,
        review=stmt.inserted.review,
        updated_at=stmt.inserted.updated_at,
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def update_scrap_product_card_detail_to_db(
    db: AsyncSession,
    brand_name: str,
    scrap_at: Optional[str] = None,
):
    if scrap_at:
        data = get_kream_product_card_detail(brand_name, scrap_at, 100000)["data"]
    else:
        data = get_last_scrap_kream_product_card_detail(brand_name, 100000)["data"]

    stmt = insert(KreamProductCardTable).values(data)
    stmt = stmt.on_duplicate_key_update(
        retail_price=stmt.inserted.retail_price,
        product_release_date=stmt.inserted.product_release_date,
        color=stmt.inserted.color,
        updated_at=stmt.inserted.updated_at,
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def update_scrap_trading_volume_to_db(
    db: AsyncSession,
    brand_name: str,
    scrap_at: Optional[str] = None,
):
    if scrap_at:
        data = get_kream_trading_volume(brand_name, scrap_at, 100000)["data"]
    else:
        data = get_last_scrap_kream_trading_volume(brand_name, 100000)["data"]

    stmt = insert(KreamTradingVolumeTable).values(data)
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def update_scrap_buy_and_sell_to_db(
    db: AsyncSession, brand_name: str, scrap_at: Optional[str] = None
):
    if scrap_at:
        data = get_kream_buy_and_sell(brand_name, scrap_at, 100000)["data"]
    else:
        data = get_last_scrap_kream_buy_and_sell(brand_name, 100000)["data"]

    stmt = insert(KreamBuyAndSellTable).values(data)
    stmt = stmt.on_duplicate_key_update(
        buy=stmt.inserted.buy,
        sell=stmt.inserted.sell,
        updated_at=stmt.inserted.updated_at,
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def update_scrap_kream_product_bridge_to_db(
    db: AsyncSession, brand_name: str, scrap_at: Optional[str] = None
):
    if scrap_at:
        data = get_kream_product_bridge(brand_name, scrap_at, 100000)["data"]
    else:
        data = get_last_scrap_kream_product_bridge(brand_name, 100000)["data"]

    stmt = insert(KreamProductIdBridgeTable).values(data).prefix_with("IGNORE")
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}
