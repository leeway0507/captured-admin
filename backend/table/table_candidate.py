import json
from typing import List, Dict
from sqlalchemy import select, update, insert


from db.dev_db import AdminDB
from db.production_db import ProdDB
from db.tables_shop import ShopInfoTable, ShopProductCardTable
from db.tables_kream import KreamProductIdBridgeTable
from db.tables_production import ProductInfoTable
from model.product_model import ProductInfoForTableDataSchema
from model.db_model_shop import ShopProductCardSchema, ShopInfoSchema


class CandidateTable:
    def __init__(self):
        self.admin_db = AdminDB()
        self.prod_db = ProdDB()

    async def get(self, type: str, content: str):
        shop_card_list = await self._shop_card_list(type, content)
        prod_id_list = self._product_id_list(shop_card_list)
        return {
            "shopCard": shop_card_list,
            "prodCard": await self._prod_card_list(prod_id_list),
            "kreamMatch": await self._kream_match_info(prod_id_list),
            "currency": self._buying_currency(),
            "shopInfo": await self._shop_info(),
        }

    async def _shop_card_list(self, type: str, content: str) -> List[Dict]:
        stmt = getattr(LoadStrategy(), type)(content)
        result = await self.admin_db.execute(stmt)
        return [
            ShopProductCardSchema(**row[0].to_dict()).model_dump(by_alias=True)
            for row in result
        ]

    def _product_id_list(self, shop_card_list: List[dict]) -> List[str]:
        l = []
        for row in shop_card_list:
            if not row["productId"] in ("-", None):
                l.append(row["productId"])
        return list(set(l))

    async def _kream_match_info(self, product_id_list: List[str]):
        stmt = select(KreamProductIdBridgeTable.product_id).filter(
            KreamProductIdBridgeTable.product_id.in_(product_id_list)
        )
        result = await self.admin_db.execute(stmt)
        return [row[0] for row in set(result)]

    async def _prod_card_list(self, product_id_list: List):
        stmt = select(ProductInfoTable).where(
            ProductInfoTable.product_id.in_(product_id_list)
        )
        result = await self.prod_db.execute(stmt)

        return [
            ProductInfoForTableDataSchema(**row[0].to_dict()).model_dump(by_alias=True)
            for row in result
        ]

    async def _shop_info(self):
        stmt = select(ShopInfoTable)
        result = await self.admin_db.execute(stmt)
        return [
            ShopInfoSchema(**row[0].to_dict()).model_dump(by_alias=True)
            for row in result
        ]

    def _buying_currency(self):
        path = "components/currency/data/buying_currency.json"
        with open(path, "r") as f:
            return json.load(f)

    async def patch(self, shop_product_card_id: int, column: str, content: str) -> None:
        stmt = (
            update(ShopProductCardTable)
            .where(ShopProductCardTable.shop_product_card_id == shop_product_card_id)
            .values({column: content})
        )
        return await self.admin_db.execute_and_commit(stmt)

    async def delete(self, shop_product_card_id: int):
        stmt = (
            update(ShopProductCardTable)
            .where(ShopProductCardTable.shop_product_card_id == shop_product_card_id)
            .values(candidate=-1)
        )
        return await self.admin_db.execute_and_commit(stmt)

    async def put(self, shop_product_card_id: int, value: Dict):
        stmt = (
            update(ShopProductCardTable)
            .where(ShopProductCardTable.shop_product_card_id == shop_product_card_id)
            .values(**value)
        )
        return await self.admin_db.execute_and_commit(stmt)


class LoadStrategy:
    def brand(self, content: str):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.brand_name == content,
            ShopProductCardTable.candidate != -1,
            ShopProductCardTable.sold_out != 1,
        )

    def shop(self, content: str):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.shop_name == content,
            ShopProductCardTable.candidate != -1,
            ShopProductCardTable.sold_out != 1,
        )
