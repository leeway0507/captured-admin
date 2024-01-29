from typing import List, Callable

from components.abstract_class.scraper_main import Scraper, ScrapStatusBase
from components.browser_handler import PwKreamContextHanlder
from .scraper_sub import PwKreamListSubScraper


class PlatformListScraperFactory:
    def __init__(self, path: str):
        self.path = path

    async def kream(
        self,
        target_list: List,
        num_processor: int = 1,
        max_scroll: int = 20,
        min_volume: int = 50,
        min_wish: int = 50,
    ):
        pw_kream_browser = await PwKreamContextHanlder.start(allow_cookie=True)
        return PwKreamListScraper(
            self.path,
            pw_kream_browser,
            PwKreamListSubScraper,
            target_list,
            num_processor,
            max_scroll,
            min_volume,
            min_wish,
        )


class PlatformScrapStatus(ScrapStatusBase):
    platform_type: str


class PwKreamListScraper(Scraper):
    def __init__(
        self,
        path: str,
        browser: PwKreamContextHanlder,
        sub_scraper: Callable[..., PwKreamListSubScraper],
        target_list: List,
        num_processor: int,
        max_scroll: int,
        min_volume: int,
        min_wish: int,
    ):
        super().__init__(path, browser, num_processor, sub_scraper)
        self.browser: PwKreamContextHanlder
        self.sub_scraper: PwKreamListSubScraper
        self.target_list = target_list
        self.min_volume = min_volume
        self.min_wish = min_wish
        self.max_scroll = max_scroll
        self.platform_type = "kream"

    async def browser_login(self):
        await self.browser.login()

    def set_sub_scraper_params(self):
        return {
            "max_scroll": self.max_scroll,
            "min_volume": self.min_volume,
            "min_wish": self.min_wish,
        }

    async def save_scrap_config_to_temp_file(self):
        config = {
            "path": self.path,
            "scrap_time": self.scrap_time,
            "num_of_plan": len(self._target_list),
            "brand_name": self._target_list[0],
            "platform": self.platform_type,
            "num_processor": self.num_processor,
            "min_volume": self.min_volume,
            "min_wish": self.min_wish,
            "max_scroll": self.max_scroll,
        }
        await self.TempFile.append_temp_file("scrap_config", config)

    # concrete_method
    async def save_data_to_temp_file(self, card_data: List):
        if card_data:
            serialized_data = [x.model_dump() for x in card_data]
            await self.TempFile.append_temp_file("product_card_list", serialized_data)
