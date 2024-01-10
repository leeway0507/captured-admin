from bs4 import Tag
from datetime import datetime

from typing import Tuple, List

from components.abstract_class.scraper_sub import SubScraper
from model.kream_scraping import KreamScrapingBrandSchema
from components.browser_handler import PwPageHandler


class PwPlatformSubScaper(SubScraper):
    def __init__(self):
        self._page_handler = None
        self._brand_name = None


class PwKreamListSubScraper(SubScraper):
    def __name__(self) -> str:
        return "kream"

    def late_binding(
        self,
        page_handler: PwPageHandler,
        max_scroll: int,
        min_volume: int,
        min_wish: int,
    ):
        self.page_handler = page_handler
        self.page = page_handler.get_page()
        self._max_scroll = max_scroll
        self._min_volume = min_volume
        self._min_wish = min_wish

    @property
    def max_scroll(self):
        return self._max_scroll

    @max_scroll.setter
    def max_scroll(self, value):
        self._max_scroll = value

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

    async def execute(self, time_delay=500) -> Tuple[str, List]:
        await self._go_to_page()
        await self.page_handler.scroll_down(
            max_scroll=self.max_scroll, time_delay=time_delay
        )
        return await self.get_product_card_list()

    async def _go_to_page(self):
        url = f"https://kream.co.kr/search?keyword={self.job}&sort=wish"
        await self.page_handler.go_to(url)
        await self.page_handler.sleep_until(2000)

    async def get_product_card_list(
        self,
    ) -> Tuple[str, List[KreamScrapingBrandSchema] | List]:
        raw_card = await self._extract_card_list_from_page()
        if not raw_card:
            print(f"[{self.__name__}] has no [{self.job}] cards items")
            return "failed", []

        card_data = [self._extract_info(card) for card in raw_card]

        filtered_card_data = self._filter_card_data(card_data)

        return "success", filtered_card_data

    async def _extract_card_list_from_page(self):
        return await self.page_handler.extract_html(".product_card")

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
