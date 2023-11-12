from typing import Dict, List, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import update, bindparam, select

from db.tables_shop import ShopInfoTable, ShopProductCardTable, ShopProductSizeTable
from .load_scrap_result import get_last_scrap_product_dict, get_scrap_product_dict
from model.shop_model import ShopProductId, RequestShopInfo
from model.db_model_shop import ShopInfoSchema


async def update_scrap_product_card_list_to_db(
    db: AsyncSession,
    shop_name: str,
    list_scrap_at: Optional[str] = None,
):
    if list_scrap_at:
        data = get_scrap_product_dict(shop_name, list_scrap_at)["data"]
    else:
        data = get_last_scrap_product_dict(shop_name)["data"]

    stmt = insert(ShopProductCardTable).values(data)
    stmt = stmt.on_duplicate_key_update(
        kor_price=stmt.inserted.kor_price,
        us_price=stmt.inserted.us_price,
        original_price=stmt.inserted.original_price,
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def update_scrap_product_card_product_id_to_db(
    db: AsyncSession,
    data: List[ShopProductId],
):
    stmt = (
        update(ShopProductCardTable)
        .where(
            ShopProductCardTable.shop_product_card_id
            == bindparam("shop_product_card_id")
        )
        .values(product_id=bindparam("product_id"))
    )
    await db.execute(stmt, data)
    await db.commit()
    return {"message": "success"}


# async def update_scrap_product_size_to_db(
#     db: AsyncSession,
#     shop_name: str,
#     list_scrap_at: Optional[str] = None,
# ):
#     if list_scrap_at:
#         data = get_scrap_product_list(shop_name, list_scrap_at)["data"]
#     else:
#         data = get_last_scrap_product_list(shop_name)["data"]

#     data = list(
#         map(
#             lambda x: {
#                 "shop_product_card_id": x.get("shop_product_card_id"),
#                 "size": x.get("size"),
#             },
#             data,
#         )
#     )

#     stmt = insert(ShopProductSizeTable).values(data)
#     stmt = stmt.on_duplicate_key_update(
#         shop_product_card_id=stmt.inserted.shop_product_card_id,
#         size=stmt.inserted.size,
#         updated_at=stmt.inserted.updated_at,
#     )
#     await db.execute(stmt)
#     await db.commit()
#     return {"message": "success"}


#### shop_info ####


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


async def get_shop_name_from_db(
    db: AsyncSession,
):
    stmt = select(ShopInfoTable.shop_name)
    result = await db.execute(stmt)
    result = result.scalars().all()
    return result
