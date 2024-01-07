from typing import List
from platform_scrap.list.scraper_main import PlatformListScraperFactory
from platform_scrap.list.report import PlatformListReport
from platform_scrap.list.data_save import PlatformListDataSave
from components.abstract_class.scraper_main import PlatformScraper


class PlatformListMain:
    def __init__(self, path: str):
        self.main_scraper_factory = PlatformListScraperFactory(path)
        self.Report = PlatformListReport(path)
        self.DataSave = PlatformListDataSave(path)
        self._main_scraper = None

    @property
    def main_scraper(self):
        if not self._main_scraper:
            raise ValueError("main scraper is not set")
        return self._main_scraper

    @main_scraper.setter
    def main_scraper(self, main_scraper: PlatformScraper):
        self._main_scraper = main_scraper

    async def execute(self):
        await self.main_scraper.scrap()
        await self.Report.save_report()
        await self.DataSave.save_scrap_data()

    async def init_pw_kream_scraper(self, target_list: List[str], num_processor: int):
        self.main_scraper = await self.main_scraper_factory.pw_kream()
        self.main_scraper.target_list = target_list
        self.main_scraper.late_binding(num_processor)
