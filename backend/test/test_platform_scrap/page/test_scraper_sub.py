from typing import AsyncGenerator, List
import os
import pytest
from datetime import date, timedelta
from components.browser_handler import PwKreamContextHanlder
from platform_scrap.page.scraper_sub import PwKreamPageSubScraper


curr_path = __file__.rsplit("/", 1)[0]
html_path = os.path.join(curr_path, "html")

test_brand_name = "Adidas"

product_detail_path = f"file://{os.path.join(html_path,'product_detail.html')}"
buy_and_sell_path = f"file://{os.path.join(html_path,'buy.html')}"
trading_volume_path = f"file://{os.path.join(html_path,'trading_volume.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def sub_scraper() -> AsyncGenerator:
    pw_browser = await PwKreamContextHanlder().start()
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
    result = await sub_scraper.scrap_trading_volume()

    from pprint import pprint

    pprint(result)

    assert result[0] in ["success", "success:no_trading_volume"]


@pytest.mark.anyio
async def test_execute(sub_scraper: PwKreamPageSubScraper):
    # When

    result = await sub_scraper.execute()
    assert type(result) == tuple
