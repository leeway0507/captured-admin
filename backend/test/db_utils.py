from sqlalchemy import create_engine
from components.env import dev_env
from db import tables_kream, tables_shop, tables_production
from sqlalchemy import select, insert
import os
import pandas as pd


def sync_admin_engine():
    username = dev_env.DB_USER_NAME
    password = dev_env.DB_PASSWORD
    host = dev_env.DB_HOST
    db_name = dev_env.DB_NAME

    db_url = f"mysql+pymysql://{username}:{password}@{host}:3306/{db_name}"
    return create_engine(db_url)


def sync_test_engine():
    username = dev_env.DB_USER_NAME
    password = dev_env.DB_PASSWORD
    host = dev_env.DB_HOST
    db_name = dev_env.TEST_DB_NAME

    db_url = f"mysql+pymysql://{username}:{password}@{host}:3306/{db_name}"
    return create_engine(db_url)


class TestDB:
    def __init__(self, path: str, folder_name: str) -> None:
        self.admin_db = sync_admin_engine()
        self.test_db = sync_test_engine()
        self.path = path
        self.folder_name = folder_name

    def sync_last_data(self):
        self._drop_test_table()
        self._create_test_table()
        self._sync_last_batch()

    def _drop_test_table(self):
        db = self.test_db
        # tables_kream.KreamProductIdBridgeTable.__table__.drop(db)  # type:ignore
        # tables_kream.KreamBuyAndSellTable.__table__.drop(db)  # type:ignore
        # tables_kream.KreamTradingVolumeTable.__table__.drop(db)  # type:ignore
        # tables_kream.KreamProductCardTable.__table__.drop(db)  # type:ignore
        # tables_shop.ShopInBrandTable.__table__.drop(db)  # type:ignore

        tables_shop.ShopProductSizeTable.__table__.drop(db)  # type:ignore
        tables_shop.ShopProductCardTable.__table__.drop(db)  # type:ignore
        tables_shop.ShopInfoTable.__table__.drop(db)  # type:ignore

        tables_production.SizeTable.__table__.drop(db)  # type:ignore
        tables_production.ProductInfoTable.__table__.drop(db)  # type:ignore

    def _create_test_table(self):
        db = self.test_db
        # tables_kream.KreamProductCardTable.__table__.create(db)  # type:ignore
        # tables_kream.KreamTradingVolumeTable.__table__.create(db)  # type:ignore
        # tables_kream.KreamBuyAndSellTable.__table__.create(db)  # type:ignore
        # tables_kream.KreamProductIdBridgeTable.__table__.create(db)  # type:ignore
        # tables_shop.ShopInBrandTable.__table__.create(db)  # type:ignore

        tables_shop.ShopInfoTable.__table__.create(db)  # type:ignore
        tables_shop.ShopProductCardTable.__table__.create(db)  # type:ignore
        tables_shop.ShopProductSizeTable.__table__.create(db)  # type:ignore

        tables_production.ProductInfoTable.__table__.create(db)  # type:ignore
        tables_production.SizeTable.__table__.create(db)  # type:ignore

    def _sync_last_batch(self):
        self._sync_shop_info_data_from_admin_table()
        self._sync_shop_data_from_batch_data()

    def _sync_shop_info_data_from_admin_table(self):
        data = self._load_shop_info_data()
        stmt = insert(tables_shop.ShopInfoTable).values(data)
        self.test_db.execute(stmt)

    def _load_shop_info_data(self):
        stmt = select(tables_shop.ShopInfoTable)
        result = self.admin_db.execute(stmt)
        return [dict(r) for r in result.all()]

    def _sync_shop_data_from_batch_data(self):
        self._sync_shop_card_data()
        self._sync_shop_size_data()
        self._sync_prod_card_data()
        self._sync_prod_size_data()

    def _sync_shop_size_data(self):
        data = self._load_db_data("shop_size_data")
        stmt = insert(tables_shop.ShopProductSizeTable).values(data)
        self.test_db.execute(stmt)

    def _sync_shop_card_data(self):
        data = self._load_db_data("shop_card_data")
        stmt = insert(tables_shop.ShopProductCardTable).values(data)
        self.test_db.execute(stmt)

    def _sync_prod_card_data(self):
        data = self._load_db_data("prod_card_data")
        stmt = insert(tables_production.ProductInfoTable).values(data)
        self.test_db.execute(stmt)

    def _sync_prod_size_data(self):
        data = self._load_db_data("prod_size_data")
        stmt = insert(tables_production.SizeTable).values(data)
        self.test_db.execute(stmt)

    def _load_db_data(self, file_name: str):
        file_path = os.path.join(
            self.path, self.folder_name, file_name + ".parquet.gzip"
        )
        return pd.read_parquet(file_path).to_dict("records")
