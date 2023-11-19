from typing import Dict
from sqlalchemy import select
from db.tables_shop import ShopProductCardTable
from db.dev_db import session_local
from model.db_model_shop import ShopProductCardSchema


async def get_track_size_list(searchType: str, content: str):
    """track size list 조회"""

    if searchType == "all":
        assert content.isdigit(), "seacrhType = all, content must be digit"

        stmt = (
            select(ShopProductCardTable)
            .where(ShopProductCardTable.candidate == 2)
            .limit(int(content))
        )

    else:
        content_list = content.split(",")

        filter_dict = {
            "productId": ShopProductCardTable.product_id.in_(content_list),
            "shopProductCardId": ShopProductCardTable.shop_product_card_id.in_(
                content_list
            ),
            "shopName": ShopProductCardTable.shop_name.in_(content_list),
            "brandName": ShopProductCardTable.brand_name.in_(content_list),
        }

        stmt = select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2, filter_dict[searchType]
        )

    db = session_local()
    result = await db.execute(stmt)
    result = result.scalars().all()
    await db.close()  # type: ignore
    return [ShopProductCardSchema(**r.to_dict()) for r in result]
