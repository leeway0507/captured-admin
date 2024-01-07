from typing import List
from shop_scrap.list.scraper_main import ShopListScraperFactory
from shop_scrap.list.report import ShopListReport
from shop_scrap.list.data_save import ShopListDataSave
from components.abstract_class.scraper_main import ShopScraper


class ShopListMain:
    def __init__(self, path: str):
        self.main_scraper_factory = ShopListScraperFactory(path)
        self.Report = ShopListReport(path)
        self.DataSave = ShopListDataSave(path)
        self._main_scraper = None

    @property
    def main_scraper(self):
        if not self._main_scraper:
            raise ValueError("main scraper is not set")
        return self._main_scraper

    @main_scraper.setter
    def main_scraper(self, main_scraper: ShopScraper):
        self._main_scraper = main_scraper

    async def execute(self):
        await self.main_scraper.scrap()
        await self.Report.save_report()
        await self.DataSave.save_scrap_data()

    async def init_main_scraper(
        self, shop_name: str, target_list: List[str], num_processor: int
    ):
        self.main_scraper = await getattr(self.main_scraper_factory, shop_name)()
        self.main_scraper.target_list = target_list
        self.main_scraper.late_binding(num_processor)
