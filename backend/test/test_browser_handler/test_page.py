import pytest

from components.browser_handler import PwPageHandler
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

test_url = "https://www.naver.com/"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def scraper():
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(headless=False, timeout=5000)
    page = await browser.new_page()
    yield PwPageHandler(page)


@pytest.mark.anyio
async def test_go_to_url(scraper: PwPageHandler):
    await scraper.go_to(test_url)

    assert scraper.page.url == test_url


@pytest.mark.anyio
async def test_get_page(scraper: PwPageHandler):
    page = scraper.get_page()

    assert isinstance(page, Page)


@pytest.mark.anyio
async def test_scroll_down(scraper: PwPageHandler):
    await scraper.scroll_down(max_scroll=1)


@pytest.mark.anyio
async def test_check_not_found_page(scraper: PwPageHandler):
    not_found_page_feature = '//*[@id="shopping"]'
    is_not_found = await scraper.check_curr_page_is_not_found_page(
        not_found_page_feature
    )

    assert is_not_found == True


@pytest.mark.anyio
async def test_extract_html(scraper: PwPageHandler):
    soup = await scraper.extract_html('//*[@id="newsstand"]/div[1]')

    assert isinstance(soup[0], BeautifulSoup)
