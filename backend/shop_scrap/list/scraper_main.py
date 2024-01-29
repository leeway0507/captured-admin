from typing import List, Callable, Dict, Any
from datetime import datetime


from components.abstract_class.scraper_main import Scraper
from components.abstract_class.scraper_sub import PwShopListSubScraper

from components.browser_handler import PwContextHandler, PwPageHandler
from ..shop_list.consortium import PwConsortiumListSubScraper
from ..shop_list.seven_store import PwSevenStoreListSubScraper
from ..shop_list.urban_industry import PwUrbanIndustryListSubScraper


class ShopListScraperFactory:
    def __init__(self, path: str):
        self.path = path
        self._browser = None

    @property
    async def browser(self):
        if not self._browser:
            self._browser = await PwContextHandler.start()
        return self._browser

    async def playwright(self, shop_name: str, target_list: List, num_processor: int):
        return PwShopListScraper(
            target_list,
            self.path,
            await self.browser,
            num_processor,
            PwConsortiumListSubScraper,
            shop_name,
        )

    @classmethod
    def pw_sub_scraper_list(cls):
        method_list = dir(PwShopListSubScraperFactory)
        return [m for m in method_list if not "__" in m]

    @classmethod
    def pw_sub_scraper_brand(cls, shop_name: str):
        sub_scraper = getattr(PwShopListSubScraperFactory(), shop_name)()
        brand_list = sub_scraper._load_brand_list()
        return brand_list["brand_list"]


class PwShopListSubScraperFactory:
    def consortium(self):
        return PwConsortiumListSubScraper()

    def seven_store(self):
        return PwSevenStoreListSubScraper()

    def urban_industry(self):
        return PwUrbanIndustryListSubScraper()


class PwShopListScraper(Scraper):
    def __init__(
        self,
        target_list: List,
        path: str,
        browser: PwContextHandler,
        num_processor: int,
        sub_scraper_class: Callable[..., PwShopListSubScraper],
        shop_name: str,
    ):
        super().__init__(path, browser, num_processor, sub_scraper_class)
        self.target_list = target_list
        self.shop_name = shop_name
        self.temp_file_name = "product_card_list"

    def set_sub_scraper_params(self):
        return {"shop_name": self.shop_name}

    async def browser_login(self):
        pass

    async def sub_processor(self, page: PwPageHandler, jobs: List[Any]):
        sub_scraper = None

        for job in jobs:
            sub_scraper = getattr(PwShopListSubScraperFactory(), self.shop_name)()
            sub_scraper.late_binding(page_handler=page, **self.set_sub_scraper_params())
            status = await self.execute_job(sub_scraper, job)
            await self.save_scrap_status_to_temp_file(job, status)

        if sub_scraper:
            await sub_scraper.page_handler.close_page()

    async def save_scrap_config_to_temp_file(self):
        config = {
            "path": self.path,
            "scrap_time": self.scrap_time,
            "num_of_plan": len(self._target_list),
            "brand_name": ",".join(self._target_list),
            "shop_name": self.shop_name,
            "num_processor": self.num_processor,
        }
        await self.TempFile.append_temp_file("scrap_config", config)

    async def save_data_to_temp_file(self, data: List):
        if data:
            await self.TempFile.append_temp_file(self.temp_file_name, data)
