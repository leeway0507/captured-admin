import asyncio
import base64
from dotenv import dotenv_values
from .utils import load_page, load_cookies, save_cookies

from playwright.async_api import (
    async_playwright,
    Page,
    Browser,
    TimeoutError as PlaywrightTimeoutError,
)


init_page_error = "init_page가 None입니다. init 메서드를 먼저 실행해주세요."
browser_error = "browser가 None입니다. init 메서드를 먼저 실행해주세요."
login_password_error = "KREAM_PASSWORD가 설정되지 않았습니다. 재확인 바랍니다."


class customPage:
    def __init__(self):
        self.browser = None
        self.context = None
        self.init_page = None

    async def init(self) -> None:
        pw = await async_playwright().start()
        self.browser = await pw.firefox.launch(headless=False, timeout=5000)
        self.context = await self.browser.new_context()
        self.init_page = await self.context.new_page()
        await load_cookies(self.init_page)

    async def close_browser(self):
        assert isinstance(self.browser, Browser), browser_error
        return await self.browser.close()

    async def close_page(self, page):
        return await page.close()

    def get_init_page(self):
        assert isinstance(self.init_page, Page), init_page_error
        return self.init_page

    def get_context(self):
        return self.context


class KreamPage(customPage):
    def __init__(self):
        super().__init__()

    async def is_login(self, page):
        """로그인 상태를 확인하는 메서드"""
        # top_link
        v = await page.query_selector_all(".top_link")
        status = await v[-1].inner_text()
        if status == "로그아웃":
            return True
        return False

    async def login(self):
        assert isinstance(self.init_page, Page), init_page_error

        if self.init_page.is_closed():
            self.init_page = await self.context.new_page()

        login_page = await load_page(self.init_page, "https://kream.co.kr/login")

        if not await self.is_login(login_page):
            return await self._login(login_page, **self._get_secret())

    def _get_secret(self):
        config = dotenv_values(".env.dev")
        email = config.get("KREAM_EMAIL")
        encoded_password = config.get("KREAM_PASSWORD")

        assert encoded_password, login_password_error
        decoded_password = base64.b64decode(encoded_password).decode("ascii")
        return {"email": email, "password": decoded_password}

    async def _login(self, page, email, password):
        """로그인"""

        await page.fill("input[type='email']", email)
        await asyncio.sleep(1)
        await page.fill("input[type='password']", password)
        await page.keyboard.press("Enter")
        await page.wait_for_load_state(state="networkidle")
        await save_cookies(page)
        print("save_login_cookies")