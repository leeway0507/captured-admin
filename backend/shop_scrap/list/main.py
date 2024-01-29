from typing import List
from shop_scrap.list.scraper_main import ShopListScraperFactory, PwShopListScraper
from shop_scrap.list.report import ShopListReport
from shop_scrap.list.data_save import ShopListDataSave
from components.abstract_class.scraper_main import Scraper
from db.scrap_data_sync_db import load_sync_db
from db.dev_db import admin_session_local


class ShopListMain:
    def __init__(self, path: str):
        self.main_scraper_factory = ShopListScraperFactory(path)
        self.Report = ShopListReport(path)
        self.DataSave = ShopListDataSave(path)
        self._main_scraper: PwShopListScraper
        self.sync_db = load_sync_db("shop_list")(admin_session_local, path)

    @property
    def main_scraper(self):
        if not self._main_scraper:
            raise ValueError("main scraper is not set")
        return self._main_scraper

    @main_scraper.setter
    def main_scraper(self, main_scraper: PwShopListScraper):
        self._main_scraper = main_scraper

    async def execute(self, shop_name: str, target_list: List[str], num_processor: int):
        self.main_scraper = await self.main_scraper_factory.playwright(
            shop_name, target_list, num_processor
        )

        await self.main_scraper.scrap()
        report_name = await self.Report.save_report()
        await self.DataSave.save_scrap_data()
        return report_name

    async def sync(self, scrap_time: str):
        self.sync_db.scrap_time = scrap_time
        await self.sync_db.sync_data()
        return {"status": "success"}
