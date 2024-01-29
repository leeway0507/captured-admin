import pytest
from db.scrap_data_sync_db import (
    ShopPageDataSyncDB,
    ShopListDataSyncDB,
    SizeDataSyncProdDB,
)
from db.dev_db import admin_session_local


current_path = __file__.rsplit("/", 1)[0]
shop_list_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/test_shop_scrap/test_list"
)
shop_page_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/test_shop_scrap/test_page/data"
)

kream_list_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/test_platform_scrap/list"
)

kream_page_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/test_platform_scrap/page"
)

pytestmark = pytest.mark.asyncio(scope="module")


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


# ## Shop List

# @pytest.mark.anyio
# async def test_ScrapDataSyncDB_load_db_data(test_session):
#     # Given
#     SyncDB = ShopListDataSyncDB(test_session, shop_list_path, "20240107-215804")

#     # When
#     data = SyncDB._load_db_data("20240107-215804")

#     # Then
#     assert isinstance(data[0], dict)


# @pytest.mark.anyio
# async def test_sync_shop_list(test_session):
#     # Given
#     SyncDB = ShopListDataSyncDB(test_session, shop_list_path, "20240107-215804")
#     await SyncDB.sync_data()


# shop_page
@pytest.fixture(scope="module")
def ShopPageSyncDB(test_session):
    sync_db = ShopPageDataSyncDB(admin_session_local, shop_page_path)
    sync_db.scrap_time = "20240123-000452"
    yield sync_db


# @pytest.mark.anyio
# async def test_ShopPage_get_unique_id(ShopPageSyncDB: ShopPageDataSyncDB):
#     data = ShopPageSyncDB._load_db_data("20240110-145730-size")
#     assert ShopPageSyncDB.get_unique_id(data)[0] == 4096


@pytest.mark.anyio
async def test_sync_page_get_card_info_without_prod_id(
    ShopPageSyncDB: ShopPageDataSyncDB,
):
    data = ShopPageSyncDB._load_db_data("shop_scrap_page_card_data")
    print(ShopPageSyncDB.get_card_info_without_prod_id(data))


@pytest.mark.anyio
async def test_sold_out_items(ShopPageSyncDB: ShopPageDataSyncDB):
    print(ShopPageSyncDB.sold_out_items())
    assert isinstance(ShopPageSyncDB.sold_out_items(), list)


@pytest.mark.anyio
async def test_product_id(ShopPageSyncDB: ShopPageDataSyncDB):
    data = ShopPageSyncDB._load_db_data("shop_scrap_page_card_data")
    print(ShopPageSyncDB.get_data_for_update_product_id(data))


@pytest.mark.anyio
async def test_update_product_id(ShopPageSyncDB: ShopPageDataSyncDB):
    data = ShopPageSyncDB._load_db_data("shop_scrap_page_card_data")
    data = ShopPageSyncDB.get_data_for_update_product_id(data)
    await ShopPageSyncDB.update_product_id()


# @pytest.mark.anyio
# async def test_sync_shop_page(ShopPageSyncDB: ShopPageDataSyncDB):
#     await ShopPageSyncDB.sync_data()


# ## size_batch_sync
# @pytest.mark.anyio
# async def test_sync_prodDB(test_session):
#     SyncDB = SizeDataSyncProdDB(
#         test_session,
#         test_session,
#         shop_page_path,
#         "20240110-145730",
#     )
#     await SyncDB.sync_to_dev()


# product_info = [
# key: shop_product_card_id
# value: product_id
# ]
