import pytest

from shop_scrap.page.scraper_main import ShopPageScraperFactory, PwShopPageScraper

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Scraper():
    factory = ShopPageScraperFactory(curr_path)
    PwKreamScraper = await factory.consortium()
    PwKreamScraper.late_binding(num_processor=1)
    yield PwKreamScraper


@pytest.mark.anyio
async def test_scrap(Scraper: PwShopPageScraper):
    Scraper.target_list = [
        {
            "shop_product_card_id": "12345",
            "product_url": "https://www.consortium.co.uk/adidas-originals-x-fucking-awesome-samba-fa-core-black-footwear-white-gold-metallic-id7339.html",
        },
        {
            "shop_product_card_id": "67890",
            "product_url": "https://www.consortium.co.uk/adidas-originals-gazelle-indoor-bliss-pink-core-black-collegiate-purple-ie7002.html",
        },
    ]
    await Scraper.scrap()
