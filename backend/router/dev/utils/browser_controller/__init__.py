import json
from typing import Protocol, List, Type


import playwright.async_api as pw
import playwright.sync_api as spw
from playwright.async_api import async_playwright
from bs4 import Tag, BeautifulSoup


class PageController(Protocol):
    async def go_to(self, url) -> pw.Response | None:
        ...

    async def deal_with_cookies(self, xpath_list: List[str]) -> None:
        ...

    async def get_page(self) -> pw.Page:
        ...

    async def scroll_down(self, max_scroll: int, time_delay: float) -> None:
        ...

    async def check_not_found(self, xpath: str) -> bool:
        ...

    async def sleep_until(self, time: int):
        ...

    async def reopen_new_page(self):
        ...

    async def extract_html(self, query: str) -> List[Tag] | None:
        ...

    async def close_page(self):
        ...


class BrowserController(Protocol):
    @classmethod
    async def create(cls) -> "BrowserController":
        ...

    async def create_page_controller(self) -> PageController:
        ...

    async def load_cookies(self) -> None:
        ...

    async def close_browser(self) -> None:
        ...


class PwPageController:
    def __init__(self, page: pw.Page):
        self.page = page

    async def go_to(self, url: str):
        return await self.page.goto(url, wait_until="domcontentloaded", timeout=20000)

    async def get_page(self) -> pw.Page:
        return self.page

    async def deal_with_cookies(self, xpath_list: List[str]):
        for xpath in xpath_list:
            cookies = await self.page.is_visible(xpath)
            if cookies:
                button = await self.page.query_selector(xpath)
                if button:
                    await button.evaluate("node => node.click()")
                    await self.page.wait_for_timeout(1000)

        if xpath_list:
            await self.save_cookies()

    async def save_cookies(self):
        # Get cookies from the current page
        cookies = await self.page.context.cookies()

        # Save cookies to a file or database
        # In this example, cookies are saved to a file named 'cookies.json'

        path = "router/dev/shop/components/"
        with open(path + "/cookie/cookies.json", "w") as file:
            file.write(json.dumps(cookies, indent=2, default=str))

    async def scroll_down(self, max_scroll: int = 10, time_delay: float = 500):
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
            await self.page.evaluate("(async () => { window.scrollBy(0, 400); })()")
            await self.page.wait_for_timeout(time_delay)

    async def check_not_found(self, xpath: str) -> bool:
        not_found_page = await self.page.query_selector(xpath)
        if not_found_page:
            return True
        return False

    async def sleep_until(self, time: int):
        await self.page.wait_for_timeout(time)

    async def reopen_new_page(self):
        await self.page.close()
        self.page = await self.page.context.new_page()

    async def extract_html(self, query: str) -> List[Tag] | None:
        value = await self.page.query_selector_all(query)
        return [BeautifulSoup(await row.inner_html(), "html.parser") for row in value]

    async def close_page(self):
        await self.page.close()


class PwBrowserController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.context = None  # Initialize context to None
        return cls._instance

    @classmethod
    async def create(cls) -> "PwBrowserController":
        if cls._instance is None or cls._instance.context is None:
            self = cls()
            self.context = await self.init_pw()
            return self
        else:
            return cls._instance

    async def init_pw(self) -> pw.BrowserContext:
        pw = await async_playwright().start()
        self.browser = await pw.firefox.launch(headless=False, timeout=5000)
        self.context = await self.browser.new_context()
        await self.load_cookies()
        return self.context

    async def create_page_controller(self) -> PwPageController:
        page = await self.context.new_page()
        return PwPageController(page)

    async def load_cookies(self):
        path = "router/dev/shop/components/"
        with open(path + "/cookie/cookies.json", "r") as file:
            cookies = json.loads(file.read())

        await self.context.add_cookies(cookies)
        print("cookies loaded")

    async def close_browser(self):
        if self.browser is not None:
            await self.browser.close()
