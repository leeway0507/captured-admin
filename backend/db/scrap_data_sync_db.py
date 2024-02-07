import os
from typing import List, Dict
import pandas as pd

from db.tables_shop import ShopProductCardTable, ShopProductSizeTable
from db.tables_production import SizeTable, ProductInfoTable
from db.tables_kream import (
    KreamProductCardTable,
    KreamBuyAndSellTable,
    KreamProductIdBridgeTable,
    KreamTradingVolumeTable,
)
from model.db_model_shop import ShopProductSizeSchema

from sqlalchemy.dialects.mysql import insert
from sqlalchemy import delete, update, bindparam, and_, delete, null, or_
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
from components.file_manager import ScrapReport


def load_sync_db(file_name) -> type["ScrapDataSyncDB"]:
    return getattr(ScrapDataSyncDBFactory(), file_name)()


class ScrapDataSyncDBFactory:
    def platform_list(self) -> type["PlatformListDataSyncDB"]:
        return PlatformListDataSyncDB

    def platform_page(self) -> type["PlatformPageDataSyncDB"]:
        return PlatformPageDataSyncDB

    def shop_list(self) -> type["ShopListDataSyncDB"]:
        return ShopListDataSyncDB

    def shop_page(self) -> type["ShopPageDataSyncDB"]:
        return ShopPageDataSyncDB

    def size_batch(self) -> type["SizeDataSyncProdDB"]:
        return SizeDataSyncProdDB


class ScrapDataSyncDB(ABC):
    def __init__(self, session: sessionmaker, path: str) -> None:
        self.session = session
        self.path = path
        self.Report = ScrapReport(os.path.join(self.path, "_report"))
        self._scrap_time = None

    @property
    def scrap_time(self):
        if self._scrap_time:
            return self._scrap_time
        raise (ValueError("self._scrap_time is None"))

    @scrap_time.setter
    def scrap_time(self, scrap_time: str):
        self._scrap_time = scrap_time
        self.Report.report_file_name = scrap_time

    async def execute(self, stmt):
        async with self.session() as db:  # type:ignore
            await db.execute(stmt)
            await db.commit()

    @abstractmethod
    async def sync_data(self): ...

    def _load_db_data(self, file_name: str):
        folder_path = self.get_folder_path()
        file_path = os.path.join(folder_path, file_name + ".parquet.gzip")
        return pd.read_parquet(file_path).to_dict("records")

    @abstractmethod
    def get_folder_path(self) -> str: ...

    def get_report_data(self):
        return self.Report.get_report()


class PlatformListDataSyncDB(ScrapDataSyncDB):
    async def sync_data(self):
        data = super()._load_db_data(self.scrap_time)
        await super().execute(self.insert_shop_card(data))
        self.Report.update_report({"db_update": True})

    def get_folder_path(self):
        return os.path.join(self.path, "kream")

    def insert_shop_card(self, data: List[Dict]):
        stmt = insert(KreamProductCardTable).values(data)
        stmt = stmt.on_duplicate_key_update(
            trading_volume=stmt.inserted.trading_volume,
            wish=stmt.inserted.wish,
            review=stmt.inserted.review,
            updated_at=stmt.inserted.updated_at,
        )
        return stmt


