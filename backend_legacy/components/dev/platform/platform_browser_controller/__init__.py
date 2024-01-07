from ...utils.browser_controller import (
    BrowserController,
    PwBrowserController,
)
from typing import Protocol
from env import dev_env
from base64 import b64decode
from playwright.async_api import Page


class PlatformBrowserController(BrowserController, Protocol):
    async def is_login(self) -> bool:
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
    _instance = None

    @classmethod
    async def start(cls) -> "PwKreamBrowserController":
        if cls._instance is None or cls._instance.context is None:
            self = cls()
            self.context = await self._init_pw()
            return self
        else:
            return cls._instance

    async def login(self):
        page_controller = await self.create_page()
        self.login_page = page_controller.get_page()

        if self.login_page.is_closed():
            print("page is closed, reopen new page")
            page = await self.context.new_page()

        await self.login_page.goto(
            "https://kream.co.kr/login", wait_until="networkidle", timeout=20000
        )
        if not await self.is_login():
            await self._login(**self._get_secret())

        await self.login_page.wait_for_timeout(1000)

    async def is_login(self):
        """로그인 상태를 확인하는 메서드"""
        # top_link
        v = await self.login_page.query_selector_all(".top_link")
        status = await v[-1].inner_text()
        print(f"login status: {status}")
        if status == "로그아웃":
            return True
        return False

    def _get_secret(self):
        email = dev_env.KREAM_EMAIL
        encoded_password = dev_env.KREAM_PASSWORD

        decoded_password = b64decode(encoded_password).decode("ascii")
        return {"email": email, "password": decoded_password}

    async def _login(self, email, password):
        """로그인"""

        await self.login_page.fill("input[type='email']", email)
        await self.login_page.wait_for_timeout(1000)
        await self.login_page.fill("input[type='password']", password)
        await self.login_page.keyboard.press("Enter")
        await self.login_page.wait_for_load_state(state="networkidle")
        print("save_login_cookies")
