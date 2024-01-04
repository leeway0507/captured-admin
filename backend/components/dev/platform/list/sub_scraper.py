from abc import ABC, abstractmethod
from typing import Any, List, Protocol

from ...utils.browser_controller import PageController as P
from bs4 import Tag
from typing import List
from datetime import datetime
from model.kream_scraping import KreamScrapingBrandSchema

from components.dev.utils.browser_controller import PageController as P
from components.dev.sub_scraper import SubScraper


class PlatformListSubScraper(SubScraper):
    def __init__(self):
        self._page_controller = None
        self._brand_name = None
        self._min_volume = 0
        self._min_wish = 0

    def late_binding(self, page_controller: P, min_volume: int, min_wish: int):
        self.page_controller = page_controller
        self.min_volume = min_volume
        self.min_wish = min_wish

    async def execute(
        self, max_scroll=20, time_delay=500
    ) -> List[KreamScrapingBrandSchema] | List:
        await self._goto_list_page()
        await self.page_controller.scroll_down(
            max_scroll=max_scroll, time_delay=time_delay
        )
        return await self.get_product_card_list()

    @property
    def page_controller(self):
        if not self._page_controller:
            raise ValueError(
                """
                page_controller is None. Plase update page_controller 
                """
            )
        return self._page_controller

    @page_controller.setter
    def page_controller(self, value):
        self._page_controller = value

    @property
    def brand_name(self):
        if not self._brand_name:
            raise ValueError(
                """
                brand_name is None. Plase update brand_name.
                """
            )
        return self._brand_name

    @brand_name.setter
    def brand_name(self, value):
        self._brand_name = value

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
        await self.page_controller.go_to(url)
        await self.page_controller.sleep_until(2000)

    @abstractmethod
    def __name__(self) -> str:
        ...

    @abstractmethod
    def get_url(self) -> str:
        ...

    @abstractmethod
    async def get_product_card_list(self) -> List[Any]:
        ...


class PwKreamListSubScraper(PlatformListSubScraper):
    def __name__(self) -> str:
        return "kream"

    def get_url(self) -> str:
        return f"https://kream.co.kr/search?keyword={self.job}&sort=wish"

    async def get_product_card_list(self) -> List[KreamScrapingBrandSchema] | List:
        raw_card = await self._extract_card_list_from_page()
        if not raw_card:
            print(f"[{self.__name__}] has no [{self.job}] cards items")
            return []

        card_data = [self._extract_info(card) for card in raw_card]

        filtered_card_data = self._filter_card_data(card_data)

        return filtered_card_data

    async def _extract_card_list_from_page(self):
        return await self.page_controller.extract_html(".product_card")

    def _extract_info(self, card: Tag):
        return KreamScrapingBrandSchema(
            updated_at=datetime.now().replace(microsecond=0),
            kream_id=self._get_kream_id(card),
            kream_product_img_url=self._get_kream_product_img_url(card),
            kream_product_name=self._get_kream_product_name(card),
            brand_name=self._get_brand_name(card),
            trading_volume=self._get_trading_volume(card),
            wish=self._get_wish_count(card),
            review=self._get_review_count(card),
        )

    def _filter_card_data(self, card_data: List[KreamScrapingBrandSchema]):
        return list(
            filter(
                lambda x: x.trading_volume >= self.min_volume
                and x.wish >= self.min_wish,
                card_data,
            )
        )

    def _get_kream_id(self, card: Tag) -> int:
        return int(card.find("a", class_="item_inner")["href"].split("/")[-1])  # type: ignore

    def _get_kream_product_img_url(self, card: Tag) -> str:
        return card.find("img", class_="image full_width")["src"]  # type: ignore

    def _get_kream_product_name(self, card: Tag) -> str:
        return card.find("p", class_="name").get_text(strip=True).lower()  # type: ignore

    def _get_brand_name(self, card: Tag) -> str:
        return card.find("p", class_="product_info_brand").get_text(strip=True).lower()  # type: ignore

    def _get_trading_volume(self, card: Tag) -> int:
        trading_volume_element = card.find("div", class_="status_value")

        trading_volume = 0
        if trading_volume_element is not None:
            trading_volume = self._convert_str_to_int(
                trading_volume_element.get_text(strip=True)
            )

        return trading_volume

    def _get_wish_count(self, card: Tag) -> int:
        wish_element = card.find("span", class_="wish_figure")

        wish = 0
        if wish_element is not None:
            wish = self._convert_str_to_int(wish_element.get_text(strip=True))

        return wish

    def _get_review_count(self, card: Tag) -> int:
        review_element = card.find("span", class_="review_figure")

        review = 0
        if review_element is not None:
            review = self._convert_str_to_int(review_element.get_text(strip=True))

        return review

    def _convert_str_to_int(self, value: str) -> int:
        """문자열을 숫자로 변환"""

        if "거래" in value:
            value = value.replace("거래", "").replace(" ", "")

        if "만" in value:
            value = value.replace("만", "")
            return int(float(value) * 10000)

        value = value.replace(",", "")
        if value == "":
            return 0
        return int(value)
