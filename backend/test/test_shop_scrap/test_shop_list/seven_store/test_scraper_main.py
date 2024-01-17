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
async def test_seven_store(Fac: ShopPageScraperFactory):
    target_list = [
        {
            "shop_name": "seven_store",
            "shop_product_card_id": "12345",
            "product_url": "https://www.sevenstore.com/footwear/sneakers/adidas-collegiate-purplecream-whitedark-purple-bermuda-sneaker/",
        },
        # {
        #     "shop_name": "seven_store",
        #     "shop_product_card_id": "67890",
        #     "product_url": "https://www.sevenstore.com/accessories/face-body/aesop-multi-reverence-aromatique-hand-wash-500ml/",
        # },
    ]
    scraper = await Fac.playwright(target_list, 1)
    await scraper.scrap()
