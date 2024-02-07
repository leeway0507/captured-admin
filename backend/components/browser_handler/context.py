import json
from abc import ABC, abstractmethod
import os
import base64
from random import randint

import playwright.async_api as pw
from playwright.async_api import async_playwright

from components.env import dev_env
from .page import PageHandler, PwPageHandler

from stem import Signal
from stem.control import Controller
from components.subprocess import check_port_open

user_agent_string = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


class ContextHandler(ABC):
    @classmethod
    async def start(cls): ...

    @abstractmethod
    async def create_page(self) -> PageHandler: ...

    @abstractmethod
    async def load_cookies(self) -> None: ...

    @abstractmethod
    async def close_context(self) -> None: ...


class PlatformContextHandler(ContextHandler):
    @abstractmethod
    async def login(self): ...


class PwContextHandler(ContextHandler):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.context = None  # Initialize context to None

        cls.allow_cookie = False
        cls.allow_proxy = False
        return cls._instance

    @classmethod
    async def start(cls, allow_proxy: bool = False, allow_cookie: bool = False):
        if cls._instance is None or cls._instance.context is None:
            self = cls()
            self.context = await self._init_pw(allow_proxy, allow_cookie)
            return self
        else:
            return cls._instance

    @classmethod
    async def re_start(cls, allow_proxy: bool = False, allow_cookie: bool = False):
        self = cls()
        self.context = await self._init_pw(allow_proxy, allow_cookie)
        return self

    async def _init_pw(
        self, allow_proxy: bool, allow_cookie: bool
    ) -> pw.BrowserContext:
        config = {"headless": False, "timeout": 5000}
        # tor proxy 제거
        # if allow_proxy:
        #     proxy_exist = self.get_new_ip()
        #     if proxy_exist:
        #         config.update({"proxy": {"server": "socks5://localhost:9050"}})
        #     else:
        #         raise (ImportError("9051 포트가 꺼져있습니다. Proxy 사용을 위해선 docker tor를 실행하세요."))

        pw = await async_playwright().start()
        self.browser = await pw.chromium.launch(**config)
        self.context = await self.browser.new_context(
            user_agent=user_agent_string[randint(0, len(user_agent_string) - 1)],
            viewport={"width": 1280, "height": 1440},
        )
        # header 내 webdriver 제거
        await self.context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        if allow_cookie == True:
            await self.load_cookies()

        print("----- 브라우저 옵션 -----")
        print(f"allow_proxy : {allow_proxy}")
        print(f"allow_cookie : {allow_cookie}")
        return self.context

    def get_new_ip(self):
        if check_port_open(9051):
            with Controller.from_port(port=9051) as controller:  # type:ignore
                controller.authenticate()
                controller.signal(Signal.NEWNYM)  # type:ignore
            return True
        else:
            return False

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
