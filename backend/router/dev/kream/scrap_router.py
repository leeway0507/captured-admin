"""dev Router"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from dotenv import dotenv_values

from .components.load_scrap_result import *
from .components.scrap_product_detail import scrap_product_detail_main, save_scrap_files
from .components.create_log import get_scrap_result
from .components.scrap_product_card_list import *
from .components.main import KreamPage

config = dotenv_values(".env.dev")

kream_scrap_router = APIRouter()

kream_dict = {}


async def get_kream_page():
    """kream page 로드"""
    print("""kream page 로드""")
    if kream_dict.get("kream_page") is None:
        kream_page = KreamPage()
        await kream_page.init()
        kream_dict.update({"kream_page": kream_page})

    return kream_dict.get("kream_page")


@kream_scrap_router.get("/reload-kream-page")
async def reload_kream_page():
    """kream page 리로드"""

    if kream_dict.get("kream_page"):
        b = kream_dict.get("kream_page")
        assert isinstance(b, KreamPage), "kream_page is not KreamPage"
        assert b.browser, "browser is not exist"
        await b.close_browser()  # type: ignore
        kream_dict.pop("kream_page")

    await get_kream_page()
    return {"result": "success"}


@kream_scrap_router.get("/init-product-detail")
async def init_product_detail(
    brandName: str,
    numProcess: int,
    kreamIds: Optional[str] = None,
    kream_page: KreamPage = Depends(get_kream_page),
):
    """scrap product_detal"""

    # login
    await kream_page.login()
    result = await scrap_product_detail_main(
        kream_page, brandName, kreamIds, numProcess
    )
    return result


@kream_scrap_router.get("/init-product-card-list")
async def init_scraping_brand(
    brandName: str,
    maxScroll: int,
    minWish: int,
    minVolume: int,
    kream_page=Depends(get_kream_page),
):
    """크림 제품 검색 페이지 스크랩"""
    page = kream_page.login()
    try:
        await scrap_product_card_list(page, brandName, maxScroll, minWish, minVolume)
    except Exception:
        raise HTTPException(status_code=500, detail="kream scrap error")
    return {"result": "success"}


@kream_scrap_router.get("/get-scrap-list")
def get_kream_scrap_list():
    """scrap 결과 조회"""

    file_list = os.listdir(config["KREAM_SCRAP_RESULT_DIR"])
    file_list = [x.split(".json")[0] for x in file_list]
    file_list.sort(reverse=True)
    return file_list


@kream_scrap_router.get("/get-scrap-result")
def get_kream_scrap_result(scrapName: str):
    """scrap 결과 조회"""
    return get_scrap_result(scrapName)


@kream_scrap_router.get("/check-kream-product-card-list")
def get_last_scrap_kream_product_card_data_list(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_product_card_table 업데이트 전 조회"""
    data = get_last_scrap_kream_product_card_list(brand, sample)

    if not sendDate:
        data.pop("data")

    return data


@kream_scrap_router.get("/check-kream-product-card-detail")
def get_last_scrap_kream_product_card_data_detail(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_product_card_table 업데이트 전 조회"""
    data = get_last_scrap_kream_product_card_detail(brand, sample)

    if not sendDate:
        data.pop("data")

    return data


@kream_scrap_router.get("/check-kream-trading-volume")
def get_last_scrap_kream_trading_volume_data(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_trading_volume_table 업데이트 전 조회"""
    data = get_last_scrap_kream_trading_volume(brand, sample)

    if not sendDate:
        data.pop("data")

    return data


@kream_scrap_router.get("/check-kream-buy-and-sell")
def get_last_scrap_kream_buy_and_sell_data(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_buy_and_sell_table 업데이트 전 조회"""
    data = get_last_scrap_kream_buy_and_sell(brand, sample)

    if not sendDate:
        data.pop("data")

    return data


@kream_scrap_router.get("/check-kream-product-bridge")
def get_last_scrap_kream_product_bridge_data(
    brand: str,
    sendDate: bool = False,
    sample: int = 10,
):
    """kream_product_bridge_table 업데이트 전 조회"""
    data = get_last_scrap_kream_product_bridge(brand, sample)

    if not sendDate:
        data.pop("data")

    return data


@kream_scrap_router.get("/restart-saving-last-scraped-files")
async def restart_saving_last_scraped_files(brand: str):
    """scrap 파일 업데이트"""
    return await save_scrap_files(brand)
