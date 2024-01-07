import json
from enum import Enum
from typing import Dict, List, Any, Protocol, Tuple
from .. import update_to_db

from db.tables_kream import KreamProductIdBridgeTable
from db.tables_shop import ShopProductCardTable
from db.tables_production import ProductInfoTable
from model.db_model_shop import ShopProductCardSchema
from model.product_model import ProductInfoForTableDataSchema
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession


class TableType(Enum):
    CANDIDATE_TABLE = "candidate_table"
    COST_TABLE = "cost_table"


class SearchType(Enum):
    BRAND_NAME = "brand_name"
    SHOP_NAME = "shop_name"


class ShopTableDataLoader:
    _instance = {}

    def __init__(
        self,
        admin_db: AsyncSession,
        prod_db: AsyncSession,
        table_type: TableType,
        search_type: SearchType,
    ) -> None:
        self.admin_db = admin_db
        self.prod_db = prod_db
        self.table_type = table_type
        self.search_type = search_type
        self.module: DataModule = getattr(
            TableModuleFactory(admin_db), f"{table_type.value}_{search_type.value}"
        )()

    def __new__(
        cls,
        admin_db: AsyncSession,
        prod_db: AsyncSession,
        table_type: TableType,
        search_type: SearchType,
    ):
        if not (table_type, search_type) in cls._instance:
            cls._instance[(table_type, search_type)] = super(
                ShopTableDataLoader, cls
            ).__new__(cls)
        return cls._instance[(table_type, search_type)]

    async def extract_data(self, value: str):
        product_info = await self.get_product_data(value)
        product_id_list = self.__extract_product_id(product_info)
        return {
            "kreamMatchInfo": await self.get_kream_match_info(product_id_list),
            "currency": self.get_currency(),
            "shopInfo": await self.get_shop_info_list(value),
            "shopProductInfo": product_info,
            "prodProductInfo": await self.prod_product_info(product_id_list),
        }

    def get_currency(self) -> Dict:
        path = "components/dev/shop/currency/data/buying_currency.json"
        with open(path, "r") as f:
            data = json.load(f)
        return data

    async def get_shop_info_list(self, value: str) -> List[Dict]:
        shop_name_list = await self.__get_shop_name_list(value)
        return await update_to_db.get_shop_info_by_name(self.admin_db, shop_name_list)

    async def get_product_data(self, value: str):
        filter_query = self.__get_filter_query(value)

        stmt = select(ShopProductCardTable).where(and_(*filter_query))
        result = await self.admin_db.execute(stmt)
        result = result.scalars().all()
        return [
            ShopProductCardSchema(**row.to_dict()).model_dump(by_alias=True)
            for row in result
        ]

    async def get_kream_match_info(self, product_id_list: List[str]):
        stmt = select(KreamProductIdBridgeTable.product_id).filter(
            KreamProductIdBridgeTable.product_id.in_(product_id_list)
        )
        result = await self.admin_db.execute(stmt)
        result = result.all()
        return [row[0] for row in set(result)]

    async def prod_product_info(self, product_id_list: List[str]):
        stmt = select(ProductInfoTable).where(
            ProductInfoTable.product_id.in_(product_id_list)
        )
        result = await self.prod_db.execute(stmt)

        return [
            ProductInfoForTableDataSchema(**row[0].to_dict()).model_dump(by_alias=True)
            for row in result
        ]

    def __get_filter_query(self, value: str):
        """모듈 이용"""
        return self.module.admin_filter_query(value)

    async def __get_shop_name_list(self, value: str):
        """모듈 이용"""
        return await self.module.get_shop_name_list(value)

    def __extract_product_id(self, product_info: List[dict[str, Any]]) -> List[str]:
        return [row["productId"] for row in product_info if row["productId"] != "-"]


class DataModule(Protocol):
    def admin_filter_query(self, value: str) -> Tuple:
        ...

    async def get_shop_name_list(self, value: str) -> List[str]:
        ...


class CandidateTableBrandModule:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def admin_filter_query(self, value: str):
        return (ShopProductCardTable.brand_name.like(f"{value}%"),)

    async def get_shop_name_list(self, value: str) -> List[str]:
        stmt = select(ShopProductCardTable.shop_name).where(
            ShopProductCardTable.brand_name.like(f"{value}%")
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()


class CandidateTableShopNameModule:
    def admin_filter_query(self, value: str):
        return (ShopProductCardTable.shop_name == value,)

    async def get_shop_name_list(self, value: str):
        return [value]


class CostTableBrandModule(CandidateTableBrandModule):
    def admin_filter_query(self, value: str):
        return (
            ShopProductCardTable.brand_name.like(f"{value}%"),
            ShopProductCardTable.candidate != 0,
        )


class CostTableShopNameModule(CandidateTableShopNameModule):
    def admin_filter_query(self, value: str):
        return (
            ShopProductCardTable.shop_name == value,
            ShopProductCardTable.candidate != 0,
        )


class TableModuleFactory:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def candidate_table_brand_name(self):
        return CandidateTableBrandModule(self.db)

    def candidate_table_shop_name(self):
        return CandidateTableShopNameModule()

    def cost_table_brand_name(self):
        return CostTableBrandModule(self.db)

    def cost_table_shop_name(self):
        return CostTableShopNameModule()
