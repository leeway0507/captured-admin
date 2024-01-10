from typing import List, Dict, Any
from bs4 import BeautifulSoup, Tag
from playwright.async_api import expect

from components.abstract_class.scraper_sub import (
    PwShopListSubScraper,
    ListScrapData,
)

from components.abstract_class.scraper_sub import (
    PwShopPageSubScraper,
)


nextpage = "//a[contains(@title,'Next Page')]"


class PwSevenStoreListSubScraper(PwShopListSubScraper):
    def __init__(self):
        super().__init__(
            not_found_xpath=".not_found_xpath",
            shop_name="seven_store",
        )

    def __name__(self) -> str:
        return "seven_store"

    async def extract_card_html(self) -> List[Tag] | None:
        product_cards = await self.page.query_selector(
            '//div[contains(@id,"listing-list")]'
        )
        if product_cards:
            cards = await product_cards.inner_html()
            cards = BeautifulSoup(cards, "html.parser")
            cards = cards.find_all(attrs={"class": "nodecor"})
            # 종종 제품 카드에 홍보용 카드가 들어가는 경우가 있음, 홍보용 카드는 nodecor 클래스는 있지만 id는 없음
            cards = [card for card in cards if card.get("id") is not None]
            assert cards, "load_product_card : No product cards found"
            return cards
        else:
            return None

    async def has_next_page(self, page_num: int) -> bool:
        return False

    def extract_info(self, card: Tag):
        product_name = card.find("a", class_="f-hover-decor").text  # type: ignore
        shop_product_name = product_name + " - " + card["data-nq-product"]  # type: ignore
        price = card.find(attrs={"data-listing": "price"}).text.split(" RRP")[0]  # type: ignore

        return ListScrapData(
            shop_name=self.shop_name,
            brand_name=self.job,
            shop_product_name=shop_product_name,
            shop_product_img_url=card.img["src"],  # type: ignore
            product_url=card.img["data-url"],  # type: ignore
            price=price,
        ).model_dump()


class PwSevenStorePageSubScraper(PwShopPageSubScraper):
    def __name__(self) -> str:
        return "seven_store"

    def __init__(self):
        super().__init__()
        self.cookie_button_xpath = [".not_found_page"]

    def get_cookie_button_xpath(self) -> List[str]:
        return []

    async def get_size(self) -> List[Dict[str, Any]]:
        locator = self.page.locator(".product-sizes-title")
        await expect(locator).to_contain_text("Sizes", timeout=10000)

        size_query = await self.page.query_selector_all(
            '//div[contains(@class, "size-wrapper")]',
        )

        size_list = [await s.inner_text() for s in size_query]

        if not size_list:
            print(f"Out of Stock : {self.job}")
            raise Exception("Out of Stock")

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

    async def get_card_info(self):
        product_id = await self.get_product_id()
        original_price = await self.get_original_price()

        return {"product_id": product_id, "original_price": original_price}

    async def get_product_id(self):
        product_id_text = await self.page.query_selector(
            '//meta[contains(@name, "description")]',
        )

        try:
            product_id_text = await product_id_text.get_attribute("content")  # type: ignore
            product_id = product_id_text.split(":")[1].replace(" ", "")  # type: ignore
        except:
            product_id = "-"

        return product_id.upper()

    async def get_original_price(self):
        xpath = '//div[@class="product-price"]/span'
        if not await self.page.locator(xpath).is_visible():
            xpath = ".product-price.sale"

        result = await self.page.locator(xpath).inner_text()
        return result
