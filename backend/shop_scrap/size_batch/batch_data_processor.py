import os
from typing import List, Dict, Any

import pandas as pd
from sqlalchemy import select
from db.tables_shop import ShopProductSizeTable, ShopProductCardTable
from db.tables_production import ProductInfoTable
from components.file_manager import FileManager
from sqlalchemy.orm import sessionmaker


class SizeBatchProcessor:  # BatchMaker
    def __init__(
        self,
        admin_session: sessionmaker,
        prod_session: sessionmaker,
        path: str,
        batch_time: str,
    ):
        self.admin_session = admin_session
        self.prod_session = prod_session
        self.batch_time = batch_time
        self.path = path

    async def execute(self):
        self.create_batch_folder()
        await self.save_db_data()
        self.load_db_data()
        self.create_prod_size_data()

    def create_batch_folder(self):
        batch_path = os.path.join(self.path, self.batch_time)
        FileManager.create_folder(batch_path)

    async def save_db_data(self):
        await self.save_shop_size_data()
        await self.save_shop_card_data()
        await self.save_prod_card_data()

    async def save_shop_size_data(self):
        data = await self._shop_size_data()
        self._save_data_to_parquet("batch_shop_size_data", data)

    async def _shop_size_data(self):
        stmt = (
            select(ShopProductSizeTable)
            .join(ShopProductCardTable)
            .where(ShopProductCardTable.candidate == 2)
        )
        return await self._execute_stmt(self.admin_session, stmt)

    async def save_shop_card_data(self):
        data = await self._shop_card_data()
        self._save_data_to_parquet("batch_shop_card_data", data)

    async def _shop_card_data(self):
        stmt = select(ShopProductCardTable).where(
            ShopProductCardTable.candidate == 2, ShopProductCardTable.sold_out == False
        )
        return await self._execute_stmt(self.admin_session, stmt)

    async def save_prod_card_data(self):
        data = await self._prod_card_data()
        self._save_data_to_parquet("batch_prod_card_data", data)

    async def _prod_card_data(self):
        stmt = select(ProductInfoTable).where(
            ProductInfoTable.deploy != -1,
        )
        return await self._execute_stmt(self.prod_session, stmt)

    async def _execute_stmt(self, session, stmt: Any) -> List[Dict]:
        async with session() as db:
            result = await db.execute(stmt)
            result = result.scalars().all()

        return [row.to_dict() for row in result]

    def _save_data_to_parquet(self, file_name: str, data: List[Dict]):
        pd.DataFrame(data).to_parquet(
            os.path.join(self.path, self.batch_time, file_name + ".parquet.gzip"),
            index=False,
            compression="gzip",
        )

    def load_db_data(self):
        self.shop_size_data_df = self._load_db_data("batch_shop_size_data")
        self.shop_card_data_df = self._load_db_data("batch_shop_card_data")
        self.prod_card_data_df = self._load_db_data("batch_prod_card_data")

    def _load_db_data(self, file_name: str):
        file_path = os.path.join(
            self.path, self.batch_time, file_name + ".parquet.gzip"
        )
        return pd.read_parquet(file_path)

    def create_prod_size_data(self):
        sku_prod_id_map_df = self.generate_id_map()
        size_batch_df = pd.merge(
            sku_prod_id_map_df,
            self.shop_size_data_df,
            on="shop_product_card_id",
            how="left",
        )
        size_batch_df = self.preprocess_size_batch_df(size_batch_df)
        self._save_data_to_parquet(
            "batch_prod_size_data", size_batch_df.to_dict("records")
        )

    def generate_id_map(self):
        sku_prod_id = self.prod_card_data_df[["sku", "product_id"]]
        sh_prod_id_prod_id = self.shop_card_data_df[
            ["product_id", "shop_product_card_id"]
        ]
        return pd.merge(sh_prod_id_prod_id, sku_prod_id, on="product_id", how="inner")

    def preprocess_size_batch_df(self, size_batch_df: pd.DataFrame):
        df = size_batch_df[["sku", "kor_product_size", "updated_at"]]
        df = df.drop_duplicates(subset=["sku", "kor_product_size"])  # type: ignore
        df["available"] = 1
        df.rename(columns={"kor_product_size": "size"}, inplace=True)
        return df
