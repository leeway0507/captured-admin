import os
import shutil
import pytest
from components.dev.shop.shop_list.consortium import PwConsortiumListSubScraper
from components.dev.shop.list import ShopListScraper, ListScrapData
from components.dev.utils.browser_controller import PwBrowserController

folder_path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/shop/shop_list/"
html_path = os.path.join(folder_path, "consortium")
test_html = f"file://{os.path.join(html_path,'test.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def scraper():
    browser = await PwBrowserController.start()
    sub_scraper = PwConsortiumListSubScraper()
    scraper = ShopListScraper(1, folder_path, browser, sub_scraper, "consortium")
    yield scraper


@pytest.fixture(scope="module")
async def list_result():
    import json

    with open(os.path.join(html_path, "shop_product_list.json")) as f:
        cards = json.load(f)
        yield ["success", cards]


# save temp
@pytest.mark.anyio
async def test_save_temp(scraper: ShopListScraper, list_result):
    await scraper.save_data_to_temp(list_result[1])


def test_set_scrap_status_temp_template(scraper: ShopListScraper):
    template = scraper.set_scrap_status_temp_template("adidas", "success")

    assert template.model_dump() == {
        "job": "adidas",
        "status": "success",
    }


@pytest.mark.anyio
async def test_save_scrap_status_to_temp(scraper: ShopListScraper):
    # Given
    os.remove(os.path.join(folder_path, "_temp", "scrap_status.json"))
    template = scraper.set_scrap_status_temp_template("adidas", "success")

    # When
    await scraper.save_scrap_status_to_temp(template)

    # Then
    assert os.path.exists(os.path.join(folder_path, "_temp", "scrap_status.json"))


# create report
@pytest.mark.anyio
async def test_create_report_template(scraper: ShopListScraper):
    # Given
    scraper.set_scrap_time()
    temp_scrap_status = await scraper.load_temp_scrap_data()

    # When
    report_template = scraper.create_report_template(temp_scrap_status)

    assert report_template.model_dump() == {
        "scrap_time": scraper.scrap_time,
        "num_of_plan": 1,
        "num_processor": 1,
        "db_update": False,
        "job": [{"job": "adidas", "status": "success"}],
    }


@pytest.mark.anyio
async def test_create_scrap_report(scraper: ShopListScraper):
    # Given
    shutil.rmtree(os.path.join(folder_path, "_report"))
    scraper.set_scrap_time()

    # When
    await scraper.create_scrap_report()

    # Then
    assert os.path.exists(
        os.path.join(folder_path, "_report", f"{scraper.scrap_time}.json")
    )


# save data


def test_generate_shop_list_folder_path(scraper: ShopListScraper):
    path = scraper._generate_shop_folder_path()
    assert path == html_path


def test_preprocess_data(scraper: ShopListScraper, list_result):
    preprocessed_data = scraper.preprocess_data(list_result[1])

    assert list(preprocessed_data[0].keys()) == [
        "shop_product_card_id",
        "shop_product_name",
        "shop_product_img_url",
        "product_url",
        "shop_name",
        "brand_name",
        "product_id",
        "kor_price",
        "us_price",
        "original_price_currency",
        "original_price",
        "sold_out",
        "candidate",
        "coupon",
        "updated_at",
    ]


@pytest.mark.anyio
async def test_scrap_data(scraper: ShopListScraper):
    scraper.set_scrap_time()

    await scraper.save_scrap_data()

    assert os.path.exists(
        os.path.join(folder_path, "consortium", f"{scraper.scrap_time}.parquet.gzip")
    )
