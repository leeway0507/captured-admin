"""dev Router"""

from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from env import dev_env

from db.dev_db import get_dev_db

from .components.data_loader import *
from .components.platform_product_card_page import PlatformPageMain, PageSearchType
from .components.platform_product_card_list import PlatformListMain
from .components.update_to_db import (
    get_kream_product_detail_list_from_db,
    get_kream_product_size_info,
    get_kream_product_color_for_registration,
)
from .components.platform_browser_controller import PwPlatformBrowserControllerFactory
from .components.platform_product_card_page.module_factory import (
    PwPlatformPageModuleFactory,
)
from .components.platform_product_card_list.module_factory import (
    PwPlatformListModuleFactory,
)
from .components.platform_product_card_page.save_manager import (
    SaveManager,
    ModuleFactory,
    PreprocessType,
)
from .components.data_loader import loader, LoadType
from ..utils.scrap_report import ScrapReport
from ..utils.temp_file_manager import TempFileManager
from ..utils.util import save_to_parquet

platform_router = APIRouter()

platformPage = ScrapReport("platform_page")
platformList = ScrapReport("platform_list")


@platform_router.get("/init-product-page")
async def scrap_product_page(
    search_type: str,
    value: str,
    numProcess: int,
    platformType: str = "kream",
):
    browser_controller = getattr(PwPlatformBrowserControllerFactory(), platformType)()
    browser_controller = await browser_controller.create()

    module = getattr(PwPlatformPageModuleFactory(), platformType)()

    Scraper = PlatformPageMain(
        n_p=numProcess,
        browser_controller=browser_controller,
        module=module,
        min_volume=100,
        min_wish=50,
        platform_type=platformType,
    )
    return await Scraper.main(PageSearchType(search_type), value)


@platform_router.get("/save-last-product-page")
async def save_last_data(searchType: str, value: str, platformType: str = "kream"):
    if searchType == PageSearchType.LAST_SCRAP.value:
        scrap_folder = value
    elif searchType == PageSearchType.PRODUCT_ID.value:
        scrap_folder = "product_id"
    elif searchType == PageSearchType.SKU.value:
        scrap_folder = "sku"
    else:
        raise Exception("Invalid Search Type")

    path = dev_env.PLATFORM_PRODUCT_PAGE_DIR
    save_path = os.path.join(path, scrap_folder)

    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)

    save_time = datetime.now().strftime("%y%m%d-%H%M%S")
    preprocess_module = getattr(ModuleFactory(), platformType)()
    manager = SaveManager(save_path, save_time, preprocess_module)

    await manager.save(PreprocessType.PRODUCT_DETAIL)
    await manager.save(PreprocessType.PRODUCT_BRIDGE)
    await manager.save(PreprocessType.TRADING_VOLUME)
    await manager.save(PreprocessType.BUY_AND_SELL)

    platformPage.create_new_report(
        save_time,
        platformType,
        external_data={
            "product_detail": loader(LoadType.PRODUCT_DETAIL, scrap_folder, save_time),
            "product_bridge": loader(LoadType.PRODUCT_BRIDGE, scrap_folder, save_time),
            "trading_volume": loader(LoadType.TRADING_VOLUME, scrap_folder, save_time),
            "buy_and_sell": loader(LoadType.BUY_AND_SELL, scrap_folder, save_time),
        },
    )

    return {"status": "success"}


@platform_router.get("/init-product-card-list")
async def scrap_product_list(
    brandName: str,
    minWish: int,
    minVolume: int,
    platformType: str = "kream",
):
    browser_controller = getattr(PwPlatformBrowserControllerFactory(), platformType)()
    browser_controller = await browser_controller.create()

    module = getattr(PwPlatformListModuleFactory(), platformType)()
    Scraper = PlatformListMain(
        n_p=1,
        browser_controller=browser_controller,
        module=module,
        min_volume=minVolume,
        min_wish=minWish,
        platform_type=platformType,
    )
    return await Scraper.main(brandName)


