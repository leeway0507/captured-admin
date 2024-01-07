import os
import pytest

from shop_scrap.page.report import ShopPageReport
from test.utils import remove_test_folder

current_path = __file__.rsplit("/", 1)[0]

report_path = os.path.join(current_path, "_report")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def Report():
    yield ShopPageReport(current_path)


@pytest.mark.anyio
async def test_load_scrap_config(Report: ShopPageReport):
    temp_file = await Report.load_scrap_config()
    result = set(temp_file.keys())
    assert result == {
        "scrap_time",
        "path",
        "num_processor",
        "num_of_plan",
        "shop_name",
    }


@pytest.mark.anyio
async def test_load_scrap_status(Report: ShopPageReport):
    temp_file = await Report.load_scrap_status()

    result = set(temp_file[0].keys())

    assert result == {"job", "status"}


@pytest.mark.anyio
async def test_create_report_template(Report: ShopPageReport):
    report = await Report.create_report_template()

    result = set(report.model_dump().keys())
    assert result == {
        "scrap_time",
        "db_update",
        "job",
        "shop_name",
        "num_processor",
        "num_of_plan",
    }


@pytest.mark.anyio
async def test_save_report_template(Report: ShopPageReport):
    # Given
    remove_test_folder(report_path)

    # When
    await Report.save_report()

    # Then
    assert os.path.exists(report_path)
