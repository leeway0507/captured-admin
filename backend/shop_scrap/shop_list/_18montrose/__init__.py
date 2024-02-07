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

nextpage = "//a[contains(@title,'Next Page')]"


class Pw18montroseListSubScraper(PwShopListSubScraper):
    def __init__(self):
        super().__init__(
            not_found_xpath=".not_found_xpath",
            shop_name="_18montrose",
            using_scroll=True,
            max_scroll=randint(0, 10),
            scroll_step_size=1000,
            cookie_button_xpath=["//*[@id='onetrust-accept-btn-handler']"],
        )

    def __name__(self) -> str:
        return "_18montrose"

    async def extract_card_html(self) -> List[Tag] | None:
        card_soup_list = await self._extract()
        return card_soup_list if card_soup_list else None

    async def _extract(self) -> List:
        card_list = await self.page.locator(
            '//*[@id="productlistcontainer"]/ul'
        ).first.inner_html()

        soup = BeautifulSoup(card_list, "html.parser")
        return [r for r in soup.find_all("li")]

    async def has_next_page(self, page_num: int) -> bool:
        button = self.page.locator("//a[contains(@class,'swipeNextClick')]").first

        if not await button.is_visible():
            return False

        await button.click()
        return True

    def extract_info(self, card: Tag):
        prod_name = card["li-url"].replace("-", " ").replace("/", "").split("#")[0]
        sku = card["li-url"].split("#colcode=")[1]

        prod_url: str = "https://www.18montrose.com" + card["li-url"]

        return ListScrapData(
            shop_name=self.shop_name,
            brand_name=self.job,
            shop_product_name=prod_name + "-" + sku,
            shop_product_img_url=card.img["src"],
            product_url=prod_url,
            price=f'£ {card["li-price"]}',
        ).model_dump()


class Pw18montrosePageSubScraper(PwShopPageSubScraper):
    def __name__(self) -> str:
        return "_18montrose"

    def __init__(self):
        super().__init__()
        self.cookie_button_xpath = [".not_found_page"]

    def get_cookie_button_xpath(self) -> List[str]:
        return ["//*[@id='onetrust-accept-btn-handler']"]

    async def get_size(self) -> List[Dict[str, Any]]:
        locator_input = await self.page.locator("//*[@id='ulSizes']").inner_html()
        soup = BeautifulSoup(locator_input, "lxml")

        size_list = []
        for inp in soup.find_all("li"):
            if "greyOut" in inp["class"]:
                continue

            s = inp.text.replace("\n", "")
            match = re.search(r"\((\d+\.*\d*)\)", s)
            if match:
                s = match.group(1)
            size_list.append({"shop_product_size": s, "kor_product_size": s})

        if not size_list:
            print(f"Out of Stock : {self.job}")
            raise Exception("Out of Stock")

        return size_list

    async def get_card_info(self):
        original_price = await self.get_original_price()

        return {"product_id": "no product id", "original_price": original_price}

    async def get_original_price(self):
        return await self.page.locator(
            "//span[@id='lblSellingPrice']"
        ).first.inner_text()
