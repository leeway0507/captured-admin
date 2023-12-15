from typing import List
from logs.make_log import make_logger
from ....utils.browser_controller import PageController as P
from .list_module_factory import ShopListModule
from .schema import ListScrapData


class ShopListScrapMachine:
    def __init__(self, page_controller: P, shop_list_module: ShopListModule):
        self.page_controller = page_controller
        self.shop_module = shop_list_module
        self.shop_name = shop_list_module.__name__
        self.log_dir = f"logs/shop_product_card_list/{self.shop_name}.log"
        self.log = make_logger(self.log_dir, self.shop_name)

    async def load_page(self, url):
        page_loading_result = await self.page_controller.go_to(url)
        assert page_loading_result, self.log.error(
            f"[{self.shop_name}] page load failed"
        )
        await self.page_controller.sleep_until(2000)

    async def execute(self, brand_name: str) -> List[ListScrapData]:
        url = self.shop_module.get_url(brand_name)
        (
            scroll_on,
            reverse_not_found_result,
            page_reload_after_cookies,
            cookie_button_xpath,
            not_found_xpath,
        ) = (
            self.shop_module.config().model_dump().values()
        )

        # 1. deal with cookies
        await self.load_page(url)
        await self.page_controller.deal_with_cookies(cookie_button_xpath)

        # 1-2 page_reload after cookie
        if page_reload_after_cookies:
            await self.load_page(url)

        # 2. check page is not found
        await self.page_controller.sleep_until(2000)
        not_found = await self.page_controller.check_not_found(not_found_xpath)

        # reverse not found error for some cases
        if reverse_not_found_result:
            not_found = not not_found

        if not_found:
            self.log.warning(f"[{self.shop_name}] has no [{brand_name}] items")
            return []

        # 3. scrap items
        cards_info = []
        page_num: int = 0
        while True:
            if scroll_on:
                await self.page_controller.scroll_down(max_scroll=20, time_delay=0.5)

            page = await self.page_controller.get_page()
            cards = await self.shop_module.extract_card_html(page)

            if not cards:
                txt = f"[{self.shop_name}] has no [{brand_name}] cards items"
                self.log.warning(txt)
                break

            cards_info += [self.shop_module.extract_info(card) for card in cards]

            if not await self.shop_module.get_next_page(page, page_num):
                break

            page_num += 1

        return cards_info
