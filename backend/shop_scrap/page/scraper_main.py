from typing import List, Callable, Dict, Any
from datetime import datetime


from components.abstract_class.scraper_main import Scraper
from components.abstract_class.scraper_sub import PwShopPageSubScraper

from components.browser_handler import PwContextHandler, PwPageHandler
from ..shop_list.consortium import PwConsortiumPageSubScraper
from ..shop_list.seven_store import PwSevenStorePageSubScraper


class ShopPageScraperFactory:
    def __init__(self, path: str):
        self.path = path
        self._browser = None

    @property
    async def browser(self):
        if not self._browser:
            self._browser = await PwContextHandler().start()
        return self._browser

    async def playwright(self, target_list: List, num_processor: int):
        return PwShopPageScraper(
            target_list,
            self.path,
            await self.browser,
            num_processor,
            PwConsortiumPageSubScraper,
        )

    async def size_batch(self, target_list: List, num_processor: int, scrap_time: str):
        return PwSizeBatchScraper(
            target_list,
            self.path,
            await self.browser,
            num_processor,
            PwConsortiumPageSubScraper,
            scrap_time,
        )


class PwShopPageSubScraperFactory:
    def consortium(self):
        return PwConsortiumPageSubScraper()

    def seven_store(self):
        return PwSevenStorePageSubScraper()


class PwShopPageScraper(Scraper):
    def __init__(
        self,
        target_list: List,
        path: str,
        browser: PwContextHandler,
        num_processor: int,
        sub_scraper_class: Callable[..., PwShopPageSubScraper],
    ):
        super().__init__(path, browser, num_processor, sub_scraper_class)
        self.target_list = target_list
        self.temp_file_name = "product_card_page"

    def set_sub_scraper_params(self):
        return {}

    async def browser_login(self):
        pass

    async def sub_processor(self, page: PwPageHandler, jobs: List[Any]):
        sub_scraper = None

        for job in jobs:
            sub_scraper = getattr(PwShopPageSubScraperFactory(), job["shop_name"])()
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
            "num_processor": self.num_processor,
        }
        await self.TempFile.append_temp_file("scrap_config", config)

    async def save_data_to_temp_file(self, data: List):
        if data:
            await self.TempFile.append_temp_file(self.temp_file_name, data)


class PwSizeBatchScraper(PwShopPageScraper):
    def __init__(
        self,
        target_list: List,
        path: str,
        browser: PwContextHandler,
        num_processor: int,
        sub_scraper_class: Callable[..., PwShopPageSubScraper],
        scrap_time: str,
    ):
        super().__init__(target_list, path, browser, num_processor, sub_scraper_class)
        self.scrap_time = scrap_time

    async def init(self):
        self.TempFile.init()
        self._check_necessary_property()
        await self.save_scrap_config_to_temp_file()

    async def main(self):
        """
        기존 main method에서 init을 제외함.
        SizeBatchMain class에서 scraper 불러올 시 init 수행하는 것으로 변경
        """

        await self.browser_login()
        await self.execute_sub_processors()
        print(f"scrap done")
