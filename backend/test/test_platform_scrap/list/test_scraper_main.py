import pytest

from platform_scrap.list.scraper_main import (
    PlatformListScraperFactory,
    PwKreamListScraper,
)

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Scraper():
    factory = PlatformListScraperFactory(curr_path)
    PwKreamScraper = await factory.pw_kream()
    PwKreamScraper.late_binding(num_processor=1)
    yield PwKreamScraper


@pytest.mark.anyio
async def test_scrap(Scraper: PwKreamListScraper):
    Scraper.target_list = ["the north face"]
    await Scraper.scrap()
