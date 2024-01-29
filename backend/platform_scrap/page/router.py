from typing import Optional
from fastapi import APIRouter
from platform_scrap.page.main import PlatformPageMain
from components.env import get_path

# /api/platform/list/
platform_page = APIRouter()

ScrapPage = PlatformPageMain(get_path("platform_page"), get_path("platform_list"))


@platform_page.get("/scrap")
async def scrap(searchType: str, numProcess: int, value: Optional[str] = None):
    report_name = await ScrapPage.kream_execute(searchType, value, numProcess)
    return {"scrap_status": "success", "report_name": report_name}


@platform_page.get("/report/list")
def report_list():
    return ScrapPage.Report.get_report_list()


@platform_page.get("/report/item/{name}")
def report_item(name: str):
    ScrapPage.Report.report_file_name = name
    return ScrapPage.Report.get_report()


@platform_page.post("/sync_db/{scrap_time}")
async def sync_db(scrap_time: str):
    return await ScrapPage.sync(scrap_time)
