import os
import pytest
from platform_scrap.page.main import PlatformPageMain

current_path = __file__.rsplit("/", 1)[0]
platform_list_path = os.path.join(current_path.rsplit("/", 1)[0], "list")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def KreamPage():
    yield PlatformPageMain(current_path, platform_list_path)


@pytest.mark.anyio
async def test_kream_id_type(KreamPage: PlatformPageMain):
    await KreamPage.init_pw_kream_scraper("kreamId", "74749,76479", num_processor=2)
    await KreamPage.execute()


# @pytest.mark.anyio
# async def test_scrapDate_type(KreamPage: PlatformPageMain):
#     await KreamPage.init_pw_kream_scraper("scrapDate", "lastScrap", num_processor=6)
#     await KreamPage.execute()


@pytest.mark.anyio
async def test_extract_folder_name_and_target_data_kream_id(
    KreamPage: PlatformPageMain,
):
    KreamPage.set_values("kreamId", "74749")
    result = KreamPage.extract_folder_name_and_target_data()

    assert result == ("kream_id", ["74749"])


@pytest.mark.anyio
async def test_get_target_list_by_scrap_date(KreamPage: PlatformPageMain):
    KreamPage.set_values("scrapDate", "lastScrap")
    target_list = KreamPage.get_target_list_by_scrap_date()
    assert isinstance(target_list[0], int)


@pytest.mark.anyio
async def test_get_brand_name_by_scrap_date(KreamPage: PlatformPageMain):
    KreamPage.set_values("scrapDate", "lastScrap")
    folder_name = KreamPage.get_brand_name_by_scrap_date()

    assert folder_name == "the north face"


@pytest.mark.anyio
async def test_extract_folder_name_and_target_data_scrapDate(
    KreamPage: PlatformPageMain,
):
    KreamPage.set_values("scrapDate", "lastScrap")
    result = KreamPage.extract_folder_name_and_target_data()

    assert isinstance(result, tuple)