@platform_router.get("/save-last-product-card-list")
async def save_last_product_card_list():
    time_now = datetime.now().strftime("%y%m%d-%H%M%S")
    list_data = await TempFileManager("platform_list").load_temp_file(
        "product_card_list"
    )

    path = dev_env.PLATFORM_PRODUCT_LIST_DIR
    save_path = os.path.join(path, "kream")
    file_name = time_now + "-" + "kream"
    save_to_parquet(save_path, file_name, list_data)


@platform_router.get("/get-platform-list-report-list")
def get_platform_list_report_list():
    """platform list 수집 리스트 조회"""
    return platformList.get_report_list()


@platform_router.get("/get-platform-list-report")
def get_platform_list_report(scrapName: str):
    """platform list 수집 보고서 조회"""
    return platformList.get_report(scrapName)


@platform_router.get("/get-platform-page-report-list")
def get_platform_page_report_list():
    """platform page 수집 리스트 조회"""
    return platformPage.get_report_list()


@platform_router.get("/get-platform-page-report")
def get_platform_page_report(scrapName: str):
    """platform page 수집 보고서 조회"""
    return platformPage.get_report(scrapName)


@platform_router.get("/check-kream-product-card-list")
def get_last_scrap_kream_product_card_data_list(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_product_card_table 업데이트 전 조회"""
    data = loader(LoadType.PRODUCT_CARD_LIST, brand, None, sample)

    if not sendDate:
        data.pop("data")

    return data


@platform_router.get("/check-kream-product-card-detail")
def get_last_scrap_kream_product_card_data_detail(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_product_card_table 업데이트 전 조회"""
    data = loader(LoadType.PRODUCT_DETAIL, brand, None, sample)

    if not sendDate:
        data.pop("data")

    return data


@platform_router.get("/check-kream-trading-volume")
def get_last_scrap_kream_trading_volume_data(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_trading_volume_table 업데이트 전 조회"""
    data = loader(LoadType.TRADING_VOLUME, brand, None, sample)

    if not sendDate:
        data.pop("data")

    return data


@platform_router.get("/check-kream-buy-and-sell")
def get_last_scrap_kream_buy_and_sell_data(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_buy_and_sell_table 업데이트 전 조회"""
    data = loader(LoadType.BUY_AND_SELL, brand, None, sample)

    if not sendDate:
        data.pop("data")

    return data


@platform_router.get("/check-kream-product-bridge")
def get_last_scrap_kream_product_bridge_data(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_product_bridge_table 업데이트 전 조회"""
    data = loader(LoadType.PRODUCT_BRIDGE, brand, None, sample)

    if not sendDate:
        data.pop("data")

    return data


# @platform_router.get("/restart-saving-last-scraped-files")
# async def restart_saving_last_scraped_files(brandName: str):
#     """scrap 파일 업데이트"""
#     return await save_scrap_files(brandName)


# @platform_router.get("/restart-saving-create-log")
# def restart_create_log(scrapName: str):
#     """kream_log 파일 업데이트"""
#     return create_last_update_kream_detail_log(scrapName)


@platform_router.get("/get-kream-product-detail-list")
async def get_kream_product_detail_list(
    searchType: str,
    content: str,
    db: AsyncSession = Depends(get_dev_db),
):
    """kream_product_detail_table 조회"""

    return await get_kream_product_detail_list_from_db(db, searchType, content)


@platform_router.get("/get-kream-product-size-info")
async def get_kream_product_size_info_api(
    searchType: str, content: str, db: AsyncSession = Depends(get_dev_db)
):
    """kream_product_detail_table 조회"""
    return await get_kream_product_size_info(db, searchType, content)


@platform_router.get("/get-product-color-for-registraion")
async def get_product_color_for_registraion(
    productId: str, db: AsyncSession = Depends(get_dev_db)
):
    """kream_product_detail_table 조회"""
    return await get_kream_product_color_for_registration(db, productId)
