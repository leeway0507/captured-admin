from datetime import datetime, timedelta

from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from db.tables_kream import (
    KreamProductCardTable,
    KreamTradingVolumeTable,
    KreamBuyAndSellTable,
    KreamProductIdBridgeTable,
)
from .load_scrap_result import *
from model.kream_scraping import KreamProductDetailSchema
from model.kream_scraping import KreamProductSizeInfo


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


async def get_kream_product_detail_list_from_db(
    db: AsyncSession, searchType: str, content: str
):
    content_list = content.split(",")

    filter_dict = {
        "productId": KreamProductIdBridgeTable.product_id.in_(content_list),
        "brandName": KreamProductCardTable.brand_name.in_(content_list),
        "kreamId": KreamProductCardTable.kream_id.in_(content_list),
    }

    # join kreamProductCardTable and kreamProductIdBridgeTable
    stmt = (
        select(KreamProductCardTable, KreamProductIdBridgeTable.product_id)
        .join(KreamProductIdBridgeTable)
        .filter(filter_dict[searchType])
    )
    result = await db.execute(stmt)
    result = result.fetchall()
    return [
        KreamProductDetailSchema(**row[0].to_dict(), product_id=row[1]).model_dump(
            by_alias=True
        )
        for row in result
    ]


async def get_kream_product_size_from_db(
    db: AsyncSession, searchType: str, content: str
):
    if searchType == "productId":
        stmt = select(KreamProductIdBridgeTable.kream_id).filter(
            KreamProductIdBridgeTable.product_id == (content)
        )
        result = await db.execute(stmt)
        content = result.first()
        if not content:
            return {"KreamTradingVolume": [], "KreamBuyAndSell": []}
        content = content[0]

    two_weeks_ago = datetime.today() - timedelta(days=14)

    two_weeks_ago = two_weeks_ago.replace(hour=0, minute=0, second=0, microsecond=0)

    stmt_1 = select(KreamTradingVolumeTable).filter(
        and_(
            KreamTradingVolumeTable.kream_id == (content),
            KreamTradingVolumeTable.trading_at >= (two_weeks_ago),
        )
    )
    result_1 = await db.execute(stmt_1)

    stmt_2 = select(KreamBuyAndSellTable).filter(
        KreamBuyAndSellTable.kream_id == (content)
    )
    result_2 = await db.execute(stmt_2)

    result_1 = result_1.scalars().all()
    result_2 = result_2.scalars().all()

    return {
        "KreamTradingVolume": [row.to_dict() for row in result_1],
        "KreamBuyAndSell": [row.to_dict() for row in result_2],
    }


async def get_kream_product_size_info(db: AsyncSession, searchType: str, content: str):
    data = await get_kream_product_size_from_db(db, searchType, content)

    if not data["KreamTradingVolume"]:
        return {"date": [], "data": []}

    buy_and_sell_df = pd.DataFrame(data["KreamBuyAndSell"])
    trading_volume_df = pd.DataFrame(data["KreamTradingVolume"])

    # get least and last date
    date = sorted(trading_volume_df["trading_at"].unique())
    least_date = date[0]
    last_date = date[-1]

    # get price info
    df = (
        trading_volume_df.groupby(["kream_product_size"])["price"]
        .describe()
        .reset_index()
    )
    df = pd.merge(buy_and_sell_df, df, on="kream_product_size", how="left").fillna(0)
    df = df[["kream_product_size", "buy", "sell", "count", "min", "50%", "max"]]
    df = df.rename(columns={"50%": "median"})

    # get lightening info
    lightening_df = (
        trading_volume_df.groupby(["kream_product_size"])["lightening"]
        .value_counts()
        .reset_index()
    )
    lightening_df = lightening_df[lightening_df["lightening"] == True][
        ["kream_product_size", "count"]
    ]
    lightening_df = lightening_df.rename(columns={"count": "lightening"})
    df = pd.merge(df, lightening_df, on="kream_product_size", how="left").fillna(0)

    return {
        "scrapDate": [least_date, last_date],
        "sizeData": [KreamProductSizeInfo(**row) for row in df.to_dict(orient="records")],  # type: ignore
    }


async def get_kream_product_color_for_registration(db: AsyncSession, product_id: str):
    stmt = (
        select(KreamProductCardTable.color)
        .join(KreamProductIdBridgeTable)
        .filter(KreamProductIdBridgeTable.product_id == product_id)
    )
    result = await db.execute(stmt)
    result = result.first()
    return result if result else "no data"
