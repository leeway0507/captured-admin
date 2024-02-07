from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Optional
from ..browser_handler import PageHandler, PwPageHandler
from bs4 import Tag
from pydantic import BaseModel
from ..env import dev_env
from random import randint


class SubScraper(ABC):
    def __init__(self):
        self._page_handler = None
        self._job = None

    @abstractmethod
    def __name__(self) -> str:
        pass

    def late_binding(self, page_handler: PageHandler):
        self.page_handler = page_handler
        self.page = page_handler.get_page()

    def allocate_job(self, job: Any):
        self.job = job

    @abstractmethod
    async def execute() -> Tuple[str, Dict | List]:
        pass

    @property
    def page_handler(self):
        if not self._page_handler:
            raise ValueError("page_handler is None. Please update page_handler")

        return self._page_handler

    @page_handler.setter
    def page_handler(self, page_handler: PageHandler):
        self._page_handler = page_handler

    @property
    def job(self):
        if not self._job:
            raise ValueError("job is None. Please update job")
        return self._job

    @job.setter
    def job(self, job: Any):
        self._job = job


class ListScrapData(BaseModel):
    shop_name: str
    brand_name: str = ""
    shop_product_name: str
    shop_product_img_url: str
    product_url: str
    product_id: Optional[str] = None
    price: str


class PwShopListSubScraper(SubScraper):
    def __init__(
        self,
        not_found_xpath: str,
        shop_name: str = "",
        reverse_not_found_result: bool = False,
        page_reload_after_cookies: bool = False,
        cookie_button_xpath: List[str] = [],
        using_scroll=False,
        scroll_down_time_delay=1000,
        max_scroll: int = 10,
        scroll_step_size: int = 400,
    ):
        super().__init__()
        self.not_found_xpath: str = not_found_xpath
        self.shop_name: str = shop_name
        self.reverse_not_found_result: bool = reverse_not_found_result
        self.page_reload_after_cookies: bool = page_reload_after_cookies
        self.cookie_button_xpath: List[str] = cookie_button_xpath
        self.using_scroll = using_scroll
        self.scroll_down_time_delay = scroll_down_time_delay
        self.max_scroll: int = max_scroll
        self.scroll_step_size: int = scroll_step_size

    def late_binding(self, page_handler: PwPageHandler, shop_name: str):
        self.page_handler = page_handler
        self.page = page_handler.get_page()
        self.shop_name = shop_name

    async def execute(self) -> Tuple[str, List[ListScrapData] | List]:
        await self.page_handler.sleep_until(randint(0, 3000))
        await self.load_page()
        await self.handle_cookies()
        return (
            await self.scrap_data()
            if not await self.item_is_not_found()
            else self._failed()
        )

    async def load_page(self):
        url = self.get_url()
        await self.page_handler.go_to(url)
        await self.page_handler.sleep_until(randint(500, 3000))

    def get_url(self) -> str:
        brand_list = self._load_brand_list()["data"]

        for brand in brand_list:
            if brand["brand_name"] == self.job:
                return brand["brand_url"]

        raise Exception(f"brand_name: {self.job} not found")

    def _load_brand_list(self):
        import os
        import json

        path = os.path.join(dev_env.SHOP_LIST_DIR, self.shop_name, "brand_list.json")

        with open(path) as f:
            return json.load(f)

    async def handle_cookies(self):
        if self.cookie_button_xpath:
            await self.page_handler.handle_cookies(self.cookie_button_xpath)

        if self.page_reload_after_cookies:
            await self.load_page()

    async def item_is_not_found(self):
        not_found = await self.page_handler.check_curr_page_is_not_found_page(
            self.not_found_xpath
        )

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

            await self.page_handler.sleep_until(randint(500, 5000))
            raw_card_data += await self.extract_card_html()

            if not await self.has_next_page(page_num):
                break
            page_num += 1

        return raw_card_data

    async def page_scroll(self):
        if self.using_scroll:
            await self.page_handler.scroll_down(
                max_scroll=self.max_scroll,
                time_delay=self.scroll_down_time_delay,
                step_size=self.scroll_step_size,
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


class PwShopPageSubScraper(SubScraper):
    def __init__(self):
        self._cookie_button_xpath = None

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

    def late_binding(self, page_handler: PwPageHandler):
        self.page_handler = page_handler
        self.page = self.page_handler.get_page()

    async def execute(self):
        # go_to page
        await self.load_page()

        # handle cookies
        await self.handle_cookies()

        # scrap size and product_id
        size = await self.get_size()
        card_info = await self.get_card_info()
        return "success", {
            "shop_product_card_id": self.job["shop_product_card_id"],
            "product_url": self.job["product_url"],
            "size": size,
            "card_info": card_info,
        }

    def _load_brand_list(self):
        import os
        import json

        path = os.path.join(dev_env.SHOP_LIST_DIR, self.__name__(), "brand_list.json")

        with open(path) as f:
            return json.load(f)

    async def load_page(self):
        url = self.get_url()
        await self.page_handler.go_to(url)
        await self.page_handler.sleep_until(randint(1000, 2000))

    def get_url(self) -> str:
        return self.job["product_url"]

    async def handle_cookies(self):
        if self.cookie_button_xpath:
            await self.page_handler.handle_cookies(self.cookie_button_xpath)

    @abstractmethod
    async def get_card_info(self):
        pass

    @abstractmethod
    async def get_size(self):
        pass
