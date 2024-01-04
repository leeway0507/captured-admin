import json
from typing import List, Dict, Any
from playwright.async_api import Page
from ...list.schema import ListConfig, ListScrapData
from bs4 import BeautifulSoup, Tag
from ..parent_class import PwShopList, PwShopPage

# async def a_few_store_product_list(
#     page: Page, brand_name: str, brand_url: str, **_kwargs
# ):
#     return await get_a_few_store_product_list(page, brand_name, brand_url)


class PwAfewStoreList(PwShopList):
    def __name__(self) -> str:
        return "a_few_store"

    def config(self) -> ListConfig:
        return ListConfig(
            scroll_on=True,
            reverse_not_found_result=True,
            page_reload_after_cookies=False,
            not_found_xpath='//div[contains(@class,"findify-components-search--lazy-results")]',
            cookie_button_xpath=["button.klaviyo-close-form"],
            wait_until_load=10000,
        )

    async def extract_card_html(self, page: Page) -> List[Tag] | None:
        global soup
        product_cards = await page.query_selector(
            '//div[contains(@class,"findify-components-search--lazy-results")]'
        )
        if product_cards:
            cards = await product_cards.inner_html()
            soup = BeautifulSoup(cards, "html.parser")
            cards = soup.find_all(attrs={"class": "product-card"})
            assert cards, "load_product_card : No product cards found"
            return cards
        else:
            return None

    def extract_info(self, card: Tag, brand_name: str) -> ListScrapData:
        price = card.find(class_="price").text  # type: ignore
        id = card["id"].replace("findify_", "")  # type: ignore

        return ListScrapData(
            shop_name=self.__name__(),
            brand_name=brand_name,
            shop_product_name=card.img["data-src"].split("/")[-1],  # type: ignore
            shop_product_img_url=card.img["src"],  # type: ignore
            product_url=card["href"],  # type: ignore
            product_id=id,
            price=price,
        )

    async def get_next_page(self, page: Page, page_num: int) -> bool:
        xpath = "//button[contains(@class,'findify-components--button btn btn-outline-dark')]"
        button = await page.query_selector(xpath)

        if not button:
            return False

        await button.click()
        await page.wait_for_timeout(5000)
        return True


class PwAfewStorePage(PwShopPage):
    def __name__(self) -> str:
        return "a_few_store"

    def get_cookie_button_xpath(self) -> List[str]:
        return ['//*[@id="CybotCookiebotDialogBodyButtonAccept"]']

    async def get_size_info(self, page: Page) -> List[Dict[str, Any]]:
        size_query = await page.query_selector('//div[contains(@class,"size-picker")]')

        if size_query:
            sizes = await size_query.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            size_list = soup.find_all("a")
            size_list = [
                size.text
                for size in size_list
                if "disabled" not in size.get("class", [])
            ]
            size_btn = await page.query_selector(
                "button.btn.btn-sm.btn-dark.dropdown-toggle"
            )
            if size_btn:
                btn_text = await size_btn.query_selector("strong")
                btn_text = await btn_text.inner_text()  # type: ignore
                size_list = [f"{btn_text} {size}" for size in size_list]
        else:
            return [{"shop_product_size": "-", "kor_product_size": "-"}]

        return [{"shop_product_size": s, "kor_product_size": s} for s in size_list]

    async def get_product_id(self, page: Page) -> str:
        product_id_text = await page.query_selector("//*[@id='content-details']")
        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            text_list = product_id_text.split(" ")
            product_id_idx = text_list.index("Style") + 1
            product_id = text_list[product_id_idx]
        else:
            product_id = "-"
        return product_id.upper()
