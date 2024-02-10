from typing import Dict
from shop_scrap.page.scraper_main import ShopPageScraperFactory
from shop_scrap.page.report import ShopPageReport
from shop_scrap.page.data_save import ShopPageDataSave
from shop_scrap.page.target_extractor import TargetExractor, load_target_strategy
from components.abstract_class.scraper_main import Scraper
from sqlalchemy.orm import sessionmaker
from db.scrap_data_sync_db import load_sync_db
from db.dev_db import admin_session_local


class ShopPageMain:
    def __init__(self, path: str, dev_session: sessionmaker):
        self.main_scraper_factory = ShopPageScraperFactory(path)
        self.Report = ShopPageReport(path)
        self.DataSave = ShopPageDataSave(path)
        self._main_scraper = None
        self.Target = TargetExractor(dev_session)
        self.sync_db = load_sync_db("shop_page")(admin_session_local, path)

    @property
    def main_scraper(self):
        if not self._main_scraper:
            raise ValueError("main scraper is not set")
        return self._main_scraper

    @main_scraper.setter
    def main_scraper(self, main_scraper: Scraper):
        self._main_scraper = main_scraper

    async def execute(self, searchType: str, value: str | Dict, num_processor: int):
        target_list = await self.extract_target_list(searchType, value)
        print("shop_page : target_list")
        print(len(target_list))
        self.main_scraper = await self.main_scraper_factory.playwright(
            target_list, num_processor
        )
        await self.main_scraper.scrap()
        report_name = await self.Report.save_report()
        await self.DataSave.save_scrap_data()
        return report_name

    async def extract_target_list(self, searchType: str, value: str | Dict):
        self.Target.strategy = load_target_strategy(searchType)
        return await self.Target.extract_data(value)

    async def sync(self, scrap_time: str):
        self.sync_db.scrap_time = scrap_time
        await self.sync_db.sync_data()
        return {"status": "success"}
