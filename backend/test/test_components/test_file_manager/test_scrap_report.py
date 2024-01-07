import os
import pytest

from components.file_manager import (
    ScrapReport,
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

test_current_path = __file__.rsplit("/", 1)[0]
test_report_path = os.path.join(test_current_path, "_report")


test_report_file_name = "20231231-123456"
test_report_file_path = os.path.join(test_report_path, test_report_file_name + ".json")


### Test Functions ###


@pytest.fixture
def scrap_report():
    scrap_report = ScrapReport(test_report_path)
    scrap_report.report_file_name = test_report_file_name
    yield scrap_report


### start Test ###
def test_ScrapReport_is_singleton(scrap_report: ScrapReport):
    # Given
    scrap_report_other = ScrapReport(test_report_path)

    # Then
    assert scrap_report is scrap_report_other


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
    # When
    report = scrap_report.get_report()

    assert report == test_scrap_report_data.model_dump()


def test_update_report(scrap_report: ScrapReport):
    # Given

    # When
    scrap_report.update_report({"db_update": True})

    # Then
    report = scrap_report.get_report()
    assert report["db_update"] == True
    scrap_report.update_report({"db_update": False})


@pytest.mark.asyncio
async def test_delete_report(scrap_report: ScrapReport):
    # Given

    # When
    scrap_report.delete_report()

    # Then
    assert not os.path.exists(scrap_report.report_file_path)

    await scrap_report.create_report_with_scrap_time_as_file_name(
        report_data=test_scrap_report_data
    )


def test_get_report_list(scrap_report: ScrapReport):
    # When
    report_list = scrap_report.get_report_list()

    # Then
    assert report_list == [test_report_file_name]
