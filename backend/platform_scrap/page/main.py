import os
from typing import List

import pandas as pd

from platform_scrap.page.scraper_main import PlatformPageScraperFactory
from platform_scrap.page.report import PlatformPageReport
from platform_scrap.page.data_save import PlatformPageDataSave
from components.abstract_class.scraper_main import PlatformScraper
from components.file_manager import ScrapReport


class PlatformPageMain:
    def __init__(self, path: str, platform_list_path: str):
        self.platform_list_path = platform_list_path
        self.main_scraper_factory = PlatformPageScraperFactory(path)
        self.Report = PlatformPageReport(path)
        self.DataSave = PlatformPageDataSave(path)
        self._main_scraper = None

    @property
    def main_scraper(self):
        if not self._main_scraper:
            raise ValueError("main scraper is not set")
        return self._main_scraper

    @main_scraper.setter
    def main_scraper(self, main_scraper: PlatformScraper):
        self._main_scraper = main_scraper

    async def execute(self):
        await self.main_scraper.scrap()
        await self.Report.save_report()
        await self.DataSave.save_scrap_data()

    async def init_pw_kream_scraper(
        self, searchType: str, value: str, num_processor: int
    ):
        self.set_values(searchType, value)
        self.main_scraper = await self.main_scraper_factory.pw_kream()
        self.set_target_list_and_folder_name()
        self.main_scraper.late_binding(num_processor)

    def set_values(self, searchType, value):
        self.searchType = searchType
        self.value = value

    def set_target_list_and_folder_name(self):
        folder_name, target_list = self.extract_folder_name_and_target_data()
        self.DataSave.folder_name = folder_name
        self.main_scraper.target_list = target_list

    def extract_folder_name_and_target_data(self):
        if self.searchType == "scrapDate":
            folder_name = self.get_brand_name_by_scrap_date()
            target_list = self.get_target_list_by_scrap_date()
            return folder_name, target_list

        if self.searchType == "kreamId":
            return "kream_id", self.value.split(",")

        raise Exception("searchType should be scrapDate or kreamId")

    def get_brand_name_by_scrap_date(self):
        if self.value == "lastScrap":
            self.value = self.get_last_scrap_date_name()

        return self.get_brand_name_from_report()

    def get_brand_name_from_report(self):
        import json

        file_path = os.path.join(
            self.platform_list_path, "_report", self.value + ".json"
        )
        with open(file_path) as f:
            file = json.load(f)

        return file["brand_name"]

    def get_target_list_by_scrap_date(self):
        if self.value == "lastScrap":
            self.value = self.get_last_scrap_date_name()

        return self.get_kream_id_by_scrap_date()

    def get_last_scrap_date_name(self) -> str:
        """가장 최근에 생성된 데이터명을 가져온다."""
        file_names = os.listdir(os.path.join(self.platform_list_path, "_report"))
        file_names.sort()
        last_scrap_file_name = file_names[-1]
        file_name = last_scrap_file_name.split(".json")[0]
        return file_name

    def get_kream_id_by_scrap_date(self):
        file_path = os.path.join(
            self.platform_list_path, "kream", self.value + ".parquet.gzip"
        )
        return self.extract_unique_kream_id(file_path)

    def extract_unique_kream_id(self, file_path: str):
        df = pd.read_parquet(file_path)
        series = df["kream_id"].drop_duplicates()
        return series.to_list()
