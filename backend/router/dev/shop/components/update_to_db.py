import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import update, bindparam, select, and_, delete


from db.tables_shop import ShopInfoTable, ShopProductCardTable, ShopProductSizeTable
from .load_scrap_result import (
    get_last_scrap_product_dict,
    get_scrap_product_dict,
    get_scrap_size_dict,
    get_scrap_size_product_id_dict,
)
from model.shop_model import ShopProductId, RequestShopInfo
from model.db_model_shop import (
    ShopInfoSchema,
    ShopProductCardSchema,
    ShopProductSizeSchema,
)


### production
from db.tables_production import ProductInfoTable
from db.production_db import session_local


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
    shop_name_list = shopName.split(",")
    stmt = select(ShopInfoTable).where(ShopInfoTable.shop_name.in_(shop_name_list))
    result = await db.execute(stmt)
    result = result.scalars().all()
    return [ShopInfoSchema(**row.to_dict()).model_dump(by_alias=True) for row in result]


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
    db_data = [
        ShopProductCardSchema(**row.to_dict()).model_dump(by_alias=True)
        for row in result
    ]

    shop_name = ",".join((set([row["shopName"] for row in db_data])))

    print(shop_name)

    return {
        "shopInfos": await get_shop_info_by_name(db, shop_name),
        "dbData": db_data,
        "currency": get_currency_from_local(),
    }


def get_currency_from_local() -> Dict:
    path = "router/dev/shop/components/currency/data/buying_currency.json"
    with open(path, "r") as f:
        data = json.load(f)

    return data


async def update_shop_product_card_list_for_cost_table(
    db: AsyncSession,
    shop_product_card_id: int,
    value: Dict[str, Any],
):
    stmt = (
        update(ShopProductCardTable)
        .where(ShopProductCardTable.shop_product_card_id == shop_product_card_id)
        .values(**value)
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


async def update_product_id_by_shop_product_card_id(
    db: AsyncSession, product_info: List[dict[str, Any]]
):
    """
    product_info = [
    key: shop_product_card_id
    value: product_id
    ]
    key,value로 이름을 변경한 이유는 bindparam 사용을 위해서는 column 이름과 달라야 하기 때문임.
    """

    stmt = (
        update(ShopProductCardTable)
        .where(ShopProductCardTable.shop_product_card_id == bindparam("key"))
        .values(product_id=bindparam("value"))
    )
    await db.execute(stmt, product_info)
    await db.commit()
    return {"message": "success"}


async def upsert_size_table(db: AsyncSession, scrapDate: str):
    """size table에 insert"""

    size_dict = get_scrap_size_dict(scrapDate)
    product_id_dict = get_scrap_size_product_id_dict(scrapDate)

    # delete
    stmt = delete(ShopProductSizeTable).where(
        ShopProductSizeTable.shop_product_card_id.in_(size_dict.get("unique_id"))
    )
    await db.execute(stmt)

    # insert
    stmt = insert(ShopProductSizeTable).values(size_dict.get("data"))
    await db.execute(stmt)

    # update product_id
    product_id_info = product_id_dict.get("data")
    assert product_id_info, "product_id_info is None"

    await update_product_id_by_shop_product_card_id(db, product_id_info)

    await db.commit()
    return True


async def get_size_table_data(db: AsyncSession, product_id):
    product_id_list = product_id.split(",")

    stmt = (
        select(ShopProductSizeTable)
        .join(ShopProductCardTable)
        .where(ShopProductCardTable.product_id.in_(product_id_list))
    )
    size_rows = await db.execute(stmt)
    size_rows = size_rows.scalars().all()

    stmt = select(ShopProductCardTable).where(
        ShopProductCardTable.product_id.in_(product_id_list)
    )
    prod_rows = await db.execute(stmt)
    prod_rows = prod_rows.scalars().all()
    return {
        "sizeInfo": [ShopProductSizeSchema(**row.to_dict()) for row in size_rows],
        "productInfo": [ShopProductCardSchema(**row.to_dict()) for row in prod_rows],
    }
