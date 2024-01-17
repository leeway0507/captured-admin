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
