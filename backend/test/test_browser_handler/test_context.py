import pytest

from components.browser_handler import PwContextHandler, PwPageHandler


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def scraper():
    scraper = await PwContextHandler.start()
    yield scraper


@pytest.mark.anyio
async def test_PwContextHandler_is_singleton(scraper: PwContextHandler):
    scraper_other = await PwContextHandler.start()

    assert scraper is scraper_other


@pytest.mark.anyio
async def test_create_page(scraper: PwContextHandler):
    page = await scraper.create_page()

    assert isinstance(page, PwPageHandler)
