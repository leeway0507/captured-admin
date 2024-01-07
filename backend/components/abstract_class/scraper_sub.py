from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Optional, TypeVar
from ..browser_handler import PageHandler, PwPageHandler
from bs4 import Tag
from pydantic import BaseModel
from ..env import dev_env

T = TypeVar("T")


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


class PwPlatformSubScaper(SubScraper):
    def __init__(self):
        self._page_handler = None
        self._brand_name = None

    async def execute(self, max_scroll=20, time_delay=500) -> Tuple[str, List]:
        await self._goto_list_page()
        await self.page_handler.scroll_down(
            max_scroll=max_scroll, time_delay=time_delay
        )
        return await self.get_product_card_list()

    @property
    def page_handler(self):
        if not self._page_handler:
            raise ValueError(
                """
                page_handler is None. Plase update page_handler 
                """
            )
        return self._page_handler

    @page_handler.setter
    def page_handler(self, value):
        self._page_handler = value

    @property
    def min_volume(self):
        return self._min_volume

    @min_volume.setter
    def min_volume(self, value):
        self._min_volume = value

    @property
    def min_wish(self):
        return self._min_wish

    @min_wish.setter
    def min_wish(self, value):
        self._min_wish = value

    async def _goto_list_page(self):
        url = self.get_url()
        await self.page_handler.go_to(url)
        await self.page_handler.sleep_until(2000)

    @abstractmethod
    def __name__(self) -> str:
        ...

    @abstractmethod
    def get_url(self) -> str:
        ...

    @abstractmethod
    async def get_product_card_list(self) -> Tuple[str, List]:
        ...


class ListScrapData(BaseModel):
    shop_name: str
    brand_name: str = ""
    shop_product_name: str
    shop_product_img_url: str
    product_url: str
    product_id: Optional[str] = None
    price: str


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

    def late_binding(self, page_handler: PwPageHandler):
        self.page_handler = page_handler
        self.page = page_handler.get_page()

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
        await self.page_handler.go_to(url)
        await self.page_handler.sleep_until(self.wait_until_load)

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

            raw_card_data += await self.extract_card_html()

            if not await self.has_next_page(page_num):
                break
            page_num += 1

        return raw_card_data

    async def page_scroll(self):
        if self.using_scroll:
            await self.page_handler.scroll_down(
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


class PwShopPageSubScraper(SubScraper):
    def __init__(self):
        self._cookie_button_xpath = None
        self.wait_until_load = 2000

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
        product_id = await self.get_product_id()
        return "success", {
            "shop_product_card_id": self.job["shop_product_card_id"],
            "product_url": self.job["product_url"],
            "size": size,
            "product_id": product_id,
        }

    async def load_page(self):
        url = self.get_url()
        await self.page_handler.go_to(url)
        await self.page_handler.sleep_until(self.wait_until_load)

    def get_url(self) -> str:
        return self.job["product_url"]

    async def handle_cookies(self):
        if self.cookie_button_xpath:
            await self.page_handler.handle_cookies(self.cookie_button_xpath)

    @abstractmethod
    async def get_product_id(self):
        pass

    @abstractmethod
    async def get_size(self):
        pass
