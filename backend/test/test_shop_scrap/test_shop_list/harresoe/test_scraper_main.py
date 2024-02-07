import pytest

from shop_scrap.page.scraper_main import ShopPageScraperFactory

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Fac():
    yield ShopPageScraperFactory(curr_path)


@pytest.mark.anyio
async def test_page_main(Fac: ShopPageScraperFactory):
    target_list = [
        {
            "shop_name": "_18montrose",
            "shop_product_card_id": "12345",
            "product_url": "https://www.18montrose.com/adidas-originals-gazelle-trainers-110270#colcode=11027041",
        },
    ]
    scraper = await Fac.playwright(target_list, 1)
    await scraper.scrap()
