from typing import Any, Dict, List
from playwright.async_api import Page
from bs4 import BeautifulSoup


class Pw18montrosePage:
    def __name__(self) -> str:
        return "18montrose"

    def get_cookie_button_xpath(self) -> List[str]:
        return [""]

    async def get_size_info(self, page: Page) -> List[Dict[str, Any]]:
        size_list = await page.query_selector(
            '//div[contains(@id,"divSize")]',
        )
        if size_list:
            size_list = await size_list.inner_html()
            soup = BeautifulSoup(size_list, "html.parser")
            size_list = soup.find_all("a")
            size_list = [size.text.strip().split("(")[0] for size in size_list]
        else:
            size_list = [{"shop_product_size": "-", "kor_product_size": "-"}]

        return [{"shop_product_size": s, "kor_product_size": s} for s in size_list]

    async def get_product_id(self, page: Page) -> str:
        return "-"
