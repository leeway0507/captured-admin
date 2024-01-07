import os
import pytest
from shop_scrap.page.main import ShopPageMain

current_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def ShopPage():
    yield ShopPageMain(current_path)


@pytest.mark.anyio
async def test_PlatformPage(ShopPage: ShopPageMain):
    target_list = [
        {
            "shop_product_card_id": "12345",
            "product_url": "https://www.consortium.co.uk/adidas-originals-x-fucking-awesome-samba-fa-core-black-footwear-white-gold-metallic-id7339.html",
        },
        {
            "shop_product_card_id": "67890",
            "product_url": "https://www.consortium.co.uk/adidas-originals-gazelle-indoor-bliss-pink-core-black-collegiate-purple-ie7002.html",
        },
    ]
    await ShopPage.init_main_scraper(
        "consortium", target_list=target_list, num_processor=2
    )
    await ShopPage.execute()
