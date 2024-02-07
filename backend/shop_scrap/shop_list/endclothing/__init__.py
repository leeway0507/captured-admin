from typing import List, Dict, Any
import re
from bs4 import BeautifulSoup, Tag
from playwright.async_api import expect

from components.abstract_class.scraper_sub import (
    PwShopListSubScraper,
    ListScrapData,
)

from components.abstract_class.scraper_sub import (
    PwShopPageSubScraper,
)
from random import randint


class PwEndClothingListSubScraper(PwShopListSubScraper):
    def __init__(self):
        super().__init__(
            not_found_xpath=".not_found_xpath",
            shop_name="endclothing",
            using_scroll=True,
            max_scroll=randint(25, 30),
            scroll_step_size=1000,
            cookie_button_xpath=[],
        )

    def __name__(self) -> str:
        return "endclothing"

    async def extract_card_html(self) -> List[Tag] | None:
        card_soup_list = await self._extract()
        return card_soup_list if card_soup_list else None

    async def _extract(self) -> List:
        card_list = await self.page.locator(
            "//*[@data-test-id='ProductCard__ProductCardSC']"
        ).all()

        return [
            BeautifulSoup(
                await r.evaluate("elem => elem.outerHTML"),
                "html.parser",
            )
            for r in card_list
        ]

    async def has_next_page(self, page_num: int) -> bool:
        next_page = self.page.locator(
            "//div[contains(@class,'PageProgressBar__ProgressBarSC')]"
        ).last

        if not await next_page.is_visible():
            return False

        button = self.page.locator(
            "//div[contains(@class,'AnimatedLoader__LoadedItemContainer')]"
        ).last
        await button.click()
        await self.page.evaluate("(async () => { window.scrollBy(0,-1500); })()")
        return True

    def extract_info(self, card: Tag):

        prod_url: str = "https://www.endclothing.com" + card.a["href"]
        price = card.find(attrs={"data-test-id": "ProductCard__ProductFinalPrice"}).text

        return ListScrapData(
            shop_name=self.shop_name,
            brand_name=self.job,
            shop_product_name=card.img["alt"],
            shop_product_img_url=card.img["src"],
            product_url=prod_url,
            price=price,
            product_id=card.a["id"],
        ).model_dump()


class PwEndClothingPageSubScraper(PwShopPageSubScraper):
    def __name__(self) -> str:
        return "endclothing"

    def __init__(self):
        super().__init__()
        self.cookie_button_xpath = [".not_found_page"]

    def get_cookie_button_xpath(self) -> List[str]:
        return ["//*[@id='onetrust-accept-btn-handler']"]

    async def get_size(self) -> List[Dict[str, Any]]:
        # soldout
        if await self.page.locator(
            "//h2[contains(@data-test-id,'SoldOut')]"
        ).is_visible():
            print(f"Out of Stock : {self.job}")
            raise Exception("Out of Stock")

        locator_input = await self.page.locator(
            "//div[contains(@data-test-id,'Size__List')]"
        ).inner_html()
        soup = BeautifulSoup(locator_input, "lxml")

        size_list = []
        for inp in soup.find_all(attrs={"data-test-id": "Size__Button"}):
            s = inp.text
            size_list.append({"shop_product_size": s, "kor_product_size": s})

        if not size_list:
            print(f"Out of Stock : {self.job}")
            raise Exception("Out of Stock")

        return size_list

    async def get_card_info(self):
        original_price = await self.get_original_price()

        return {"product_id": "no need", "original_price": original_price}

    async def get_original_price(self):
        return await self.page.locator(
            "//span[@id='pdp__details__final-price']"
        ).first.inner_text()
