import json
from abc import ABC, abstractmethod
import os
import base64

import playwright.async_api as pw
from playwright.async_api import async_playwright

from components.env import dev_env
from .page import PageHandler, PwPageHandler


class ContextHandler(ABC):
    @classmethod
    async def start(cls):
        ...

    @abstractmethod
    async def create_page(self) -> PageHandler:
        ...

    @abstractmethod
    async def load_cookies(self) -> None:
        ...

    @abstractmethod
    async def close_context(self) -> None:
        ...


class PlatformContextHandler(ContextHandler):
    @abstractmethod
    async def login(self):
        ...


class PwContextHandler(ContextHandler):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.context = None  # Initialize context to None
        return cls._instance

    @classmethod
    async def start(cls):
        if cls._instance is None or cls._instance.context is None:
            self = cls()
            self.context = await self._init_pw()
            return self
        else:
            return cls._instance

    async def _init_pw(self) -> pw.BrowserContext:
        pw = await async_playwright().start()
        self.browser = await pw.firefox.launch(headless=False, timeout=5000)
        self.context = await self.browser.new_context()
        await self.load_cookies()
        return self.context

    async def create_page(self) -> "PwPageHandler":
        page = await self.context.new_page()
        return PwPageHandler(page)

    async def load_cookies(self):
        curr_path = __file__.rsplit("/", 1)[0]
        path = os.path.join(curr_path, "cookie", "cookies.json")
        with open(path, "r") as file:
            cookies = json.loads(file.read())

        await self.context.add_cookies(cookies)
        print("cookies loaded")

    async def close_context(self):
        if self.browser is not None:
            await self.browser.close()


class PwKreamContextHanlder(PwContextHandler, PlatformContextHandler):
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
        decoded_password = base64.b64decode(encoded_password).decode("ascii")

        return {"email": email, "password": decoded_password}

    async def _login(self, email, password):
        """로그인"""

        await self.login_page.fill("input[type='email']", email)
        await self.login_page.wait_for_timeout(1000)
        await self.login_page.fill("input[type='password']", password)
        await self.login_page.keyboard.press("Enter")
        await self.login_page.wait_for_load_state(state="networkidle")
        print("save_login_cookies")
