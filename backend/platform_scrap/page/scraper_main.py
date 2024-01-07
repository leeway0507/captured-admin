from typing import Callable
from .scraper_sub import PwKreamPageSubScraper
from components.browser_handler import PwKreamContextHanlder, PwPageHandler
from components.abstract_class.scraper_main import PlatformScraper


class PlatformPageScraperFactory:
    def __init__(self, path: str):
        self.path = path

    async def pw_kream(self):
        pw_kream_browser = await PwKreamContextHanlder.start()
        return PlatformPageScraper(self.path, pw_kream_browser, PwKreamPageSubScraper)


class PlatformPageScraper(PlatformScraper):
    def __init__(
        self,
        path: str,
        browser: PwKreamContextHanlder,
        sub_scraper: Callable[..., PwKreamPageSubScraper],
    ):
        super().__init__(path, browser, sub_scraper, platform_type="kream")
        self.path = path

    def set_sub_scraper_params(self):
        pass

    async def save_scrap_config_to_temp_file(self):
        config = {
            "path": self.path,
            "scrap_time": self.scrap_time,
            "num_of_plan": len(self._target_list),
            "brand_name": self._target_list,
            "platform": self.platform_type,
            "num_processor": self.num_processor,
        }
        await self.TempFile.append_temp_file("scrap_config", config)

    # concrete_method
    async def save_data_to_temp_file(self, data: dict):
        for data_type, card_data in data.items():
            await self.TempFile.append_temp_file(data_type, card_data)
