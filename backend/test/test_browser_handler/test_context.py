import pytest

from components.browser_handler import PwContextHandler, PwPageHandler
from time import time


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def scraper():
    scraper = await PwContextHandler.start()
    yield scraper


@pytest.mark.anyio
async def test_create_page(scraper: PwContextHandler):
    page = await scraper.create_page()

    assert isinstance(page, PwPageHandler)


@pytest.mark.anyio
async def test_PwContextHandler_is_singleton():
    scraper = await PwContextHandler.start()
    scraper_other = await PwContextHandler.start()
    assert scraper is scraper_other

    scraper_proxy = await PwContextHandler.re_start()
    assert scraper is scraper_proxy

    scraper_cookie = await PwContextHandler.re_start(allow_cookie=True)
    assert scraper is scraper_cookie


@pytest.fixture(scope="module")
async def scraper_cookie_allow():
    scraper = await PwContextHandler.start(allow_cookie=True)
    yield scraper


@pytest.mark.anyio
async def test_create_page_cookie_allow(scraper_cookie_allow: PwContextHandler):
    page = await scraper_cookie_allow.create_page()

    assert isinstance(page, PwPageHandler)


@pytest.fixture(scope="module")
async def scraper_proxy_allow():
    scraper = await PwContextHandler.re_start()
    yield scraper


@pytest.mark.anyio
async def test_create_page_scraper_proxy_allow(scraper_proxy_allow: PwContextHandler):
    page = await scraper_proxy_allow.create_page()
    await page.go_to("https://check.torproject.org/")
    assert isinstance(page, PwPageHandler)
