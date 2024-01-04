import os
import json
from typing import List, Tuple, Dict

from abc import abstractmethod

from bs4 import Tag

from env import dev_env

from ...utils.browser_controller import PageController as P
from components.dev.sub_scraper import SubScraper
from components.dev.shop.list import ListScrapData


class PwShopListSubScraper(SubScraper):
    def __init__(self):
        super().__init__()
        self.shop_name: str = ""
        self.wait_until_load = 2000
        self.reverse_not_found_result: bool = False
        self.page_reload_after_cookies: bool = False
        self.cookie_button_xpath: List[str] = []
        self.not_found_xpath: str
        self.wait_until_load: int = 2000
        self.using_scroll = False
        self.scroll_down_time_delay = 1000
        self.max_scroll: int = 10

    def late_binding(self, page_controller: P):
        self.page_controller = page_controller
        self.page = page_controller.get_page()

    async def execute(self) -> Tuple[str, List[ListScrapData] | List]:
        await self.load_page()
        await self.handle_cookies()

        return (
            await self.scrap_data()
            if not await self.item_is_not_found()
            else self._failed()
        )

    async def load_page(self):
        url = self.get_url()
        await self.page_controller.go_to(url)
        await self.page_controller.sleep_until(self.wait_until_load)

    def get_url(self) -> str:
        brand_list = self._load_brand_list()["data"]

        for brand in brand_list:
            if brand["brand_name"] == self.job:
                return brand["brand_url"]

        raise Exception(f"brand_name: {self.job} not found")

    def _load_brand_list(self):
        path = os.path.join(dev_env.SHOP_LIST_DIR, self.shop_name, "brand_list.json")

        with open(path) as f:
            return json.load(f)

    async def handle_cookies(self):
        if self.cookie_button_xpath:
            await self.page_controller.handle_cookies(self.cookie_button_xpath)

        if self.page_reload_after_cookies:
            await self.load_page()

    async def item_is_not_found(self):
        not_found = await self.page_controller.check_not_found(self.not_found_xpath)

        if self.reverse_not_found_result:
            not_found = not not_found

        if not_found:
            print(f"[{self.shop_name}] has no [{self.job}] items")

        return not_found

    def _failed(self):
        print(f"[{self.shop_name}] has no [{self.job}] items")
        return "fail", []

    async def scrap_data(self) -> Tuple[str, List]:
        card_raw_data = await self.scrap_card_raw_data()
        return "success", self.drop_duplicate_data(card_raw_data)

    async def scrap_card_raw_data(self):
        # 3. scrap items

        raw_card_data = []
        page_num = 0
        while True:
            await self.page_scroll()

            raw_card_data += await self.extract_card_html()

            if not await self.has_next_page(page_num):
                break
            page_num += 1

        return raw_card_data

    async def page_scroll(self):
        if self.using_scroll:
            await self.page_controller.scroll_down(
                max_scroll=self.max_scroll, time_delay=self.scroll_down_time_delay
            )

    @abstractmethod
    async def extract_card_html(self) -> List:
        pass

    @abstractmethod
    async def has_next_page(self, page_num: int) -> bool:
        pass

    def drop_duplicate_data(self, card_raw_data: List[Tag]):
        return [self.extract_info(card) for card in set(card_raw_data)]

    @abstractmethod
    def extract_info(self, card: Tag) -> Dict:
        pass
