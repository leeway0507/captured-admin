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
async def ScrapPage():
    yield PlatformPageMain(current_path, platform_list_path)


# @pytest.mark.anyio
# async def test_kream_id_type(ScrapPage: PlatformPageMain):
#     await ScrapPage.kream_execute("kreamId", "74749,76479", num_processor=2)


# @pytest.mark.anyio
# async def test_scrapDate_type(ScrapPage: PlatformPageMain):
#     await ScrapPage.init_pw_kream_scraper("scrapDate", "lastScrap", num_processor=6)
#     await ScrapPage.execute()


@pytest.mark.anyio
async def test_check_None_to_lastScrape(
    ScrapPage: PlatformPageMain,
):
    ScrapPage.set_values("scrapDate", None)

    assert (ScrapPage.searchType, ScrapPage.value) == ("scrapDate", "lastScrap")


@pytest.mark.anyio
async def test_check_value_is_lastScrap(
    ScrapPage: PlatformPageMain,
):
    ScrapPage.set_values("kreamId", "74749")

    assert (ScrapPage.searchType, ScrapPage.value) == ("kreamId", "74749")


@pytest.mark.anyio
async def test_check_value_is_lastScrap_error(
    ScrapPage: PlatformPageMain,
):
    with pytest.raises(ValueError):
        ScrapPage.set_values("kreamId", None)


@pytest.mark.anyio
async def test_extract_folder_name_and_target_data_kream_id(
    ScrapPage: PlatformPageMain,
):
    ScrapPage.set_values("kreamId", "74749")
    result = ScrapPage.extract_folder_name_and_target_data()

    assert result == ("kream_id", ["74749"])


@pytest.mark.anyio
async def test_get_target_list_by_scrap_date(ScrapPage: PlatformPageMain):
    ScrapPage.set_values("scrapDate", "lastScrap")
    target_list = ScrapPage.get_target_list_by_scrap_date()
    assert isinstance(target_list[0], int)


@pytest.mark.anyio
async def test_get_brand_name_by_scrap_date(ScrapPage: PlatformPageMain):
    ScrapPage.set_values("scrapDate", "lastScrap")
    folder_name = ScrapPage.get_brand_name_by_scrap_date()

    assert folder_name == "the north face"


@pytest.mark.anyio
async def test_extract_folder_name_and_target_data_scrapDate(
    ScrapPage: PlatformPageMain,
):
    ScrapPage.set_values("scrapDate", "lastScrap")
    result = ScrapPage.extract_folder_name_and_target_data()

    assert isinstance(result, tuple)
