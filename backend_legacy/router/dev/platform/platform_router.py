"""dev Router"""
import os
from typing import Literal
from datetime import datetime

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from env import dev_env, get_path

from db.dev_db import get_dev_db


from components.dev.platform.platform_data_loader import *

from components.dev.platform.page import PlatformPageScraper
from components.dev.platform.page.sub_scraper import PwKreamPageSubScraper
from components.dev.platform.list import PlatformListScraper
from components.dev.platform.list.sub_scraper import PwKreamListSubScraper
from components.dev.platform.platform_browser_controller import (
    PwKreamBrowserController,
)
from components.dev.platform.utils import load_page_target_list


# from components.dev.platform.platform_db import (
#     get_kream_product_detail_list_from_db,
#     get_kream_product_size_info,
#     get_kream_product_color_for_registration,
# )

from components.dev.utils.file_manager import ScrapTempFile
from components.dev.utils.util import save_to_parquet

platform_router = APIRouter()

platform_list_path = get_path("platform_list")
platform_page_path = get_path("platform_page")


list_scraper = PlatformListScraper(platform_list_path)
page_scraper = PlatformPageScraper(platform_page_path)


@platform_router.get("/scrap-platform-list")
async def scrap_product_list(
    brandName: str,
    maxScroll: int,
    minWish: int,
    minVolume: int,
    numProcess: int = 1,
):
    """SCRAP PLATFORM LIST"""
    browser = await PwKreamBrowserController.start()
    # binding vars
    list_scraper.late_binding(browser, PwKreamListSubScraper(), numProcess, "kream")
    list_scraper.scrap_folder_name = brandName
    list_scraper.min_wish = minWish
    list_scraper.min_volume = minVolume
    list_scraper.target_list = brandName.split(",")

    return await list_scraper.scrap()


@platform_router.get("/scrap-platform-page")
async def scrap_product_page(
    searchType: Literal["kreamId", "scrapDate"],
    value: str,
    numProcess: int,
):
    """SCRAP PLATFORM PAGE"""
    browser = await PwKreamBrowserController.start()
    page_scraper.late_binding(browser, PwKreamPageSubScraper(), numProcess, "kream")
    page_scraper.target_list = load_page_target_list(searchType, value)

    return await page_scraper.scrap()


@platform_router.post("/save-last-product-card-list")
async def save_last_scrap_list_data():
    return await list_scraper.save_scrap_data()


@platform_router.get("/get-platform-list-report-list")
def get_platform_list_report_list():
    """platform list 수집 리스트 조회"""
    return list_scraper.Report.get_report_list()


@platform_router.get("/get-platform-page-report-list")
def get_platform_page_report_list():
    """platform page 수집 리스트 조회"""
    return page_scraper.Report.get_report_list()


@platform_router.get("/get-platform-list-report")
def get_platform_list_report(scrapName: str):
    """platform list 수집 보고서 조회"""
    list_scraper.Report.report_file_name = scrapName + "-kream"
    return list_scraper.Report.load_report()


@platform_router.get("/get-platform-page-report")
def get_platform_page_report(scrapName: str):
    """platform page 수집 보고서 조회"""
    page_scraper.Report.report_file_name = scrapName + "-kream"
    return page_scraper.Report.load_report()
