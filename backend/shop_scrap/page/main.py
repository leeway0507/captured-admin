from typing import List
from shop_scrap.page.scraper_main import ShopPageScraperFactory
from shop_scrap.page.report import ShopPageReport
from shop_scrap.page.data_save import ShopPageDataSave
from components.abstract_class.scraper_main import ShopScraper


class ShopPageMain:
    def __init__(self, path: str):
        self.main_scraper_factory = ShopPageScraperFactory(path)
        self.Report = ShopPageReport(path)
        self.DataSave = ShopPageDataSave(path)
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
        self, shop_name: str, target_list: List, num_processor: int
    ):
        self.main_scraper = await getattr(self.main_scraper_factory, shop_name)()
        self.main_scraper.target_list = target_list
        self.main_scraper.late_binding(num_processor)
