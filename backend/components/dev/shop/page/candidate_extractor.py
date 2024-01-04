from typing import Protocol, List, Any, TypeVar
from sqlalchemy import select
from db.tables_shop import ShopProductCardTable
from db.dev_db import session_local
from model.db_model_shop import ShopProductCardSchema as schema
from enum import Enum
from db.tables_shop import MyBase


class SearchType(Enum):
    ALL = "all"
    PRODUCT_ID = "productId"
    SHOP_PRODUCT_CARD_ID = "shopProductCardId"
    SHOP_NAME = "shopName"


class CandidateExtractor(Protocol):
    async def extract_data(self, search_type: SearchType, value: str) -> List[schema]:
        ...


class RDBCandidateExtractor:
    async def extract_data(self, search_type: SearchType, value: str) -> List[schema]:
        stmt = SearchTypeHandler(search_type, value).get_stmt()
        result = await self.execute_stmt(stmt)
        return [schema(**r.to_dict()) for r in result]

    async def execute_stmt(self, statement) -> List[MyBase]:
        async with session_local() as session:  # type: ignore
            result = await session.execute(statement)
            return result.scalars().all()


class SearchTypeHandler:
    def __init__(self, search_type: SearchType, value: str):
        self.search_type = search_type
        self.value = value

    def get_stmt(self):
        match self.search_type:
            case SearchType.ALL:
                value = self.str_to_int(self.value)
                return AllStmt().get_stmt(value)

            case SearchType.PRODUCT_ID:
                value = self.str_to_list(self.value)
                return ProductIdStmt().get_stmt(value)

            case SearchType.SHOP_PRODUCT_CARD_ID:
                value = self.str_to_list(self.value)
                return ShopProductCardIdStmt().get_stmt(value)

            case SearchType.SHOP_NAME:
                value = self.str_to_list(self.value)
                return ShopNameStmt().get_stmt(value)

    def str_to_list(self, v: str):
        return v.split(",")

    def str_to_int(self, v: str):
        return int(v)


class SearchTypeStmt(Protocol):
    def get_stmt(self, value) -> Any:
        ...


class AllStmt:
    def get_stmt(self, value: int):
        return (
            select(ShopProductCardTable)
            .where(ShopProductCardTable.candidate == 2)
            .limit(value)
        )


class ProductIdStmt:
    def get_stmt(self, value: List[str]):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2,
            ShopProductCardTable.product_id.in_(value),
        )


class ShopProductCardIdStmt:
    def get_stmt(self, value: List[str]):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2,
            ShopProductCardTable.shop_product_card_id.in_(value),
        )


class ShopNameStmt:
    def get_stmt(self, value: List[str]):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2,
            ShopProductCardTable.shop_name.in_(value),
        )
