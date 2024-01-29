from typing import List
from platform_scrap.list.scraper_main import (
    PlatformListScraperFactory,
    PwKreamListScraper,
)
from platform_scrap.list.report import PlatformListReport
from platform_scrap.list.data_save import PlatformListDataSave
from db.scrap_data_sync_db import load_sync_db
from db.dev_db import admin_session_local


class PlatformListMain:
    def __init__(self, path: str):
        self.path = path
        self.main_scraper_factory = PlatformListScraperFactory(path)
        self.Report = PlatformListReport(path)
        self.DataSave = PlatformListDataSave(path)
        self._main_scraper = None
        self.sync_db = load_sync_db("platform_list")(admin_session_local, path)

    @property
    def main_scraper(self):
        if not self._main_scraper:
            raise ValueError("main scraper is not set")
        return self._main_scraper

    @main_scraper.setter
    def main_scraper(self, main_scraper: PwKreamListScraper):
        self._main_scraper = main_scraper

    async def kream_execute(
        self,
        target_list: List[str],
        num_processor: int,
        max_scroll: int = 20,
        min_volume: int = 50,
        min_wish: int = 50,
    ):
        self.main_scraper = await self.main_scraper_factory.kream(
            target_list, num_processor, max_scroll, min_volume, min_wish
        )
        await self.main_scraper.scrap()
        report_name = await self.Report.save_report()
        await self.DataSave.save_scrap_data()

        return report_name

    async def sync(self, scrap_time: str):
        self.sync_db.scrap_time = scrap_time
        await self.sync_db.sync_data()
        return {"status": "success"}
