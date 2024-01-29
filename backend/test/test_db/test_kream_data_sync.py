import pytest
from db.scrap_data_sync_db import (
    PlatformPageDataSyncDB,
    PlatformListDataSyncDB,
)


current_path = __file__.rsplit("/", 1)[0]

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


@pytest.fixture(scope="module")
def PlatformListSyncDB(test_session):
    yield PlatformListDataSyncDB(test_session, kream_list_path, "20240120-151340")


@pytest.mark.anyio
async def test_ScrapDataSyncDB_load_db_data(PlatformListSyncDB: PlatformListDataSyncDB):
    # When
    data = PlatformListSyncDB._load_db_data("20240120-151340")
    print(data[0])
    # Then
    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_sync_shop_list(PlatformListSyncDB: PlatformListDataSyncDB):
    # Given
    await PlatformListSyncDB.sync_data()


@pytest.fixture(scope="module")
def PlatformPageSyncDB(test_session):
    yield PlatformPageDataSyncDB(test_session, kream_page_path, "20240120-155158")


@pytest.mark.anyio
async def test_PlatformPage_load_db_data(PlatformPageSyncDB: PlatformPageDataSyncDB):
    # When
    data = PlatformPageSyncDB._load_db_data("20240120-155158" + "-buy_and_sell")
    assert isinstance(data[0], dict)
    data = PlatformPageSyncDB._load_db_data("20240120-155158" + "-product_detail")
    assert isinstance(data[0], dict)
    data = PlatformPageSyncDB._load_db_data("20240120-155158" + "-trading_volume")
    assert isinstance(data[0], dict)
    data = PlatformPageSyncDB._load_db_data("20240120-155158" + "-product_bridge")
    assert isinstance(data[0], dict)

    print(data[0])


@pytest.mark.anyio
async def test_sync_PlatformPage(PlatformPageSyncDB: PlatformPageDataSyncDB):
    # Given
    await PlatformPageSyncDB.sync_data()
