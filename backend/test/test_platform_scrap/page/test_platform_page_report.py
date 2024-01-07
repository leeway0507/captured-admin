import os
import pytest

from platform_scrap.page.report import PlatformPageReport
from test.utils import remove_test_folder

current_path = __file__.rsplit("/", 1)[0]

report_path = os.path.join(current_path, "_report")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def Report():
    yield PlatformPageReport(current_path)


@pytest.mark.anyio
async def test_load_scrap_config(Report: PlatformPageReport):
    temp_file = await Report.load_scrap_config()
    result = set(temp_file.keys())
    assert result == {
        "scrap_time",
        "path",
        "brand_name",
        "num_processor",
        "num_of_plan",
        "platform",
    }


@pytest.mark.anyio
async def test_load_scrap_status(Report: PlatformPageReport):
    temp_file = await Report.load_scrap_status()

    result = set(temp_file[0].keys())

    assert result == {"job", "status"}


@pytest.mark.anyio
async def test_create_report_template(Report: PlatformPageReport):
    report = await Report.create_report_template()

    result = set(report.model_dump().keys())
    assert result == {
        "scrap_time",
        "num_of_plan",
        "num_processor",
        "db_update",
        "job",
        "product_detail",
        "trading_volume",
        "buy_and_sell",
        "platform_type",
    }


@pytest.mark.anyio
async def test_save_report_template(Report: PlatformPageReport):
    # Given
    remove_test_folder(report_path)

    # When
    await Report.save_report()

    # Then
    assert os.path.exists(report_path)
