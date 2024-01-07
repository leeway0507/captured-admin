import pytest

from shop_scrap.list.scraper_main import ShopListScraperFactory, PwShopListScraper

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Scraper():
    factory = ShopListScraperFactory(curr_path)
    PwKreamScraper = await factory.consortium()
    PwKreamScraper.late_binding(num_processor=1)
    yield PwKreamScraper


@pytest.mark.anyio
async def test_scrap(Scraper: PwShopListScraper):
    Scraper.target_list = ["a.p.c. children", "a.p.c."]
    await Scraper.scrap()
