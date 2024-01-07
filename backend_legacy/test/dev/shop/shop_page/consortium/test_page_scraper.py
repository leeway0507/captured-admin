import os
import shutil
import pytest
from components.dev.shop.shop_list.consortium import PwConsortiumPageSubScraper
from components.dev.shop.page import ShopPageData, ShopPageScraper
from components.dev.utils.browser_controller import PwBrowserController

folder_path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/shop/shop_page/"
html_path = os.path.join(folder_path, "consortium")
test_html = f"file://{os.path.join(html_path,'test.html')}"


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def scraper():
    browser = await PwBrowserController.start()
    sub_scraper = PwConsortiumPageSubScraper()
    scraper = ShopPageScraper(1, folder_path, browser, sub_scraper, "consortium")
    yield scraper


@pytest.fixture(scope="module")
async def page_result():
    import json

    with open(os.path.join(html_path, "shop_product_page.json")) as f:
        cards = json.load(f)
        yield cards


@pytest.mark.anyio
async def test_allocate_job(scraper: ShopPageScraper):
    scraper.sub_scraper.allocate_job("12345")
    assert scraper.sub_scraper.job == "12345"


# save temp
@pytest.mark.anyio
async def test_save_temp(scraper: ShopPageScraper, page_result):
    # Given
    os.remove(os.path.join(folder_path, "_temp", "product_card_page.json"))

    await scraper.save_data_to_temp(page_result[1])


def test_set_scrap_status_temp_template(scraper: ShopPageScraper):
    template = scraper.set_scrap_status_temp_template("adidas", "success")

    assert template.model_dump() == {
        "job": "adidas",
        "status": "success",
    }


@pytest.mark.anyio
async def test_save_scrap_status_to_temp(scraper: ShopPageScraper):
    # Given
    os.remove(os.path.join(folder_path, "_temp", "scrap_status.json"))
    template = scraper.set_scrap_status_temp_template("12345", "success")

    # When
    await scraper.save_scrap_status_to_temp(template)

    # Then
    assert os.path.exists(os.path.join(folder_path, "_temp", "scrap_status.json"))


# create report
@pytest.mark.anyio
async def test_create_report_template(scraper: ShopPageScraper):
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
        "job": [{"job": "12345", "status": "success"}],
    }


@pytest.mark.anyio
async def test_create_scrap_report(scraper: ShopPageScraper):
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
def test_generate_shop_list_folder_path(scraper: ShopPageScraper):
    path = scraper._generate_shop_folder_path()
    assert path == html_path


def test_preprocess_data(scraper: ShopPageScraper, page_result):
    preprocessed_data = scraper.preprocess_data(page_result[1])

    assert list(preprocessed_data[0].keys()) == [
        "shop_product_card_id",
        "shop_product_size",
        "kor_product_size",
        "available",
        "updated_at",
        "product_id",
    ]


@pytest.mark.anyio
async def test_scrap_data(scraper: ShopPageScraper):
    scraper.set_scrap_time()
    await scraper.save_scrap_data()

    size_path = os.path.join(
        folder_path, "consortium", f"{scraper.scrap_time}-size.parquet.gzip"
    )
    product_id_path = os.path.join(
        folder_path, "consortium", f"{scraper.scrap_time}-product-id.parquet.gzip"
    )
    assert os.path.exists(os.path.join(size_path))
    assert os.path.exists(os.path.join(product_id_path))

    # clean up
    os.remove(size_path)
    os.remove(product_id_path)
