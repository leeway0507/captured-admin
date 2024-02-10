from typing import List, Dict, Any, Tuple
import json
from random import randint

from components.abstract_class.scraper_sub import (
    PwShopListSubScraper,
    ListScrapData,
)

from components.abstract_class.scraper_sub import (
    PwShopPageSubScraper,
)
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class PwSsenseListSubScraper(PwShopListSubScraper):
    def __init__(self):
        super().__init__(
            not_found_xpath=".not_found_xpath",
            shop_name="ssense",
            using_scroll=False,
        )

    def __name__(self) -> str:
        return "ssense"

    async def execute(self) -> Tuple[str, List[ListScrapData] | List]:
        await self._extract(self.get_url())

        soup_list = []
        next_page = True
        while next_page:
            soup = await self.extract_card_html()

            if soup == "Access denied":
                next_page = False
                return ("Failed", [])

            soup_list.extend(soup)

            next_page_url = self.has_next_page_url()
            if next_page_url:
                print("ssense || Current Scraping......")
                await self._extract(next_page_url)
            else:
                next_page = False

            await asyncio.sleep(randint(1, 5))

        return ("success", [self.extract_info(s) for s in soup_list])

    async def _extract(self, url: str):
        headers = {
            "User-Agent": user_agent_string[randint(0, len(user_agent_string) - 1)],
            "Referer": "https://www.google.com/",
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                self.soup = BeautifulSoup(await response.text(), "xml")

        await asyncio.sleep(randint(1, 5))

    async def extract_card_html(self) -> List | str:
        if self.soup.title.text == "Access to this page has been denied":
            print("Ssense : 'Access to this page has been denied'", self.job)
            return "Access denied"

        return [
            s.text
            for s in self.soup.find_all("script", attrs={"type": "application/ld+json"})
        ]

    def has_next_page_url(self):
        for s in self.soup.find_all(
            "span", class_="pagination__direction s-text s-text--uppercase"
        ):
            if "next" in s.text:
                return "https://www.ssense.com/en-kr" + s.parent["href"]
        return None

    async def has_next_page(self, page_num: int) -> bool:
        return False

    def extract_info(self, card: str):

        id_json = json.loads(card)

        curr_dict = {
            "USD": "$",
            "EUR": "€",
            "KRW": "₩",
        }

        price = (
            curr_dict[id_json["offers"]["priceCurrency"]]
            + " "
            + str(id_json["offers"]["price"])
        )
        prod_url = "https://www.ssense.com/en-kr" + id_json["url"]

        return ListScrapData(
            shop_name=self.shop_name,
            brand_name=id_json["brand"]["name"].lower(),
            shop_product_name=id_json["name"],
            shop_product_img_url=id_json["image"],
            product_url=prod_url,
            price=price,
        ).model_dump()


class PwSsensePageSubScraper(PwShopPageSubScraper):
    def __name__(self) -> str:
        return "ssense"

    def __init__(self):
        super().__init__()
        self.cookie_button_xpath = [".not_found_page"]

    def get_cookie_button_xpath(self) -> List[str]:
        return []

    async def execute(self):
        await self.load_page()
        await self.check_failed()
        await self.extract_soup()

        size = await self.get_size()
        card_info = self.get_card_info()

        return "success", {
            "shop_product_card_id": self.job["shop_product_card_id"],
            "product_url": self.job["product_url"],
            "size": size,
            "card_info": card_info,
        }

    async def extract_soup(self):
        self.soup = BeautifulSoup(
            await self.page.locator('//main[@id="wrap"]').inner_html(),
            "xml",
        )

        await asyncio.sleep(randint(1, 5))
        return

    async def check_failed(self):
        captcha = await self.page.locator("//title").last.inner_text()

        if captcha == "Access to this page has been denied":
            raise RuntimeError("ssense : captcha Detected")

    async def get_size(self) -> List[Dict[str, Any]]:
        add_to_bag = await self.check_add_to_bag_box_exist()

        size_soup = self.soup.find("select", {"id": "pdpSizeDropdown"})
        if not size_soup and add_to_bag.text == "Add to bag":
            return [{"shop_product_size": "one size", "kor_product_size": "one size"}]

        # extract all size list
        size_list = []
        for soup in size_soup.find_all("option"):
            if not soup.has_attr("disabled"):
                s = soup["value"].split("_")[0]
                size_list.append({"shop_product_size": s, "kor_product_size": s})

        if not size_list:
            print(f"Out of Stock : {self.job}")
            raise Exception("Out of Stock")

        return size_list

    async def check_add_to_bag_box_exist(self):
        box = self.soup.find("button", attrs={"id": "pdpAddToBagButton"})
        if not box:
            print(f"Out of Stock : {self.job}")
            raise Exception("Page Not Found - Out of Stock")
        return box

    def get_card_info(self):
        original_price = self.get_original_price()

        return {"product_id": "no product id", "original_price": original_price}

    def get_original_price(self):
        s = self.soup.find("script", attrs={"type": "application/ld+json"})
        id_json = json.loads(s.text)

        curr_dict = {
            "USD": "$",
            "EUR": "€",
            "KRW": "₩",
        }

        price = (
            curr_dict[id_json["offers"]["priceCurrency"]]
            + " "
            + str(id_json["offers"]["price"])
        )
        return price
