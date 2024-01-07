from typing import List, Callable, Dict
from datetime import datetime


from components.abstract_class.scraper_main import ShopScraper
from components.abstract_class.scraper_sub import PwShopListSubScraper

from components.browser_handler import PwContextHandler
from ..shop_list.consortium import PwConsortiumListSubScraper


class ShopListScraperFactory:
    def __init__(self, path: str):
        self.path = path

    async def consortium(self):
        pw_browser = await PwContextHandler.start()
        return PwShopListScraper(
            self.path, pw_browser, PwConsortiumListSubScraper, "consortium"
        )


class PwShopListScraper(ShopScraper):
    def __init__(
        self,
        path: str,
        browser: PwContextHandler,
        sub_scraper: Callable[..., PwShopListSubScraper],
        shop_name: str,
    ):
        super().__init__(path, "product_card_list", browser)
        self.shop_name = shop_name
        self.sub_scraper_class = sub_scraper

    def set_sub_scraper_params(self):
        return {}

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
