from typing import List
from logs.make_log import make_logger
from ...utils.browser_controller import PageController as P
from .list_module_factory import ShopListModule
from .schema import ListScrapData
from time import time


class ShopListScrapMachine:
    def __init__(self, page_controller: P, shop_list_module: ShopListModule):
        self.page_controller = page_controller
        self.shop_module = shop_list_module
        self.shop_name = shop_list_module.__name__

    async def load_page(self, url, wait_until_load=2000):
        await self.page_controller.go_to(url)
        await self.page_controller.sleep_until(wait_until_load)

    async def execute(self, brand_name: str) -> List[ListScrapData]:
        url = self.shop_module.get_url(brand_name)
        (
            scroll_on,
            reverse_not_found_result,
            page_reload_after_cookies,
            cookie_button_xpath,
            not_found_xpath,
            wait_until_load,
            max_scroll,
        ) = (
            self.shop_module.config().model_dump().values()
        )

        # 1. deal with cookies
        await self.load_page(url, wait_until_load)
        if cookie_button_xpath:
            await self.page_controller.deal_with_cookies(cookie_button_xpath)

        # 1-2 page_reload after cookie
        if page_reload_after_cookies:
            await self.load_page(url, wait_until_load)

        # 2. check page is not found
        await self.page_controller.sleep_until(1000)
        not_found = await self.page_controller.check_not_found(not_found_xpath)

        # reverse not found error for some cases
        if reverse_not_found_result:
            not_found = not not_found

        if not_found:
            txt = f"[{self.shop_name}] has no [{brand_name}] items"
            print(txt)
            return []

        # 3. scrap items
        cards_info = []
        page_num: int = 0
        while True:
            if scroll_on:
                await self.page_controller.scroll_down(
                    max_scroll=max_scroll, time_delay=1000
                )

            page = await self.page_controller.get_page()
            cards = await self.shop_module.extract_card_html(page)

            if not cards:
                txt = f"[{self.shop_name}] has no [{brand_name}] cards items"
                print(txt)
                break

            cards_info += [
                self.shop_module.extract_info(card, brand_name) for card in cards
            ]

            if not await self.shop_module.get_next_page(page, page_num):
                break

            page_num += 1

        return cards_info
