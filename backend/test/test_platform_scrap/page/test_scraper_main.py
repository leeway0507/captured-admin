import pytest

from platform_scrap.page.scraper_main import (
    PlatformPageScraper,
    PlatformPageScraperFactory,
)

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Scraper():
    factory = PlatformPageScraperFactory(curr_path)
    PwKreamScraper = await factory.pw_kream()
    PwKreamScraper.late_binding(num_processor=1)
    yield PwKreamScraper


@pytest.mark.anyio
async def test_scrap(Scraper: PlatformPageScraper):
    Scraper.target_list = ["74749"]
    await Scraper.scrap()
