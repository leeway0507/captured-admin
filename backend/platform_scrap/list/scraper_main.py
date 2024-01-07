from typing import List, Callable

from components.abstract_class.scraper_main import PlatformScraper
from components.browser_handler import PwKreamContextHanlder
from .scraper_sub import PwKreamListSubScraper


class PlatformListScraperFactory:
    def __init__(self, path: str):
        self.path = path

    async def pw_kream(self, min_volume: int = 50, min_wish: int = 50):
        pw_kream_browser = await PwKreamContextHanlder.start()
        return PwKreamListScraper(
            self.path,
            pw_kream_browser,
            PwKreamListSubScraper,
            min_volume,
            min_wish,
        )


class PwKreamListScraper(PlatformScraper):
    def __init__(
        self,
        path: str,
        browser: PwKreamContextHanlder,
        sub_scraper: Callable[..., PwKreamListSubScraper],
        min_volume: int,
        min_wish: int,
    ):
        super().__init__(path, browser, sub_scraper, "kream")
        self.sub_scraper: PwKreamListSubScraper
        self.min_volume = min_volume
        self.min_wish = min_wish

    def set_sub_scraper_params(self):
        return {"min_volume": self.min_volume, "min_wish": self.min_wish}

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
        }
        await self.TempFile.append_temp_file("scrap_config", config)

    # concrete_method
    async def save_data_to_temp_file(self, card_data: List):
        if card_data:
            serialized_data = [x.model_dump() for x in card_data]
            await self.TempFile.append_temp_file("product_card_list", serialized_data)
