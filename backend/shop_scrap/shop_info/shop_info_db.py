from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import select
from db.tables_shop import ShopInfoTable
from model.shop_model import RequestShopInfo
from model.db_model_shop import ShopInfoSchema


async def create_shop_info_to_db(
    db: AsyncSession,
    data: RequestShopInfo,
):
    db_data = ShopInfoSchema(
        **data.model_dump(), updated_at=datetime.now().replace(microsecond=0)
    )

    stmt = insert(ShopInfoTable).values(db_data.model_dump())

    stmt = stmt.on_duplicate_key_update(
        shop_name=stmt.inserted.shop_name,
        shop_url=stmt.inserted.shop_url,
        tax_reduction_rate=stmt.inserted.tax_reduction_rate,
        del_agc_tax_reduction_rate=stmt.inserted.del_agc_tax_reduction_rate,
        dome_ship_price=stmt.inserted.dome_ship_price,
        intl_ship_price=stmt.inserted.intl_ship_price,
        from_us_shipping=stmt.inserted.from_us_shipping,
        is_ddp=stmt.inserted.is_ddp,
        updated_at=stmt.inserted.updated_at,
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def get_shop_info_from_db(
    db: AsyncSession,
):
    stmt = select(ShopInfoTable)
    result = await db.execute(stmt)
    result = result.scalars().all()
    return [row.to_dict() for row in result]
