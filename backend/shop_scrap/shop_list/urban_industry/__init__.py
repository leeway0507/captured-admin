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


class PwUrbanIndustryListSubScraper(PwShopListSubScraper):
    def __init__(self):
        super().__init__(
            not_found_xpath=".not_found_xpath",
            shop_name="urban_industry",
            using_scroll=True,
            max_scroll=10,
            scroll_step_size=1000,
        )

    def __name__(self) -> str:
        return "urban_industry"

    async def _extract(self) -> List:
        card_list = await self.page.locator('//*[@id="product-grid"]/li').all()

        return [await c.inner_html() for c in card_list]

    def _convert(self, extract_list: List[str]) -> List[Tag]:
        return [BeautifulSoup(c, "html.parser") for c in extract_list]

    async def extract_card_html(self) -> List[Tag] | None:
        card_text_list = await self._extract()
        card_soup_list = self._convert(card_text_list)
        return card_soup_list if card_soup_list else None

    async def has_next_page(self, page_num: int) -> bool:
        button = self.page.locator(
            '//*[@id="ProductGridContainer"]//nav//a[@aria-label="Next page"]'
        ).first

        if not await button.is_visible():
            return False

        await button.click()
        return True

    def extract_info(self, card: Tag):
        card_content = card.find_all(class_="card__content")[1]

        prod_color = card_content.h3.a.span.text.strip()
        card_content.h3.a.span.decompose()
        prod_name = card_content.h3.a.text.strip()

        img_url: str = (
            card.find(class_="card__media").img["src"].replace("//", "https://")
        )

        prod_url: str = "https://www.urbanindustry.co.uk" + card_content.h3.a["href"]

        price = (
            card.find(class_="price-item--last")
            .text.replace("KRW", "")
            .split("\xa0")[0]
            .strip()
        )

        return ListScrapData(
            shop_name=self.shop_name,
            brand_name=self.job,
            shop_product_name=prod_name + " " + prod_color,
            shop_product_img_url=img_url,
            product_url=prod_url,
            price=price,
        ).model_dump()


class PwUrbanIndustryPageSubScraper(PwShopPageSubScraper):
    def __name__(self) -> str:
        return "urban_industry"

    def __init__(self):
        super().__init__()
        self.cookie_button_xpath = [".not_found_page"]

    def get_cookie_button_xpath(self) -> List[str]:
        return []

    async def get_size(self) -> List[Dict[str, Any]]:
        locator_input = self.page.locator(
            "//variant-radios/fieldset[contains(@class,'inputfor-size')]/input"
        )
        locator_label = self.page.locator(
            "//variant-radios/fieldset[contains(@class,'inputfor-size')]/label"
        )

        # extract all size list
        product_size_list = []
        for l in await locator_label.all():
            x = await l.inner_text()
            x = x.replace("Variant sold out or unavailable", "").strip()
            product_size_list.append(x)

        # extract available size list
        size_list = []
        for i, l_input in enumerate(await locator_input.all()):
            if not await l_input.get_attribute("class", timeout=5000):
                s = product_size_list[i]
                size_list.append({"shop_product_size": s, "kor_product_size": s})

        if not size_list:
            print(f"Out of Stock : {self.job}")
            raise Exception("Out of Stock")

        return size_list

    async def get_card_info(self):
        product_id = await self.get_product_id()
        original_price = await self.get_original_price()

        return {"product_id": product_id, "original_price": original_price}

    async def get_product_id(self):
        product_id_text = self.page.locator(
            "//div[contains(@class, 'product__description')]"
        )

        try:
            product_id = await product_id_text.inner_text()
            if "product code" in product_id.lower():
                product_id = product_id.lower().split("product code")[-1].split(":")[-1]
            else:
                product_id = "-"
        except:
            product_id = "-"

        return product_id.strip().upper()

    async def get_original_price(self):
        result = await self.page.locator(
            "//span[contains(@class, 'price-item--last')]"
        ).first.inner_text()
        return result.replace("KRW", "").strip().split(" ")[0]