class PlatformPageDataSyncDB(ScrapDataSyncDB):
    def get_folder_path(self):
        report_data = super().get_report_data()
        return os.path.join(self.path, report_data["folder_name"])

    async def sync_data(self):
        await self.sync_buy_and_sell()
        await self.sync_product_detail()
        await self.sync_trading_volume()
        await self.sync_product_bridge()
        self.Report.update_report({"db_update": True})

    async def sync_buy_and_sell(self):
        data = super()._load_db_data(self.scrap_time + "-buy_and_sell")
        await super().execute(self.insert_buy_and_sell(data))

    def insert_buy_and_sell(self, data: List[Dict]):
        stmt = insert(KreamBuyAndSellTable).values(data)
        stmt = stmt.on_duplicate_key_update(
            buy=stmt.inserted.buy,
            sell=stmt.inserted.sell,
            updated_at=stmt.inserted.updated_at,
        )
        return stmt

    async def sync_product_detail(self):
        data = super()._load_db_data(self.scrap_time + "-product_detail")
        await super().execute(self.insert_product_detail(data))

    def insert_product_detail(self, data: List[Dict]):
        stmt = insert(KreamProductCardTable).values(data)
        stmt = stmt.on_duplicate_key_update(
            retail_price=stmt.inserted.retail_price,
            product_release_date=stmt.inserted.product_release_date,
            color=stmt.inserted.color,
            updated_at=stmt.inserted.updated_at,
        )
        return stmt

    async def sync_trading_volume(self):
        data = super()._load_db_data(self.scrap_time + "-trading_volume")
        await super().execute(self.insert_trading_volume(data))

    def insert_trading_volume(self, data: List[Dict]):
        stmt = insert(KreamTradingVolumeTable).values(data)
        return stmt

    async def sync_product_bridge(self):
        data = super()._load_db_data(self.scrap_time + "-product_bridge")
        await super().execute(self.insert_product_bridge(data))

    def insert_product_bridge(self, data: List[Dict]):
        stmt = insert(KreamProductIdBridgeTable).values(data).prefix_with("IGNORE")
        return stmt


class ShopListDataSyncDB(ScrapDataSyncDB):
    async def sync_data(self):
        data = super()._load_db_data(self.scrap_time)
        await super().execute(self.insert_shop_card(data))
        self.Report.update_report({"db_update": True})

    def get_folder_path(self):
        report_data = super().get_report_data()
        return os.path.join(self.path, report_data["shop_name"])

    def insert_shop_card(self, data: List[Dict]):
        stmt = insert(ShopProductCardTable).values(data)
        stmt = stmt.on_duplicate_key_update(
            kor_price=stmt.inserted.kor_price,
            us_price=stmt.inserted.us_price,
            original_price=stmt.inserted.original_price,
            updated_at=stmt.inserted.updated_at,
        )
        return stmt


