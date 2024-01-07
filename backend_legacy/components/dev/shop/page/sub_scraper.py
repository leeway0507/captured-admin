from typing import List
from ...utils.browser_controller import PageController as P

from components.dev.sub_scraper import SubScraper
from abc import abstractmethod


class PwShopPageSubScraper(SubScraper):
    def __init__(self):
        self._cookie_button_xpath = None
        self.wait_until_load = 2000
        self._shop_product_list = None

    @property
    def cookie_button_xpath(self):
        if not self._cookie_button_xpath:
            raise ValueError(
                "cookie_button_xpath is None. Please update cookie_button_xpath"
            )
        return self._cookie_button_xpath

    @cookie_button_xpath.setter
    def cookie_button_xpath(self, cookie_button_xpath: List[str]):
        self._cookie_button_xpath = cookie_button_xpath

    @property
    def shop_product_list(self):
        if not self._shop_product_list:
            raise ValueError(
                "shop_product_list is None. Please update shop_product_list"
            )
        return self._shop_product_list

    @shop_product_list.setter
    def shop_product_list(self, shop_product_list: List):
        self._shop_product_list = shop_product_list

    def late_binding(self, page_controller: P):
        self.page_controller = page_controller
        self.page = self.page_controller.get_page()

    async def execute(self):
        # go_to page
        await self.load_page()

        # handle cookies
        await self.handle_cookies()

        # scrap size and product_id
        size = await self.get_size()
        product_id = await self.get_product_id()
        return "success", {
            "shop_product_card_id": self.job,
            "size": size,
            "product_id": product_id,
        }

    async def load_page(self):
        url = self.get_url()
        await self.page_controller.go_to(url)
        await self.page_controller.sleep_until(self.wait_until_load)

    def get_url(self) -> str:
        product_list = self.shop_product_list

        for product in product_list:
            if product["shop_product_card_id"] == int(self.job):
                return product["product_url"]

        raise Exception(f"product_url: {self.job} not found")

    async def handle_cookies(self):
        if self.cookie_button_xpath:
            await self.page_controller.handle_cookies(self.cookie_button_xpath)

    @abstractmethod
    async def get_product_id(self):
        pass

    @abstractmethod
    async def get_size(self):
        pass
