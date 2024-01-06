import os
import pytest

from env import dev_env, get_path

from components.dev.platform.page import PlatformPageScraper
from components.dev.platform.list import PlatformListScraper
from components.dev.platform.platform_browser_controller import (
    PwKreamBrowserController,
)

platform_list_path = get_path("platform_list")
platform_page_path = get_path("platform_page")


@pytest.fixture(scope="module")
def list_scraper():
    return PlatformListScraper(platform_list_path)


@pytest.fixture(scope="module")
def page_scraper():
    return PlatformPageScraper(platform_page_path)


def test_load_platform_list_get_report_list(list_scraper: PlatformListScraper):
    # When
    report_list = list_scraper.Report.get_report_list()

    # Then
    assert report_list[0].split("-")[-1] == "kream"


def test_get_platform_list_report(list_scraper: PlatformListScraper):
    """platform list 수집 보고서 조회"""
    scrapName = "231222-145213"
    list_scraper.Report.report_file_name = scrapName + "-kream"
    report = list_scraper.Report.load_report()

    assert list(report) == [
        "scrap_time",
        "num_of_plan",
        "num_process",
        "scrap_log",
        "db_update",
    ]


# def test_load_platform_page_get_report_list(page_scraper: PlatformPageScraper):
#     # When
#     report_list = page_scraper.Report.get_report_list()

#     # Then

#     assert report_list[0].split("-")[-1] == "kream"


# def test_get_platform_page_report(page_scraper: PlatformPageScraper):
#     """platform page 수집 보고서 조회"""
#     scrapName = "231218-232939"
#     page_scraper.Report.report_file_name = scrapName + "-kream"
#     report = page_scraper.Report.load_report()


@pytest.mark.asyncio
async def test_save_last_scrap_list_data(list_scraper: PlatformListScraper):
    time = list_scraper.set_scrap_time()
    list_scraper.scrap_folder_name = "test_last_scrap_list_data"
    list_scraper.platform_type = "kream"
    await list_scraper.save_scrap_data()
    assert os.path.exists(
        os.path.join(
            platform_list_path,
            "kream",
            "test_last_scrap_list_data",
            time + "-product_card_list.parquet.gzip",
        )
    )


@pytest.mark.asyncio
async def test_save_last_scrap_page_data(page_scraper: PlatformPageScraper):
    time = page_scraper.set_scrap_time()
    page_scraper.scrap_folder_name = "test_last_scrap_page_data"
    await page_scraper.save_scrap_data()
