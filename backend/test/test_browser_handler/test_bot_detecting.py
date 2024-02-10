import pytest

from components.browser_handler import PwContextHandler, PwPageHandler
from time import time
import os

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def scraper():
    scraper = await PwContextHandler.start()
    yield scraper


@pytest.mark.anyio
async def test_page_web_detecting(scraper: PwContextHandler):
    page = await scraper.create_page()
    await page.page.goto("https://bot.sannysoft.com/")
    await page.page.screenshot(path=os.path.join(curr_path, "capture.png"))
    await page.page.wait_for_timeout(1000000)

    assert isinstance(page, PwPageHandler)
