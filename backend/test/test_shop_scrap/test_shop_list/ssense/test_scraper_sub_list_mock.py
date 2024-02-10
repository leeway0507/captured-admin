import os
import pytest
from shop_scrap.shop_list.ssense import PwSsenseListSubScraper
from playwright.async_api import async_playwright
from components.browser_handler import PwPageHandler
from random import randint

curr_path = __file__.rsplit("/", 1)[0]


def html(name: str):
    return f"file://{os.path.join(curr_path,name+'.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


async def route_intercept(route):
    if route.request.resource_type != "document":
        await route.abort()
    else:
        await route.continue_()


@pytest.fixture(scope="module")
async def sub_scraper_mock():
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(timeout=5000, headless=True)
    page = await browser.new_page()
    await page.route(url="**/*", handler=route_intercept)
    pw_page = PwPageHandler(page)
    sub_scraper = PwSsenseListSubScraper()
    sub_scraper.late_binding(pw_page, "ssense")
    sub_scraper.allocate_job("mock")
    await sub_scraper.page_handler.go_to(html("list"))
    yield sub_scraper


@pytest.mark.anyio
async def test_extract_card_html(sub_scraper_mock: PwSsenseListSubScraper):
    # When
    # await sub_scraper.page_handler.go_to(html("seven_store"))
    sub_scraper_mock._test_extract()
    raw_html = await sub_scraper_mock.extract_card_html()

    print(raw_html[0])

    assert len(raw_html) == 120

    url = sub_scraper_mock.has_next_page_url()

    print("url")
    print(url)

    assert isinstance(url, str)


@pytest.mark.anyio
async def test_extract(sub_scraper_mock: PwSsenseListSubScraper):

    sub_scraper_mock.allocate_job("adidas originals")
    url = "https://www.ssense.com/en-us/women/designers/adidas-originals"
    await sub_scraper_mock._extract(url)

    with open(os.path.join(curr_path, "test_extract.txt"), "w") as f:
        f.write(sub_scraper_mock.soup.text)
    assert len(sub_scraper_mock.soup.text[:120]) == 120


@pytest.mark.anyio
async def test_extract_info(sub_scraper_mock: PwSsenseListSubScraper):
    # When
    sub_scraper_mock.allocate_job("mock")
    sub_scraper_mock._test_extract()
    card_list = await sub_scraper_mock.extract_card_html()

    if not card_list:
        raise (ValueError("No None"))
    card_info_list = sub_scraper_mock.extract_info(card_list[0])

    x = [sub_scraper_mock.extract_info(c) for c in card_list]
    print("변환 개수", len(x))
    print(x[randint(0, len(x))])
    assert isinstance(card_info_list, dict)
