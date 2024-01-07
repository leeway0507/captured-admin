import os
import pytest

from platform_scrap.list.report import PlatformListReport
from test.utils import remove_test_folder

current_path = __file__.rsplit("/", 1)[0]

report_path = os.path.join(current_path, "_report")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def Report():
    yield PlatformListReport(current_path)


@pytest.mark.anyio
async def test_load_scrap_config(Report: PlatformListReport):
    temp_file = await Report.load_scrap_config()
    result = set(temp_file.keys())
    assert result == {
        "min_wish",
        "scrap_time",
        "path",
        "brand_name",
        "num_processor",
        "min_volume",
        "num_of_plan",
        "platform",
    }


@pytest.mark.anyio
async def test_load_scrap_status(Report: PlatformListReport):
    temp_file = await Report.load_scrap_status()

    result = set(temp_file[0].keys())

    assert result == {"job", "status"}


@pytest.mark.anyio
async def test_create_report_template(Report: PlatformListReport):
    report = await Report.create_report_template()

    result = set(report.model_dump().keys())
    assert result == {
        "scrap_time",
        "brand_name",
        "db_update",
        "job",
        "platform_type",
        "num_processor",
        "num_of_plan",
    }


@pytest.mark.anyio
async def test_save_report_template(Report: PlatformListReport):
    # Given
    remove_test_folder(report_path)

    # When
    await Report.save_report()

    # Then
    assert os.path.exists(report_path)
