import json
from typing import List, Dict, Any

from bs4 import BeautifulSoup, Tag
from playwright.async_api import expect, Page

from ...shop_product_card_list.schema import ListConfig, ListScrapData

nextpage = "//a[contains(@title,'Next Page')]"


class PwSevenStoreList:
    def __init__(self):
        self.brand_list = json.loads("./brand_list.json")["data"]

    def __name__(self) -> str:
        return "seven_store"

    def get_url(self, brand_name) -> str:
        return self.brand_list.get(brand_name)

    def config(self) -> ListConfig:
        return ListConfig(
            scroll_on=True,
            reverse_not_found_result=True,
            page_reload_after_cookies=False,
            cookie_button_xpath=[
                '//button[@class="btn btn-level1 accept-all-cookies"]'
            ],
            not_found_xpath='//div[contains(@id,"listing-list")]',
        )

    async def extract_card_html(self, page) -> List[Tag] | None:
        product_cards = await page.query_selector('//div[contains(@id,"listing-list")]')
        if product_cards:
            cards = await product_cards.inner_html()
            cards = BeautifulSoup(cards, "html.parser")
            cards = cards.find_all({"attrs": {"class": "nodecor"}})
            assert cards, "load_product_card : No product cards found"
            return cards
        else:
            return None

    def extract_info(self, card: Tag) -> ListScrapData:
        product_name = card.find("a", class_="f-hover-decor").text  # type: ignore
        shop_product_name = product_name + " - " + card["data-nq-product"]  # type: ignore
        price = card.find(attrs={"data-listing": "price"}).text.split(" RRP")[0]  # type: ignore

        return ListScrapData(
            shop_product_name=shop_product_name,
            shop_product_img_url=card.img["src"],  # type: ignore
            product_url=card.img["data-url"],  # type: ignore
            price=price,
        )

    async def get_next_page(self, page: Page, page_num: int) -> bool:
        return False


class PwSevenStorePage:
    def __name__(self) -> str:
        return "seven_store"

    def get_cookie_button_xpath(self) -> List[str]:
        return [""]

    async def get_size_info(self, page: Page) -> List[Dict[str, Any]]:
        locator = page.locator(".product-sizes-title")
        await expect(locator).to_contain_text("Sizes", timeout=10000)

        size_query = await page.query_selector_all(
            '//div[contains(@class, "size-wrapper")]',
        )

        size_list = [await s.inner_text() for s in size_query]

        if not size_list:
            return [{"shop_product_size": "-", "kor_product_size": "-"}]

        l = []
        for s in size_list:
            kor_size = s
            try:
                if float(s) < 15:
                    kor_size = "UK " + s
            except:
                pass
            l.append({"shop_product_size": s, "kor_product_size": kor_size})

        return l

    async def get_product_id(self, page: Page) -> str:
        product_id_text = await page.query_selector(
            '//meta[contains(@name, "description")]',
        )

        try:
            product_id_text = await product_id_text.get_attribute("content")  # type: ignore
            product_id = product_id_text.split(":")[1].replace(" ", "")  # type: ignore
        except:
            product_id = "-"

        return product_id.upper()
