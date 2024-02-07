import pytest

from shop_scrap.page.scraper_main import ShopPageScraperFactory, PwShopPageScraper

curr_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Fac():
    yield ShopPageScraperFactory(curr_path)


@pytest.mark.anyio
async def test_scrap(Fac: ShopPageScraperFactory):
    target_list = [
        {
            "shop_name": "harresoe",
            "shop_product_card_id": "12345",
            "product_url": "https://harresoe.com/products/xt-6-black-falcon-cow-hide-l47293800",
        },
        {
            "shop_name": "harresoe",
            "shop_product_card_id": "12345",
            "product_url": "https://harresoe.com/products/xt-6-black-falcon-cow-hide-l47293800",
        },
        {
            "shop_name": "harresoe",
            "shop_product_card_id": "12345",
            "product_url": "https://harresoe.com/products/xt-6-black-falcon-cow-hide-l47293800",
        },
        {
            "shop_name": "harresoe",
            "shop_product_card_id": "12345",
            "product_url": "https://harresoe.com/products/xt-6-black-falcon-cow-hide-l47293800",
        },
    ]
    scraper = await Fac.playwright(target_list, 1)
    await scraper.scrap()
