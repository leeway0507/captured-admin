from ....utils.browser_controller import (
    BrowserController,
    PwBrowserController,
)
from typing import Protocol
from env import dev_env
from base64 import b64decode
from playwright.async_api import Page


class PlatformBrowserController(BrowserController, Protocol):
    async def is_login(self, page) -> bool:
        ...

    async def login(self):
        ...


class PlatformBrowserControllerFactory(Protocol):
    def kream(self) -> PlatformBrowserController:
        ...

    def stockX(self) -> PlatformBrowserController:
        ...


class PwPlatformBrowserControllerFactory:
    def kream(self) -> "PwKreamBrowserController":
        return PwKreamBrowserController()

    def stockX(self):
        ...


class SePlatformBrowserControllerFactory:
    def kream(self):
        ...

    def stockX(self):
        ...


class PwKreamBrowserController(PwBrowserController):
    async def login(self):
        page_controller = await self.create_page_controller()
        page = await page_controller.get_page()

        if page.is_closed():
            print("page is closed, reopen new page")
            page = await self.context.new_page()

        await page.goto(
            "https://kream.co.kr/login", wait_until="networkidle", timeout=20000
        )

        if not await self.is_login(page):
            await self._login(page, **self._get_secret())
            await page.wait_for_timeout(1000)

    async def is_login(self, page):
        """로그인 상태를 확인하는 메서드"""
        # top_link
        v = await page.query_selector_all(".top_link")
        status = await v[-1].inner_text()
        if status == "로그아웃":
            return True
        return False

    def _get_secret(self):
        email = dev_env.KREAM_EMAIL
        encoded_password = dev_env.KREAM_PASSWORD

        decoded_password = b64decode(encoded_password).decode("ascii")
        return {"email": email, "password": decoded_password}

    async def _login(self, page: Page, email, password):
        """로그인"""

        await page.fill("input[type='email']", email)
        await page.wait_for_timeout(1000)
        await page.fill("input[type='password']", password)
        await page.keyboard.press("Enter")
        await page.wait_for_load_state(state="networkidle")
        print("save_login_cookies")
