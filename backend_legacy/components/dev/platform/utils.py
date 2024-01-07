import os
import pandas as pd

from components.dev.utils.file_manager.scrap_report import ScrapReport

from env import get_path


platform_page_path = get_path("platform_page")
platform_list_path = get_path("platform_list")

page_report = ScrapReport(platform_page_path)
list_report = ScrapReport(platform_list_path)


def load_page_target_list(searchType, value):
    if searchType == "kreamId":
        return value.replace(" ", "").split(",")

    if searchType == "scrapDate":
        if value == "last":
            value = page_report.get_report_list()[0]
            print(f"last scrapDate: {value}")
        return load_kream_id_list_from_scrap_list(value)

    raise ValueError("searchType is not valid")


def load_kream_id_list_from_scrap_list(scrapDate):
    file_path = os.path.join(
        platform_list_path, "kream", scrapDate + "-product_card_list.parquet.gzip"
    )
    return pd.read_parquet(file_path)["kreamId"].drop_duplicates().tolist()


def set_scrap_folder_name(search_type, value: str):
    if search_type == "kreamId":
        return "kream_id"

    if search_type == "scrapDate":
        list_report.report_file_name = value + "-kream"
        list_report.load_report()
