"""Kream List Scrap Main"""
import os

from traceback import format_exception
from typing import List

from pydantic import BaseModel

from components.dev.utils.browser_controller import PageController as P
from ..platform_browser_controller import PlatformBrowserController
from .sub_scraper import PlatformListSubScraper

from ...scraper import PlatformScraper, PlatformScrapStatus, ScrapReportDataBase


class PlatformListReportData(ScrapReportDataBase):
    platform_type: str


class PlatformListScraper(PlatformScraper):
    def __init__(
        self,
        path: str,
        num_processor: int,
        browser: PlatformBrowserController,
        sub_scraper: PlatformListSubScraper,
        platform_type: str,
        min_volume: int = 100,
        min_wish: int = 50,
    ):
        super().__init__(
            os.path.join(path, "_temp"),
            os.path.join(path, "_report"),
            browser,
            num_processor,
            platform_type,
            sub_scraper,
        )
        self.path = path
        self.min_volume = min_volume
        self.min_wish = min_wish
        self.sub_scraper = sub_scraper

    ####
    # self.TempFile.init()
    # self.browser_login()
    # target_list = self.extract_target_list()
    # scrap_status_result = await self.execute_sub_processors(target_list)
    # await self.create_scrap_report(scrap_status_result)
    # self.save_scrap_data()

    # concrete_method
    def init_sub_scraper(self, page: P):
        return self.sub_scraper.late_binding(page, self.min_volume, self.min_wish)

    # concrete_method
    async def execute_job(self, job: str):
        card_data = await self.excute_sub_process_job(job)
        return f"success : {len(card_data)} 개", card_data

    async def excute_sub_process_job(self, job: str):
        self.sub_scraper.allocate_job(job)
        return await self.sub_scraper.execute()

    # concrete_method
    async def save_data_to_temp(self, data: List):
        await self.save_card_data_to_temp(data)

    async def save_card_data_to_temp(self, card_data: List):
        if card_data:
            await self._save_data_to_temp(card_data)

    async def _save_data_to_temp(self, card_data: List):
        serialized_data = [x.model_dump() for x in card_data]
        await self.TempFile.append_temp_file("product_card_list", serialized_data)

    # concrete_method
    async def reopen_page(self):
        return await self.sub_scraper.reopen_new_page()

    # concrete_method
    def create_report_template(self, temp_scrap_status: List) -> ScrapReportDataBase:
        return PlatformListReportData(
            scrap_time=self.scrap_time,
            num_of_plan=len(temp_scrap_status),
            num_processor=self.num_processor,
            job=list(temp_scrap_status),
            platform_type=self.platform_type,
        )

    # concrete_method
    async def save_scrap_data(self):
        folder_path = self.generate_folder_path()
        self.TempFile.create_folder(folder_path)

        file_path = self.generate_file_path()
        list_data = await self.load_scrap_data()
        self._save_parquet(file_path, list_data)

    def generate_folder_path(self):
        return os.path.join(self.path, self.platform_type, self.scrap_folder_name)

    def generate_file_path(self):
        file_name = self.scrap_time + "-product_card_list" + ".parquet.gzip"
        file_path = os.path.join(self.generate_folder_path(), file_name)
        return file_path

    async def load_scrap_data(self):
        return await self.TempFile.load_temp_file("product_card_list")
