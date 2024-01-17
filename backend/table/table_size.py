from collections import defaultdict
from typing import List, Dict
from db.tables_shop import ShopProductSizeTable, ShopProductCardTable
from db.dev_db import AdminDB
from sqlalchemy import select
from model.db_model_shop import SizeTableRowSchema


class SizeTable:
    def __init__(self) -> None:
        self.admin_db = AdminDB()

    async def get(self, product_id):
        product_id_list = product_id.split(",")
        raw_data = await self.get_data(product_id_list)
        meta = self.get_meta(raw_data)
        return {"meta": meta, "sizeData": self.size_data(meta, raw_data)}

    async def get_data(self, product_id_list):
        stmt = (
            select(ShopProductSizeTable, ShopProductCardTable)
            .join(ShopProductCardTable)
            .where(
                ShopProductCardTable.product_id.in_(product_id_list),
                ShopProductCardTable.sold_out == False,
                ShopProductSizeTable.available == True,
            )
        )
        size_rows = await self.admin_db.execute(stmt)
        return [
            SizeTableRowSchema(**{**row[0].to_dict(), **row[1].to_dict()})
            for row in size_rows
        ]

    def get_meta(self, data: List[SizeTableRowSchema]):
        all_size = list({r.kor_product_size for r in data})

        def sort_data(v):
            try:
                return int(v)
            except:
                return v

        all_size = sorted(all_size, key=lambda x: sort_data(x))
        all_size = [{"korSize": s, "size": "-", "updateAt": "-"} for s in all_size]
        return {
            "shop": list({r.shop_name for r in data}),
            "size": all_size,
        }

    def size_data(self, meta: Dict, data: List[SizeTableRowSchema]):
        d = defaultdict(list)
        for shop in meta["shop"]:
            for row in data:
                if row.shop_name == shop:
                    dd = {
                        "size": row.shop_product_size,
                        "korSize": row.kor_product_size,
                        "updatedAt": row.updated_at.strftime("%y-%m-%d"),
                    }
                    d[shop].append(dd)
        return dict(d)
