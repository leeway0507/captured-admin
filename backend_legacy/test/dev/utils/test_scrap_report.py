import os
import pytest

from components.dev.utils.file_manager import (
    ScrapReport,
    ScrapTempFile,
    ScrapReportDataBase,
)


test_scrap_report_data = ScrapReportDataBase(
    scrap_time="20231231-123456",
    num_of_plan=1,
    num_processor=1,
    job=[
        {
            "shop_name": "consortium",
            "brand_name": "ganni",
            "status": "success : 137 개",
        }
    ],
    db_update=False,
)

test_report_path = (
    "/Users/yangwoolee/repo/captured/admin/backend/test/dev/utils/_report"
)


test_report_file_name = "20231231-123456"
test_report_file_path = os.path.join(test_report_path, test_report_file_name + ".json")


### Test Functions ###


@pytest.fixture
def scrap_report():
    yield ScrapReport(test_report_path)


### start Test ###
def test_ScrapReport_is_singleton(scrap_report: ScrapReport):
    # Given
    scrap_report_other = ScrapReport(test_report_path)

    # Then
    assert scrap_report is scrap_report_other


def test_report_file_path_error_when_None(scrap_report: ScrapReport):
    """"""

    # Given
    # report_file_name is None

    # When & Then
    with pytest.raises(ValueError):
        scrap_report.get_report_file_path()


def test_set_report_file_path(scrap_report: ScrapReport):
    # Given
    scrap_report.set_report_name(test_report_file_name)

    # When
    report_file_path = scrap_report.get_report_file_path()

    # Then
    assert report_file_path == test_report_file_path


@pytest.mark.asyncio
async def test_create_report(scrap_report: ScrapReport):
    # When
    await scrap_report.create_report_with_scrap_time_as_file_name(
        report_data=test_scrap_report_data
    )

    # Then
    report_file_path = os.path.join(test_report_path, "20231231-123456.json")
    assert os.path.exists(report_file_path)


def test_load_report(scrap_report: ScrapReport):
    # Given
    scrap_report.set_report_name(test_report_file_name)
    # When
    report = scrap_report.load_report()

    assert report == test_scrap_report_data.model_dump()


def test_update_report(scrap_report: ScrapReport):
    # Given
    scrap_report.set_report_name(test_report_file_name)

    # When
    scrap_report.update_report({"db_update": True})

    # Then
    report = scrap_report.load_report()
    assert report["db_update"] == True
    scrap_report.update_report({"db_update": False})


@pytest.mark.asyncio
async def test_delete_report(scrap_report: ScrapReport):
    # Given
    scrap_report.set_report_name(test_report_file_name)

    # When
    scrap_report.delete_report()

    # Then
    assert not os.path.exists(scrap_report.get_report_file_path())

    await scrap_report.create_report_with_scrap_time_as_file_name(
        report_data=test_scrap_report_data
    )


def test_get_report_list(scrap_report: ScrapReport):
    # When
    report_list = scrap_report.get_report_list()

    # Then
    assert report_list == [test_report_file_name]
