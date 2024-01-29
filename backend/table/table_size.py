from collections import defaultdict
from typing import List, Dict
from db.tables_shop import ShopProductSizeTable, ShopProductCardTable, ShopInfoTable
from db.dev_db import AdminDB
from sqlalchemy import select
from model.db_model_shop import SizeTableRowSchema, ShopInfoSchema


class SizeMetaSchema(SizeTableRowSchema):
    kor_price: int
    original_price_currency: str


class SizeTable:
    def __init__(self) -> None:
        self.admin_db = AdminDB()

    async def get(self, shop_product_card_id):
        shop_product_card_id_list = shop_product_card_id.split(",")
        raw_data = await self.get_data(shop_product_card_id_list)
        meta = await self.get_meta(raw_data)
        return {"meta": meta, "sizeData": self.size_data(meta, raw_data)}

    async def get_data(self, shop_product_card_id_list):
        stmt = (
            select(ShopProductSizeTable, ShopProductCardTable)
            .join(ShopProductCardTable)
            .where(
                ShopProductCardTable.shop_product_card_id.in_(
                    shop_product_card_id_list
                ),
                ShopProductCardTable.sold_out == False,
                ShopProductSizeTable.available == True,
            )
        )
        size_rows = await self.admin_db.execute(stmt)
        return [
            SizeMetaSchema(**{**row[0].to_dict(), **row[1].to_dict()})
            for row in size_rows
        ]

    async def get_meta(self, data: List[SizeMetaSchema]):
        all_size = list({r.kor_product_size for r in data})
        price = await self.price_data(data)

        def sort_data(v):
            try:
                return int(v)
            except:
                return v

        all_size = sorted(all_size, key=lambda x: sort_data(x))
        all_size = [{"korSize": s, "size": "-", "updateAt": "-"} for s in all_size]
        return {
            "shop": list({r.shop_name for r in data}),
            "price": price,
            "size": all_size,
        }

    async def price_data(self, data: List[SizeMetaSchema]):
        curr = {
            "KRW": 1,
            "USD": 1350,
            "GBP": 1700,
            "EUR": 1450,
        }
        shop_info_list = await self.shop_info()

        price_dict = {}
        for r in data:
            p = r.kor_price
            if price_dict.get(r.shop_name, None) == None:
                shop_info = list(
                    filter(lambda x: x["shop_name"] == r.shop_name, shop_info_list)
                )[0]

                if shop_info["tax_reduction_rate"]:
                    p = r.kor_price / (1 + shop_info["tax_reduction_rate"])

                if shop_info["intl_ship_price"]:
                    p += shop_info["intl_ship_price"] * curr[r.original_price_currency]

                price_dict[r.shop_name] = int(round(p * 1.03 * 1.03, -2))

        return price_dict

    async def shop_info(self):
        stmt = select(ShopInfoTable)
        result = await self.admin_db.execute(stmt)
        return [r[0].to_dict() for r in result]

    def size_data(self, meta: Dict, data: List[SizeMetaSchema]):
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
