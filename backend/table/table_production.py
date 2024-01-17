from typing import Dict, List
from db.tables_production import ProductInfoTable
from db.production_db import ProdDB
from . import main_utils

from sqlalchemy import update


class ProductionTable:
    def __init__(self) -> None:
        self.prod_db = ProdDB()

    async def get(self, page: int):
        return await main_utils.get_production_table_data(page=page)

    async def delete(self, sku: int):
        stmt = (
            update(ProductInfoTable)
            .where(ProductInfoTable.sku == sku)
            .values(deploy=-1)
        )
        return await self.prod_db.execute_and_commit(stmt)

    async def put(self, value: Dict):
        stmt = (
            update(ProductInfoTable)
            .where(ProductInfoTable.sku == value["sku"])
            .values(**value)
        )
        return await self.prod_db.execute_and_commit(stmt)

    async def patch(self, sku: int, column: str, value: str) -> None:
        stmt = (
            update(ProductInfoTable)
            .where(ProductInfoTable.sku == sku)
            .values({column: value})
        )
        return await self.prod_db.execute_and_commit(stmt)
