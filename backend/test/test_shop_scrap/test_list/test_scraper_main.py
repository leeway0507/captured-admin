import pytest

from shop_scrap.list.scraper_main import ShopListScraperFactory, PwShopListScraper

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Fac():
    factory = ShopListScraperFactory(curr_path)
    yield factory


# @pytest.mark.anyio
# async def test_consortium(Fac: ShopListScraperFactory):
#     target_list = ["a.p.c. children", "a.p.c."]
#     scraper = await Fac.playwright("consortium", target_list, 2)
#     await scraper.scrap()


@pytest.mark.anyio
async def test_seven_store(Fac: ShopListScraperFactory):
    target_list = ["arcteryx", "asics"]
    scraper = await Fac.playwright("seven_store", target_list, 2)
    await scraper.scrap()
