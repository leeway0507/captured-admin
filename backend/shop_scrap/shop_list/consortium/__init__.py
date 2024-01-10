from typing import List, Dict, Any
from bs4 import BeautifulSoup, Tag
from components.abstract_class.scraper_sub import (
    PwShopListSubScraper,
    ListScrapData,
)

from components.abstract_class.scraper_sub import (
    PwShopPageSubScraper,
)


class PwConsortiumListSubScraper(PwShopListSubScraper):
    def __name__(self) -> str:
        return "consortium"

    def __init__(self):
        super().__init__(
            shop_name="consortium",
            reverse_not_found_result=True,
            page_reload_after_cookies=False,
            cookie_button_xpath=["#newsletter-modal > a"],
            not_found_xpath='//ul[contains(@class,"products-grid")]',
        )

    # concrete_method
    async def extract_card_html(self) -> List[Tag] | None:
        product_cards = await self.page.query_selector(
            '//ul[contains(@class,"products-grid")]'
        )

        if product_cards:
            cards = await product_cards.inner_html()
            cards = BeautifulSoup(cards, "html.parser")
            cards = cards.find_all(class_="item")
            assert cards, "load_product_card : No product cards found"
            return cards
        else:
            return None

    # concrete_method
    async def has_next_page(self, page_num: int) -> bool:
        button = await self.page.query_selector("//a[contains(@class,'next i-next')]")

        # Consortium Search Engine이 효율적이지 못해 불필요한 데이터가 수집됨.
        num = await self.page.query_selector("//div[@class='page-title']/p")
        if num:
            num = await num.inner_text()
            num = int(num.split(" ")[0])

            if num > 100:
                return False

        if not button:
            return False

        await button.click()
        return True

    # concrete_method
    def extract_info(self, card: Tag) -> Dict:
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
            shop_name=self.shop_name,
            brand_name=self.job,
            shop_product_name=shop_product_name,
            shop_product_img_url=card.img["src"],  # type: ignore
            product_url=card.a["href"],  # type: ignore
            product_id=product_id,
            price=price,
        ).model_dump()


class PwConsortiumPageSubScraper(PwShopPageSubScraper):
    def __name__(self) -> str:
        return "consortium"

    def __init__(self):
        super().__init__()
        self.cookie_button_xpath = ["//*[@id='CybotCookiebotDialogBodyButtonAccept']"]

    async def get_size(self) -> List[Dict[str, Any]]:
        size = await self.scrap_size_from_html()
        return self.size_template(size)

    async def scrap_size_from_html(self):
        size = await self.extract_size_from_html()
        return self.remove_out_of_stock(size)

    async def extract_size_from_html(self):
        size_query = await self.page.query_selector_all("div.input-box>select > option")
        return [await s.inner_text() for s in size_query]

    def remove_out_of_stock(self, size: List[str]) -> List[str]:
        # [1:] 이유 = "Shoe Size" 제거
        return [s for s in size if "Out of Stock" not in s][1:]

    def size_template(self, size: List[str]):
        if not size:
            print(f"Out of Stock : {self.job}")
            raise Exception("Out of Stock")
        return [
            {"shop_product_size": s, "kor_product_size": s.split("-")[0].strip()}
            for s in size
        ]

    async def get_card_info(self):
        product_id = await self.scrap_product_id_from_html()
        product_id = self.product_id_template(product_id)
        original_price = await self.scrap_original_price_from_html()
        return {"product_id": product_id, "original_price": original_price}

    async def scrap_product_id_from_html(self):
        element = await self.page.query_selector('//*[@id="detailsPanel"]/div')
        product_id = await element.inner_text()  # type: ignore
        return product_id.lower()

    def product_id_template(self, text: str):
        product_id = "-"

        if "product code" in text:
            product_id = text.split("product code")[1].strip()

        return product_id.upper()

    async def scrap_original_price_from_html(self):
        xpath = '//div[@class="product-sales"]//span[@class="price"]'
        element = await self.page.query_selector(xpath)
        return await element.inner_text()  # type: ignore
