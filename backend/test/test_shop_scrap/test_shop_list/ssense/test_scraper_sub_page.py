import os
import pytest
from shop_scrap.shop_list.ssense import PwSsensePageSubScraper
from playwright.async_api import async_playwright
from components.browser_handler import PwPageHandler
from playwright_stealth import stealth_async

curr_path = __file__.rsplit("/", 1)[0]


def html(name: str):
    return f"file://{os.path.join(curr_path,name+'.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def sub_scraper():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        executable_path="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        timeout=5000,
        headless=False,
    )
    page = await browser.new_page()
    await stealth_async(page)
    pw_page = PwPageHandler(page)
    sub_scraper = PwSsensePageSubScraper()
    sub_scraper.late_binding(pw_page)
    url = "https://www.ssense.com/en-kr/women/product/vivienne-westwood/navy-alex-cardigan/14613401"
    job = {"shop_product_card_id": "1234", "product_url": url}
    sub_scraper.allocate_job(job)
    yield sub_scraper


@pytest.mark.anyio
async def test_execute(sub_scraper: PwSsensePageSubScraper):
    result, data = await sub_scraper.execute()

    print(result)
    print(data)
