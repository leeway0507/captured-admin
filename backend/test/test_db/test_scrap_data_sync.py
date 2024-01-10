import pytest
from db.scrap_data_sync_db import (
    ShopPageDataSyncDB,
    ShopListDataSyncDB,
    SizeDataSyncProdDB,
)


current_path = __file__.rsplit("/", 1)[0]
shop_list_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/test_shop_scrap/test_list"
)
# shop_page_path = (
#     "/Users/yangwoolee/repo/captured/admin/backend/test/test_shop_scrap/test_page"
# )
shop_page_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/test_shop_scrap/test_size_batch"
)
pytestmark = pytest.mark.asyncio(scope="module")


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def ShopPageSyncDB(test_session):
    yield ShopPageDataSyncDB(test_session, shop_page_path, "20240110-145730")


@pytest.mark.anyio
async def test_ScrapDataSyncDB_load_db_data(test_session):
    # Given
    SyncDB = ShopListDataSyncDB(test_session, shop_list_path, "20240107-215804")

    # When
    data = SyncDB._load_db_data("20240107-215804")

    # Then
    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_sync_shop_list(test_session):
    # Given
    SyncDB = ShopListDataSyncDB(test_session, shop_list_path, "20240107-215804")
    await SyncDB.sync_data()


@pytest.mark.anyio
async def test_ShopPage_get_unique_id(ShopPageSyncDB: ShopPageDataSyncDB):
    data = ShopPageSyncDB._load_db_data("20240110-145730-size")
    assert ShopPageSyncDB.get_unique_id(data)[0] == 4096


@pytest.mark.anyio
async def test_sync_page_get_card_info_without_prod_id(
    ShopPageSyncDB: ShopPageDataSyncDB,
):
    data = ShopPageSyncDB._load_db_data("20240110-145730-card_info")
    print(ShopPageSyncDB.get_card_info_without_prod_id(data))


@pytest.mark.anyio
async def test_sold_out_items(ShopPageSyncDB: ShopPageDataSyncDB):
    assert isinstance(ShopPageSyncDB.sold_out_items(), list)


@pytest.mark.anyio
async def test_sync_shop_page(ShopPageSyncDB: ShopPageDataSyncDB):
    await ShopPageSyncDB.sync_data()


@pytest.mark.anyio
async def test_sync_prodDB(test_session):
    SyncDB = SizeDataSyncProdDB(
        test_session,
        test_session,
        shop_page_path,
        "20240110-145730",
    )
    await SyncDB.sync_to_dev()


# product_info = [
# key: shop_product_card_id
# value: product_id
# ]
