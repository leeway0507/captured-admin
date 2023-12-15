import os
from typing import Protocol, List, Any, Optional

import pandas as pd
from sqlalchemy import select
from db.tables_kream import KreamProductCardTable, KreamProductIdBridgeTable
from db.dev_db import session_local
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum
from db.tables_shop import MyBase
from env import dev_env


class PageSearchType(Enum):
    LAST_SCRAP = "lastScrap"
    SKU = "sku"
    PRODUCT_ID = "productId"


class RDBExtractor:
    # TODO: 추후 신규 플랫폼 또는 DB도입 시 extendable하게 변경시켜야함.
    def __init__(self, product_id_list: List[str]):
        self.product_id_list = product_id_list

    async def extract_data(self) -> List[int]:
        stmt = self.get_stmt(self.product_id_list)
        result = await self.execute_stmt(stmt)
        print("RDBCandidateExtractor")
        print("RDBCandidateExtractor")
        print("RDBCandidateExtractor")
        print(result)
        print(result)
        return [r[0] for r in result]  # type: ignore

    async def execute_stmt(self, statement) -> List[MyBase]:
        async with session_local() as session:  # type: ignore
            result = await session.execute(statement)
            return result.scalars().all()

    def get_stmt(self, product_id_list: List[str]):
        return (
            select(KreamProductCardTable.kream_id)
            .join(KreamProductIdBridgeTable)
            .where(
                KreamProductIdBridgeTable.product_id.in_(product_id_list),
            )
        )


class LocalExtractor:
    def __init__(self, platform_type: str, file_name: Optional[str] = None):
        self.path = dev_env.PLATFORM_PRODUCT_LIST_DIR
        self.platform_path = os.path.join(self.path, platform_type)

        if file_name:
            self.file_name = file_name
        else:
            self.file_name = self._get_last_file_name()

    def extract_data(self) -> List[int]:
        file_path = os.path.join(self.platform_path, self.file_name)
        df = pd.read_parquet(file_path)
        return df["kream_id"].tolist()

    def _get_last_file_name(self) -> str:
        file_list = os.listdir(self.platform_path)
        file_list.sort()
        return file_list[-1]


class CandidateExtractor:
    def __init__(self, search_type: PageSearchType, value: str):
        self.search_type = search_type
        self.value = value

    async def extract_candidate(self):
        match self.search_type:
            case PageSearchType.LAST_SCRAP:
                return LocalExtractor(self.value).extract_data()

            case PageSearchType.SKU:
                return self.str_to_int_list(self.value)

            case PageSearchType.PRODUCT_ID:
                product_id_list = self.str_to_list(self.value)
                return await RDBExtractor(product_id_list).extract_data()

    def str_to_list(self, v: str):
        return v.split(",")

    def str_to_int_list(self, v: str):
        return [int(i) for i in v.split(",")]

    def str_to_int(self, v: str):
        return int(v)
