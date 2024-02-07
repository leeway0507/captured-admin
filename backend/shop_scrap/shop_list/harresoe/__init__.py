from typing import List, Dict, Any, Tuple
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


class PwHarresoeListSubScraper(PwShopListSubScraper):
    def __init__(self):
        super().__init__(
            not_found_xpath=".not_found_xpath",
            shop_name="harresoe",
            using_scroll=False,
            max_scroll=0,
            scroll_step_size=1000,
            cookie_button_xpath=[],
        )

    def __name__(self) -> str:
        return "harresoe"

    async def execute(self) -> Tuple[str, List[ListScrapData] | List]:
        default_url = "https://harresoe.com/collections/sale"

        await self.page_handler.sleep_until(randint(0, 3000))

        if self.page.url != default_url:
            await self.page_handler.go_to(default_url)

        return (
            await self.scrap_data()
            if not await self.item_is_not_found()
            else self._failed()
        )

    async def extract_card_html(self) -> List[Tag] | None:
        card_soup_list = await self._extract()
        return card_soup_list if card_soup_list else None

    async def _extract(self) -> List:
        card_list = await self.page.locator(
            '//*[@id="collection-product-repeat"]'
        ).first.inner_html()

        soup = BeautifulSoup(card_list, "html.parser")
        return [
            r
            for r in soup.find_all(
                "div",
                attrs={
                    "class": lambda e: (
                        e.startswith("col-sm-4 col-xs-12 mix") if e else False
                    )
                },
            )
        ]

    async def has_next_page(self, page_num: int) -> bool:
        return False

    def extract_info(self, card: Tag):
        prod_name = card.find("span", id="product-title").text

        product_id = " ".join(prod_name.split(" ")[-3:])

        prod_url: str = "https://harresoe.com" + card.a["href"]
        brand_name = card.find("span", class_="vendor-type").text.split(",")[0].lower()
        shop_product_img_url = "https:" + card.picture.img["src"]
        price: Any = (
            card.find("span", id="price-item")
            .span["data-currency-eur"]
            .replace(".", "")
            .replace("EUR", "")
        )

        return ListScrapData(
            shop_name=self.shop_name,
            brand_name=brand_name,
            shop_product_name=brand_name + " " + prod_name,
            shop_product_img_url=shop_product_img_url,
            product_url=prod_url,
            product_id=product_id,
            price="€ " + price,
        ).model_dump()


## harresoe 특징이라 _product_dict 필요
_product_dict = {}


class PwHarresoePageSubScraper(PwShopPageSubScraper):
    def __name__(self) -> str:
        return "harresoe"

    def __init__(self):
        super().__init__()
        self.cookie_button_xpath = [".not_found_page"]

    async def execute(self):
        # go_to page
        if not _product_dict:
            print("testsesets")
            await self.load_page()
            await self.extract_page_data()

        prod_data = _product_dict.get(self.job["product_url"], None)
        if prod_data:
            return "success", {
                "shop_product_card_id": self.job["shop_product_card_id"],
                "product_url": self.job["product_url"],
                "size": prod_data["size"],
                "card_info": prod_data["card_info"],
            }
        else:
            return "failed", {
                "shop_product_card_id": self.job["shop_product_card_id"],
                "product_url": self.job["product_url"],
                "size": [],
                "card_info": {},
            }

    async def load_page(self):
        # await self.page_handler.go_to(
        #     "file:///Users/yangwoolee/repo/captured/admin/backend/test/test_shop_scrap/test_shop_list/harresoe/list.html"
        # )
        await self.page_handler.go_to("https://harresoe.com/collections/sale")
        await self.page_handler.sleep_until(randint(1000, 2000))

    async def extract_page_data(self):
        l = await self._extract()

        for r in l:
            _product_dict.update(self.extract_info(r))
        return

    async def _extract(self) -> List:
        card_list = await self.page.locator(
            '//*[@id="collection-product-repeat"]'
        ).first.inner_html()

        soup = BeautifulSoup(card_list, "html.parser")
        return [
            r
            for r in soup.find_all(
                "div",
                attrs={
                    "class": lambda e: (
                        e.startswith("col-sm-4 col-xs-12 mix") if e else False
                    )
                },
            )
        ]

    def extract_info(self, card: Tag):
        size = self.get_size_custom(card)
        prod_url: str = "https://harresoe.com" + card.a["href"]
        price: Any = (
            card.find("span", id="price-item")
            .span["data-currency-eur"]
            .replace(".", "")
            .replace("EUR", "")
        )
        prod_name = card.find("span", id="product-title").text

        return {
            prod_url: {
                "size": size,
                "card_info": {
                    "original_price": "€ " + price,
                    "product_id": " ".join(prod_name.split(" ")[-3:]),
                },
            }
        }

    def get_cookie_button_xpath(self) -> List[str]:
        return ["//*[@id='onetrust-accept-btn-handler']"]

    async def get_size(self) -> List[Dict[str, Any]]:
        return [{}]

    def get_size_custom(self, card: Tag) -> List[Dict[str, Any]]:
        size_list = card.find("div", class_="sizes")
        if size_list:
            size_list = size_list.find_all("li")
            return [
                {
                    "shop_product_size": self.get_p_size(i.text),
                    "kor_product_size": self.get_p_size(i.text),
                }
                for i in size_list
            ]
        else:
            return [
                {
                    "shop_product_size": "one size",
                    "kor_product_size": "one size",
                }
            ]

    def get_p_size(self, t: str):
        match = re.search(r"\((.*)\)", t)
        if match:
            t = match.group(1).replace(",", ".").rstrip(".")
        return t

    async def get_card_info(self):
        return {}
