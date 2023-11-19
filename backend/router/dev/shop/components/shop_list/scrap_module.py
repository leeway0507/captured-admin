import os
import json
from typing import Dict, Callable, List, Any
from datetime import date, datetime
from dotenv import dotenv_values

from bs4 import BeautifulSoup
from playwright.async_api import Page
import asyncio
import pandas as pd
from logs.make_log import make_logger
from model.db_model_shop import ShopProductCardSchema

config = dotenv_values(".env.dev")


class ScrapModule:
    @classmethod
    async def load_page(cls, page: Page, url, sleep_time=1):
        """페이지 로드"""
        await page.goto(url)
        await page.wait_for_load_state(state="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)
        await asyncio.sleep(sleep_time)
        return page

    @classmethod
    async def load_product_card(cls, page, xpath, attr: Dict):
        product_cards = await page.query_selector(xpath)
        if product_cards:
            cards = await product_cards.inner_html()
            cards = BeautifulSoup(cards, "html.parser")
            cards = cards.find_all(**attr)
            assert cards, "load_product_card : No product cards found"
            return cards
        else:
            return []

    @classmethod
    async def check_not_found(cls, page, xpath):
        not_found_page = await page.query_selector(xpath)
        if not_found_page:
            return True
        return False

    @classmethod
    async def scroll_down(
        cls, page: Page, max_scroll: int = 10, time_delay: float = 0.5
    ):
        """
        스크롤 다운

            Args:
                page (Page): Playwright Page
                max_scroll (int, optional): 최대 스크롤 횟수. Defaults to 2.
                time_delay (float, optional): 스크롤 간 딜레이. Defaults to 0.5.

            Returns:
                None
        """
        i = 0
        while i < max_scroll:
            i += 1
            await page.evaluate("(async () => { window.scrollBy(0, 400); })()")
            await asyncio.sleep(time_delay)

    @classmethod
    async def scrap_list_logic(
        cls,
        page: Page,
        shop_name: str,
        brand_name: str,
        search_url: str,
        cookie_xpath: str | List[str],
        not_found_xpath: str,
        product_card_xpath: str,
        card_attr: dict,
        next_page_xpath: str,
        get_item_info: Callable,
        get_next_page: Callable,
        scroll_on: bool = False,
        reverse_not_found_result=False,
        wait_for_loading=1000,
        page_reload_after_cookies=False,
        **kwargs,
    ) -> List[ShopProductCardSchema]:
        """
        shopping_mall에 대한 리스트 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 리스트 URL

            Returns:
                List[Any]: [urls]
        """

        log = make_logger(f"logs/shop_product_card_list/{shop_name}.log", shop_name)

        # 1. load_page
        await ScrapModule.load_cookies(page)
        local_page = await ScrapModule.load_page(page, search_url)
        assert local_page, log.error(f"[{shop_name}] page load failed")

        time = kwargs.get("wait_time_for_verification")
        if time and isinstance(time, int):
            await asyncio.sleep(time)

        # 1-1. deal with cookies
        if isinstance(cookie_xpath, str):
            cookie_xpath = [cookie_xpath]
        for xpath in cookie_xpath:
            cookies = await page.is_visible(xpath)
            if cookies:
                button = await page.query_selector(xpath)
                if button:
                    await button.evaluate("node => node.click()")
                    await page.wait_for_timeout(1000)

        if cookie_xpath:
            await ScrapModule.save_cookies(page)

        # 1-2 page_reload after cookie
        if page_reload_after_cookies:
            local_page = await ScrapModule.load_page(page, search_url)
            await page.wait_for_timeout(2000)

        # 2. check page is not found
        await page.wait_for_timeout(wait_for_loading)
        not_found = await ScrapModule.check_not_found(local_page, not_found_xpath)

        # reverse not found error for some cases
        if reverse_not_found_result:
            not_found = not not_found

        if not_found:
            log.warning(f"[{shop_name}] has no [{brand_name}] items")
            return []

        # 3. scrap items
        cards_info = []
        page_num: int = 0
        while True:
            if scroll_on:
                await ScrapModule.scroll_down(local_page, max_scroll=20, time_delay=0.5)

            cards = await ScrapModule.load_product_card(
                local_page, product_card_xpath, card_attr
            )

            if not cards:
                log.warning(f"[{shop_name}] has no [{brand_name}] cards items")
                break

            cards_info += [get_item_info(card) for card in cards]

            if not await get_next_page(page, page_num, next_page_xpath):
                break

            page_num += 1

        return cards_info

    @classmethod
    async def scrap_page_logic(
        cls,
        page: Page,
        search_url: str,
        shop_name: str,
        cookie_xpath: str | List[str],
        get_size_info: Callable,
        get_product_id: Callable,
        **kwargs,
    ):
        log = make_logger(f"logs/shop_product_card_page/{shop_name}.log", shop_name)

        # 1. load_page
        await ScrapModule.load_cookies(page)
        local_page = await ScrapModule.load_page(page, search_url)
        assert local_page, log.error(f"[{shop_name}] page load failed")

        # 1-1. deal with cookies
        if isinstance(cookie_xpath, str):
            cookie_xpath = [cookie_xpath]
        for xpath in cookie_xpath:
            cookies = await page.is_visible(xpath)
            if cookies:
                button = await page.query_selector(xpath)
                if button:
                    await button.evaluate("node => node.click()")
                    await page.wait_for_timeout(1000)

        if cookie_xpath:
            await ScrapModule.save_cookies(page)

        size_info = await get_size_info(page)
        product_id = await get_product_id(page)

        assert {*size_info[0].keys()} == {
            "shop_product_size",
            "kor_product_size",
        }, "size_info is not valid"
        return {"size_info": size_info, "product_id": product_id}

    @classmethod
    def save_to_parquet(cls, cards_info: List[Dict]):
        path = ScrapModule.get_current_dir()
        path = path + "data/scrap_list/"

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        file_name = datetime.now().strftime("%y%m%d-%H%M%S")
        cards_info = [ShopProductCardSchema(**card).model_dump() for card in cards_info]
        pd.DataFrame(cards_info).to_parquet(
            path + file_name + "-scrap_list.parquet.gzip", compression="gzip"
        )

    @classmethod
    async def save_cookies(cls, page: Page):
        # Get cookies from the current page
        cookies = await page.context.cookies()

        # Save cookies to a file or database
        # In this example, cookies are saved to a file named 'cookies.json'

        path = "router/dev/shop/components/"
        with open(path + "/cookie/cookies.json", "w") as file:
            file.write(json.dumps(cookies, indent=2, default=str))

    @classmethod
    async def load_cookies(cls, page: Page):
        # Load cookies from a file or database
        # In this example, cookies are loaded from a file named 'cookies.json'

        path = "router/dev/shop/components/"

        with open(path + "/cookie/cookies.json", "r") as file:
            cookies = json.load(file)

        # Set cookies in the current page
        await page.context.add_cookies(cookies)

    @classmethod
    def get_current_dir(cls):
        return os.path.dirname(os.path.abspath(__file__))
