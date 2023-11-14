from ast import alias
from typing import Dict, List, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import update, bindparam, select, and_

from db.tables_shop import ShopInfoTable, ShopProductCardTable, ShopProductSizeTable
from .load_scrap_result import get_last_scrap_product_dict, get_scrap_product_dict
from model.shop_model import ShopProductId, RequestShopInfo
from model.db_model_shop import ShopInfoSchema, ShopProductCardSchema


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


async def get_shop_info_by_name(db: AsyncSession, shopName: str):
    stmt = select(ShopInfoTable).where(ShopInfoTable.shop_name == shopName)
    result = await db.execute(stmt)
    result = result.scalars().first()
    return ShopInfoSchema(**result.to_dict()).model_dump(by_alias=True)


async def get_shop_product_list(db: AsyncSession, shopName: str, brandName: str):
    brand_name_list = brandName.split(",")
    stmt = select(ShopProductCardTable).where(
        and_(
            ShopProductCardTable.shop_name == shopName,
            ShopProductCardTable.brand_name.in_(brand_name_list),
        )
    )

    result = await db.execute(stmt)
    result = result.scalars().all()
    return [
        ShopProductCardSchema(**row.to_dict()).model_dump(by_alias=True)
        for row in result
    ]


async def update_candidate_to_db(
    db: AsyncSession, shopProductCardId: int, candidate: int
):
    stmt = (
        update(ShopProductCardTable)
        .where(ShopProductCardTable.shop_product_card_id == shopProductCardId)
        .values(candidate=candidate)
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def load_scraped_brand_name(db: AsyncSession, shopName: str):
    stmt = select(ShopProductCardTable.brand_name.distinct()).where(
        ShopProductCardTable.shop_name == shopName
    )
    result = await db.execute(stmt)
    result = result.scalars().all()
    return result


async def get_shop_product_list_for_cost_table(
    db: AsyncSession, searchType: str, value: str
):
    filter_dict = {
        "brandName": ShopProductCardTable.brand_name.like(f"{value}%"),
        "shopName": ShopProductCardTable.shop_name == value,
    }

    stmt = select(ShopProductCardTable).where(
        and_(
            ShopProductCardTable.candidate != 0,
            filter_dict[searchType],
        )
    )

    result = await db.execute(stmt)
    result = result.scalars().all()
    return [
        ShopProductCardSchema(**row.to_dict()).model_dump(by_alias=True)
        for row in result
    ]
