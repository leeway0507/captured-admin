from typing import Protocol, List, Optional
from sqlalchemy import select
from db.tables_shop import ShopProductCardTable
from pydantic import BaseModel
from db.tables_shop import MyBase
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class TargetModel(BaseModel):
    shop_product_card_id: int
    product_url: str
    shop_name: str
    brand_name: str
    product_id: Optional[str]


class TargetExractor:
    def __init__(self, session: sessionmaker) -> None:
        self.strategy: TargetExtreactStrategy = AllStrategy
        self.session = session

    async def extract_data(self, value: str) -> List:
        result = await self.get_target_values(value)
        return [TargetModel(**r.to_dict()).model_dump() for r in result]

    async def get_target_values(self, value: str):
        target_value = self.strategy.convert_value(value)
        stmt = self.strategy.stmt(target_value)
        return await self.execute_stmt(stmt)

    async def execute_stmt(self, statement) -> List[MyBase]:
        async with self.session() as db:  # type: ignore
            result = await db.execute(statement)
            return result.scalars().all()


def load_target_strategy(target_name: str) -> "TargetExtreactStrategy":
    target_dict = {
        "all": AllStrategy,
        "product_id": ProductIdStrategy,
        "shop_product_card": ShopProductCardIdStrategy,
        "shop_name": ShopNameStrategy,
    }
    if not target_name in target_dict.keys():
        raise ValueError(f"{target_name} is not in {target_dict.keys()}")

    return target_dict[target_name]


class TargetExtreactStrategy(Protocol):
    @staticmethod
    def stmt(value):
        ...

    @staticmethod
    def convert_value(v: str) -> int | List[int]:
        ...


class AllStrategy:
    @staticmethod
    def stmt(value: int):
        return (
            (
                select(ShopProductCardTable).where(
                    ShopProductCardTable.candidate == 2,
                    ShopProductCardTable.sold_out == 0,
                )
            )
            .order_by(ShopProductCardTable.updated_at.asc())
            .limit(value)
        )

    @staticmethod
    def convert_value(v: str):
        return int(v)


class ProductIdStrategy:
    @staticmethod
    def stmt(value: List[str]):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2,
            ShopProductCardTable.sold_out == 0,
            ShopProductCardTable.product_id.in_(value),
        )

    @staticmethod
    def convert_value(v: str):
        return v.split(",")


class ShopProductCardIdStrategy:
    @staticmethod
    def stmt(value: List[str]):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2,
            ShopProductCardTable.sold_out == 0,
            ShopProductCardTable.shop_product_card_id.in_(value),
        )

    @staticmethod
    def convert_value(v: str):
        return v.split(",")


class ShopNameStrategy:
    @staticmethod
    def stmt(value: List[str]):
        return select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2,
            ShopProductCardTable.sold_out == 0,
            ShopProductCardTable.shop_name.in_(value),
        )

    @staticmethod
    def convert_value(v: str):
        return v.split(",")
