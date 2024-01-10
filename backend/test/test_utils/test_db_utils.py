import os
import pytest
import pandas as pd
from test.db_utils import TestDB
from sqlalchemy import select
from db import tables_kream, tables_shop, tables_production

current_path = __file__.rsplit("/", 1)[0]

batch_time = "20240109-123456"


@pytest.fixture(scope="module")
def Test_DB():
    yield TestDB(current_path, batch_time)


def test_sync_last_update(Test_DB: TestDB):
    Test_DB.sync_last_data()


# def test_load_shop_info_data(Test_DB: TestDB):
#     data = Test_DB._load_shop_info_data()

#     assert isinstance(data[0], dict)


# def test_sync_shop_info_data(Test_DB: TestDB):
#     Test_DB._drop_test_table()
#     Test_DB._create_test_table()
#     Test_DB._sync_shop_info_data_from_admin_table()

#     stmt = select(tables_shop.ShopInfoTable)
#     result = Test_DB.test_db.execute(stmt)
#     result = result.all()
#     print(result[0])
#     assert isinstance(result, list)


# def test_sync_shop_data_from_batch_data(Test_DB: TestDB):
#     Test_DB._drop_test_table()
#     Test_DB._create_test_table()
#     Test_DB._sync_shop_info_data_from_admin_table()
#     Test_DB._sync_shop_data_from_batch_data()
