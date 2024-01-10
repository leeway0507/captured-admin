import pytest

from platform_scrap.list.scraper_main import PlatformListScraperFactory

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Fac():
    yield PlatformListScraperFactory(curr_path)


@pytest.mark.anyio
async def test_scrap(Fac: PlatformListScraperFactory):
    target_list = ["the north face"]
    scraper = await Fac.kream(target_list, 1)
    await scraper.scrap()
