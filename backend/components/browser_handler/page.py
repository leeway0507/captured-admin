import json
from typing import Protocol, List, Type
import os
from random import randint

import playwright.async_api as pw
from bs4 import Tag, BeautifulSoup


class PageHandler(Protocol):
    async def go_to(self, url) -> pw.Response | None: ...

    async def handle_cookies(self, query_list: List[str]) -> None: ...

    def get_page(self) -> pw.Page: ...

    async def scroll_down(
        self, max_scroll: int, time_delay: int, step_size: int
    ) -> None: ...

    async def check_curr_page_is_not_found_page(self, selector: str) -> bool: ...

    async def sleep_until(self, time: int): ...

    async def extract_html(self, query: str) -> List[Tag] | None: ...

    async def close_page(self): ...


class PwPageHandler(pw.Page):
    def __init__(self, page: pw.Page):
        self.page = page

    async def go_to(self, url: str):
        return await self.page.goto(url, wait_until="domcontentloaded", timeout=20000)

    async def handle_cookies(self, query_list: List[str]):
        for xpath in query_list:
            cookies = await self.page.is_visible(xpath)
            if cookies:
                button = await self.page.query_selector(xpath)
                if button:
                    await button.evaluate("node => node.click()")
                    await self.page.wait_for_timeout(randint(100, 2000))

        if query_list:
            await self.save_cookies()

    def get_page(self) -> pw.Page:
        return self.page

    async def save_cookies(self):
        # Get cookies from the current page
        cookies = await self.page.context.cookies()

        # Save cookies to a file or database
        # In this example, cookies are saved to a file named 'cookies.json'
        curr_path = __file__.rsplit("/", 1)[0]
        path = os.path.join(curr_path, "cookie", "cookies.json")
        with open(path, "w") as file:
            file.write(json.dumps(cookies, indent=2, default=str))

    async def scroll_down(
        self, max_scroll: int = 10, time_delay: int = 1000, step_size: int = 1000
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
            await self.page.evaluate(
                "(async () => { window.scrollBy(0, step_size); })()".replace(
                    "step_size", str(randint(100, step_size))
                )
            )
            await self.page.wait_for_timeout(randint(100, time_delay))

    async def check_curr_page_is_not_found_page(self, selector: str) -> bool:
        not_found_page = await self.page.query_selector(selector)
        if not_found_page:
            return True
        return False

    async def sleep_until(self, time: int):
        await self.page.wait_for_timeout(time)

    async def extract_html(self, query: str) -> List[Tag] | List:
        value = await self.page.query_selector_all(query)
        return [BeautifulSoup(await row.inner_html(), "html.parser") for row in value]

    async def close_page(self):
        await self.page.close()
