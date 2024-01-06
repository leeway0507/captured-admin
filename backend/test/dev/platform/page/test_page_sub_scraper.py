from typing import AsyncGenerator, List
import os
import pytest
from datetime import date, timedelta

from playwright.async_api import async_playwright
from bs4 import Tag, BeautifulSoup

from components.dev.utils.browser_controller import PwPageController
from components.dev.platform.page.sub_scraper import PwKreamPageSubScraper
from components.dev.platform.platform_browser_controller import PwKreamBrowserController


path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/page"
html_path = os.path.join(path, "html")
test_min_volume = 50
test_min_wish = 50
test_brand_name = "Adidas"

html_path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/page/html/"
product_detail_path = f"file://{os.path.join(html_path,'product_detail.html')}"
buy_and_sell_path = f"file://{os.path.join(html_path,'buy.html')}"
trading_volume_path = f"file://{os.path.join(html_path,'trading_volume.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def sub_scraper() -> AsyncGenerator:
    pw_browser = await PwKreamBrowserController().start()
    await pw_browser.login()
    pw_page = await pw_browser.create_page()
    scraper = PwKreamPageSubScraper()
    scraper.late_binding(pw_page)
    scraper.allocate_job(80591)
    yield scraper


@pytest.mark.anyio
async def test_go_to_card_page(sub_scraper: PwKreamPageSubScraper):
    # When

    await sub_scraper.go_to_card_page()

    # Then
    assert sub_scraper.page.url == sub_scraper.get_url()


@pytest.mark.anyio
async def test_scrap_product_detail(sub_scraper: PwKreamPageSubScraper):
    # When
    await sub_scraper.go_to_card_page()
    result = await sub_scraper.scrap_product_detail()

    assert result[0] == "success"


@pytest.mark.anyio
async def test_scrap_buy_and_sell(sub_scraper: PwKreamPageSubScraper):
    # When
    await sub_scraper.go_to_card_page()
    result = await sub_scraper.scrap_buy_and_sell()

    assert result[0] == "success"


@pytest.mark.anyio
async def test_trading_volume(sub_scraper: PwKreamPageSubScraper):
    # When
    await sub_scraper.go_to_card_page()
    result = await sub_scraper.scrap_trading_volume(limit_days=200)

    from pprint import pprint

    pprint(result)

    assert result[0] == "success"


@pytest.mark.anyio
async def test_execute(sub_scraper: PwKreamPageSubScraper):
    # When

    result = await sub_scraper.execute()

    assert type(result) == tuple
