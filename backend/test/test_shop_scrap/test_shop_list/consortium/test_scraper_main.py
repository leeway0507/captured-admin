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
async def test_consortium(Fac: ShopPageScraperFactory):
    target_list = [
        {
            # 품절 아이템
            "shop_name": "consortium",
            "shop_product_card_id": "12345",
            "product_url": "https://www.consortium.co.uk/adidas-originals-tobacco-pantone-mesa-gum-gy7396.html",
        },
        {
            "shop_name": "consortium",
            "shop_product_card_id": "67890",
            "product_url": "https://www.consortium.co.uk/adidas-originals-gazelle-indoor-bliss-pink-core-black-collegiate-purple-ie7002.html",
        },
    ]
    scraper = await Fac.playwright(target_list, 1)
    await scraper.scrap()