class ShopPageDataSyncDB(ScrapDataSyncDB):
    def get_folder_path(self):
        return os.path.join(self.path, self.scrap_time)

    async def sync_data(self):
        await self.delete_shop_size()
        await self.insert_shop_size()
        await self.upsert_card_info()
        await self.update_product_id()
        await self.update_sold_out_status()
        self.Report.update_report({"db_update": True})

    async def delete_shop_size(self):
        data = super()._load_db_data("shop_scrap_page_size_data")
        unique_id = self.get_unique_id(data)
        await super().execute(self.delete_shop_size_stmt(unique_id))

    def get_unique_id(self, data: List[Dict]):
        return list(set(map(lambda x: x["shop_product_card_id"], data)))

    def delete_shop_size_stmt(self, unique_id: List):
        stmt = delete(ShopProductSizeTable).where(
            ShopProductSizeTable.shop_product_card_id.in_(unique_id)
        )
        return stmt

    async def insert_shop_size(self):
        data = super()._load_db_data("shop_scrap_page_size_data")
        size_data = self.get_size(data)
        await super().execute(self.insert_shop_size_stmt(size_data))

    def get_size(self, data: List[Dict]):
        return [ShopProductSizeSchema(**row).model_dump() for row in data]

    def insert_shop_size_stmt(self, size_data: List):
        return insert(ShopProductSizeTable).values(size_data)

    async def upsert_card_info(self):
        data = super()._load_db_data("shop_scrap_page_card_data")
        card_info_without_prod_id = self.get_card_info_without_prod_id(data)
        await super().execute(self.upsert_card_info_stmt(card_info_without_prod_id))

    def get_card_info_without_prod_id(self, data: List[Dict]):
        for item in data:
            item.pop("product_id")
        return data

    def upsert_card_info_stmt(self, card_info_without_prod_id: List):
        stmt = insert(ShopProductCardTable).values(card_info_without_prod_id)
        stmt = stmt.on_duplicate_key_update(
            original_price_currency=stmt.inserted.original_price_currency,
            original_price=stmt.inserted.original_price,
            us_price=stmt.inserted.us_price,
            kor_price=stmt.inserted.kor_price,
            updated_at=stmt.inserted.updated_at,
        )
        return stmt

    async def update_product_id(self):
        data = super()._load_db_data("shop_scrap_page_card_data")
        product_info = self.get_data_for_update_product_id(data)
        await self.execute_for_update_product_id(
            self.update_product_id_stmt(),
            product_info,
        )

    def get_data_for_update_product_id(self, data: List[Dict]):
        return list(
            map(
                lambda x: {"key": x["shop_product_card_id"], "value": x["product_id"]},
                data,
            )
        )

    async def execute_for_update_product_id(self, stmt, data):
        async with self.session() as db:  # type:ignore
            await db.execute(stmt, data)
            await db.commit()

    def update_product_id_stmt(self):
        stmt = (
            update(ShopProductCardTable)
            .where(
                ShopProductCardTable.shop_product_card_id == bindparam("key"),
                or_(
                    ShopProductCardTable.product_id == null(),
                    ShopProductCardTable.product_id == "-",
                ),
            )
            .values(product_id=bindparam("value"))
        )
        return stmt

    async def update_sold_out_status(self):
        sold_out_item_id = self.sold_out_items()
        await super().execute(self.update_sold_out_items_stmt(sold_out_item_id))

    def sold_out_items(self):
        self.Report.report_file_name = self.scrap_time
        scrap_report = self.Report.get_report()
        jobs = scrap_report["job"]
        return [
            job["shop_product_card_id"] for job in jobs if job["status"] != "success"
        ]

    def update_sold_out_items_stmt(self, data: List):
        stmt = (
            update(ShopProductCardTable)
            .where(ShopProductCardTable.shop_product_card_id.in_(data))
            .values(sold_out=1, candidate=0)
        )
        return stmt


class SizeDataSyncProdDB(ScrapDataSyncDB):
    def __init__(
        self,
        dev_session: sessionmaker,
        prod_session: sessionmaker,
        path: str,
        scrap_time: str,
    ) -> None:
        super().__init__(dev_session, path)
        self.prod_session = prod_session
        self.scrap_time = scrap_time

    def get_folder_path(self):
        return os.path.join(self.path, self.scrap_time)

    async def sync_data(self):
        await self.sync_to_dev()
        await self.sync_to_prod()

    async def sync_to_prod(self):
        await self.execute_prod(self.prepare_to_insert_prod_size())

        data = super()._load_db_data("batch_prod_size_data")
        await self.execute_prod(self.insert_prod_size(data))

    def insert_prod_size(self, data: List[Dict]):
        stmt = insert(SizeTable).values(data)
        stmt = stmt.on_duplicate_key_update(
            available=stmt.inserted.available,
            updated_at=stmt.inserted.updated_at,
        )

        return stmt

    def prepare_to_insert_prod_size(self):
        stmt = update(SizeTable).values(available=0)
        return stmt

    async def sync_to_dev(self):
        await super().execute(self.prepare_to_insert_prod_size())

        data = super()._load_db_data("batch_prod_card_data")
        await super().execute(self.insert_prod_card(data))

        data = super()._load_db_data("batch_prod_size_data")
        await super().execute(self.insert_prod_size(data))

    def insert_prod_card(self, data: List[Dict]):
        stmt = insert(ProductInfoTable).values(data)
        update_dict = {x.name: x for x in stmt.inserted}
        stmt = stmt.on_duplicate_key_update(**update_dict)
        return stmt

    async def execute_prod(self, stmt):
        async with self.prod_session() as db:  # type:ignore
            await db.execute(stmt)
            await db.commit()
