import os
from typing import List, Any
from logs.make_log import make_logger
from ...utils.browser_controller import PageController as P
from ...utils.temp_file_manager import TempFileManager
from .module_factory import PlatformPageModule as M
from env import dev_env


class PlatformPageScrapMachine:
    def __init__(self, page_controller: P, platform_page_module: M):
        self.page_controller = page_controller
        self.platform = platform_page_module
        self.platform_type = platform_page_module.__name__()
        self.path = dev_env.PLATFORM_PRODUCT_LIST_DIR
        self.tfm = TempFileManager("platform_page")

    async def load_page(self, url):
        await self.page_controller.go_to(url)
        await self.page_controller.sleep_until(2000)

    async def execute(self, platform_sku: str) -> str:
        url = self.platform.get_url(platform_sku)
        await self.load_page(url)
        page = await self.page_controller.get_page()

        page_detail = await self.platform.get_product_detail(page, platform_sku)
        await self.tfm.save_temp_file("product_detail", page_detail)

        await self.page_controller.sleep_until(2000)
        buy_and_sell = await self.platform.get_buy_and_sell(page, platform_sku)
        await self.tfm.save_temp_file("buy_and_sell", buy_and_sell)

        await self.page_controller.sleep_until(2000)
        status, trading_volume = await self.platform.get_product_volume(
            page, platform_sku
        )
        await self.tfm.save_temp_file("trading_volume", trading_volume)

        if status == "success":
            return "success"

        elif status == "no_trading_volume":
            return "success:no_trading_volume"

        else:
            return "failed:can't scrap trading_volume"
