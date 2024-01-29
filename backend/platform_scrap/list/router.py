from fastapi import APIRouter
from platform_scrap.list.main import PlatformListMain
from components.env import get_path

# /api/platform/list/
platform_list = APIRouter()

ScrapList = PlatformListMain(get_path("platform_list"))


@platform_list.get("/scrap")
async def scrap(brandName: str, maxScroll: int, minVolume: int, minWish: int):
    target_list = brandName.split(",")
    report_name = await ScrapList.kream_execute(
        target_list,
        1,
        maxScroll,
        minVolume,
        minWish,
    )
    return {"scrap_status": "success", "report_name": report_name}


@platform_list.post("/sync_db/{scrap_time}")
async def sync_db(scrap_time: str):
    return await ScrapList.sync(scrap_time)


@platform_list.get("/report/list")
def report_list():
    return ScrapList.Report.get_report_list()


@platform_list.get("/report/item/{name}")
def report_item(name: str):
    ScrapList.Report.report_file_name = name
    return ScrapList.Report.get_report()
