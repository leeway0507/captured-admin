from typing import List, Any
from ....utils.browser_controller import PageController as P
from ....utils.temp_file_manager import TempFileManager
from .module_factory import PlatformListModule
from env import dev_env


class PlatformListScrapMachine:
    def __init__(self, page_controller: P, platform_list_module: PlatformListModule):
        self.page_controller = page_controller
        self.platform = platform_list_module
        self.platform_type = platform_list_module.__name__()
        self.path = dev_env.PLATFORM_PRODUCT_LIST_DIR
        self.log_dir = f"logs/platform_product_card_list/{self.platform_type}.log"
        self.tfm = TempFileManager("platform_list")

    async def execute(self, brand_name: str, min_volume=0, min_wish=0) -> List[Any]:
        url = self.platform.get_url(brand_name)
        await self.page_controller.go_to(url)
        await self.page_controller.sleep_until(2000)
        await self.page_controller.scroll_down(max_scroll=1, time_delay=500)

        card_query = self.platform.get_card_query()
        card_list = await self.page_controller.extract_html(card_query)

        if not card_list:
            txt = f"[{self.platform_type}] has no [{brand_name}] cards items"
            print(txt)
            return []

        await self.tfm.save_temp_file("scrap_raw_file", card_list)

        product_card = await self.platform.get_product_card_list(
            card_list, min_volume, min_wish
        )
        return product_card
