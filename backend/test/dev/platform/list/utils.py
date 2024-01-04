from playwright.sync_api import Page, sync_playwright
from base64 import b64decode
from env import dev_env
from components.dev.utils.browser_controller import PwPageController


class KreamLogin:
    def __init__(self, PageControllwer: PwPageController):
        self.page = PageControllwer.page

    async def login(self):
        await self.page.goto(
            "https://kream.co.kr/login", wait_until="networkidle", timeout=20000
        )

        if not await self.is_login():
            await self._login(**self._get_secret())

        await self.page.wait_for_timeout(1000)

    async def is_login(self):
        """로그인 상태를 확인하는 메서드"""
        # top_link
        v = await self.page.query_selector_all(".top_link")
        status = await v[-1].inner_text()
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

        await self.page.fill("input[type='email']", email)
        await self.page.wait_for_timeout(1000)
        await self.page.fill("input[type='password']", password)
        await self.page.keyboard.press("Enter")
        await self.page.wait_for_load_state(state="networkidle")
        print("login Success!!")
        print("save_login_cookies")
