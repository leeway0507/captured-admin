import json
from typing import List, Dict, Any
from bs4 import BeautifulSoup, Tag
from playwright.async_api import Page
from ..parent_class import PwShopList, PwShopPage

from ...shop_product_card_list.schema import ListConfig, ListScrapData


class PwConsortiumList(PwShopList):
    def __name__(self) -> str:
        return "consortium"

    def config(self) -> ListConfig:
        return ListConfig(
            scroll_on=False,
            reverse_not_found_result=True,
            page_reload_after_cookies=False,
            cookie_button_xpath=["#newsletter-modal > a"],
            not_found_xpath='//ul[contains(@class,"products-grid")]',
        )

    async def extract_card_html(self, page) -> List[Tag] | None:
        product_cards = await page.query_selector(
            '//ul[contains(@class,"products-grid")]'
        )
        if product_cards:
            cards = await product_cards.inner_html()
            cards = BeautifulSoup(cards, "html.parser")
            cards = cards.find_all(attrs={"class": "item"})
            assert cards, "load_product_card : No product cards found"
            return cards
        else:
            return None

    def extract_info(self, card: Tag, brand_name: str) -> ListScrapData:
        price = card.find(attrs={"class": "special-price"})
        if price:
            price = price.text
        else:
            price = card.find(attrs={"class": "regular-price"})
            assert price, "extract_info : No price found"
            price = price.text

        price = price.replace("\n", "").replace(" ", "").rstrip("")

        shop_product_name = (
            card.a["href"].split("https://www.consortium.co.uk/")[-1].split(".html")[0]  # type: ignore
        )

        # product_id 추출
        shop_product_color = card.find("h4", attrs={"class": "product-colour"})
        if shop_product_color:
            shop_product_color_last = (
                shop_product_color.text.replace("(", "")
                .replace(")", "")
                .split("/")[-1]
                .split(" ")[-1]
                .split("-")[-1]
                .lower()
            )
        else:
            shop_product_color_last = None

        def rindex(lst, value):
            lst.reverse()
            i = lst.index(value)
            lst.reverse()
            return len(lst) - i - 1

        product_id = "-"

        if shop_product_color_last and shop_product_color_last in shop_product_name:
            product_id = ""
            idx = rindex(shop_product_name.split("-"), shop_product_color_last) + 1
            product_id = "-".join(shop_product_name.split("-")[idx:])

        return ListScrapData(
            shop_name=self.__name__(),
            brand_name=brand_name,
            shop_product_name=shop_product_name,
            shop_product_img_url=card.img["src"],  # type: ignore
            product_url=card.a["href"],  # type: ignore
            product_id=product_id,
            price=price,
        )

    async def get_next_page(self, page: Page, page_num: int) -> bool:
        button = await page.query_selector("//a[contains(@class,'next i-next')]")

        # Consortium Search Engine이 효율적이지 못해 불필요한 데이터가 수집됨.
        # 이를 방지하기 위한 용도임(brand search에는 불필요)
        num = await page.query_selector("//div[@class='page-title']/p")
        if num:
            num = await num.inner_text()
            num = int(num.split(" ")[0])

            if num > 100:
                return False

        if not button:
            return False

        await button.click()
        return True


class PwConsortiumPage(PwShopPage):
    def __name__(self) -> str:
        return "consortium"

    def get_cookie_button_xpath(self) -> List[str]:
        return ['//*[@id="CybotCookiebotDialogBodyButtonAccept"]']

    async def get_size_info(self, page: Page) -> List[Dict[str, Any]]:
        size_query = await page.query_selector_all("div.input-box>select > option")

        size_list = [await s.inner_text() for s in size_query]
        size_list = [size for size in size_list if "Out of Stock" not in size][1:]
        if not size_list:
            return [{"shop_product_size": "-", "kor_product_size": "-"}]

        return [
            {"shop_product_size": s, "kor_product_size": s.split("-")[0].strip()}
            for s in size_list
        ]

    async def get_product_id(self, page: Page) -> str:
        product_id_text = await page.query_selector('//*[@id="detailsPanel"]/div')
        product_id_text = await product_id_text.inner_text()  # type: ignore
        text = product_id_text.lower()
        if "product code" in text:
            product_id = text.split("product code")[1].strip()
        else:
            product_id = "-"

        return product_id.upper()
