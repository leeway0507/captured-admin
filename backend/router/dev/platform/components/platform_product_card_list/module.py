from ....utils.browser_controller import PageController as P
from bs4 import Tag
from typing import List
from datetime import datetime
from model.kream_scraping import KreamScrapingBrandSchema


class PwKreamList:
    def __name__(self) -> str:
        return "kream"

    def get_url(self, brand_name: str) -> str:
        return f"https://kream.co.kr/search?keyword={brand_name}&sort=wish"

    def get_card_query(self) -> str:
        return ".product_card"

    async def get_product_card_list(
        self, card_list: List[Tag], min_volume: int, min_wish: int
    ) -> List[KreamScrapingBrandSchema]:
        data = [await self._extract_info(card) for card in card_list]

        filtered_list = list(
            filter(
                lambda x: x.trading_volume >= min_volume and x.wish >= min_wish,
                data,
            )
        )
        return filtered_list

    async def _extract_info(self, card: Tag):
        kream_id = card.find("a", class_="item_inner")["href"].split("/")[-1]  # type: ignore
        kream_product_img_url = card.find("img", class_="image full_width")["src"]  # type: ignore
        kream_product_name = card.find("p", class_="name").get_text(strip=True).lower()  # type: ignore
        brand_name = card.find("p", class_="product_info_brand").get_text(strip=True).lower()  # type: ignore

        updated_at = datetime.now().replace(microsecond=0)

        trading_volume = card.find("div", class_="status_value")
        if trading_volume is None:
            trading_volume = 0
        else:
            trading_volume = self._convert_str_to_int(
                trading_volume.get_text(strip=True)
            )

        wish = card.find("span", class_="wish_figure")
        if wish is None:
            wish = 0
        else:
            wish = self._convert_str_to_int(wish.get_text(strip=True))

        review = card.find("span", class_="review_figure")
        if review is None:
            review = 0
        else:
            review = self._convert_str_to_int(review.get_text(strip=True))

        return KreamScrapingBrandSchema(
            kream_id=kream_id,  # type: ignore
            kream_product_img_url=kream_product_img_url,  # type: ignore
            kream_product_name=kream_product_name,
            brand_name=brand_name,
            trading_volume=trading_volume,
            wish=wish,
            review=review,
            updated_at=updated_at,
        )

    def _convert_str_to_int(self, value: str) -> int:
        """문자열을 숫자로 변환"""

        if "거래" in value:
            value = value.replace("거래", "").replace(" ", "")

        if "만" in value:
            value = value.replace("만", "")
            return int(float(value) * 10000)

        value = value.replace(",", "")
        return int(value)
