import os
import asyncio
from traceback import format_exception
from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Dict
from itertools import chain
from datetime import datetime

import pandas as pd
from pydantic import BaseModel

from .utils.file_manager import ScrapTempFile, ScrapReport, ScrapReportDataBase
from .utils.browser_controller import BrowserController, PageController
from .utils.util import ListSeparator
from components.dev.platform.platform_browser_controller import (
    PlatformBrowserController,
)
from components.dev.sub_scraper import SubScraper


class ScrapStatusBase(BaseModel):
    job: str
    status: str | Dict | List | Tuple


class Scraper(ABC):
    def __init__(
        self,
        temp_path: str,
        report_path: str,
    ):
        self.TempFile = ScrapTempFile(temp_path)
        self.Report = ScrapReport(report_path)

        self.scrap_time = ""
        self._target_list = []
        self._scrap_folder_name = None

    def late_binding(
        self, browser: BrowserController, sub_scraper: SubScraper, num_processor: int
    ):
        self.browser = browser
        self.num_processor = num_processor
        self.sub_scraper = sub_scraper

    async def scrap(self):
        try:
            await self.main()

        except Exception as e:
            self.exception_error(e)

    async def main(self):
        self.set_scrap_time()
        self.check_necessary_property()
        self.TempFile.init()
        await self.browser_login()
        await self.execute_sub_processors()
        await self.create_scrap_report()
        await self.save_scrap_data()
        print(f"scrap done")

    def exception_error(self, e: Exception):
        print("shop_product_card_page scrap error")
        print("".join(format_exception(None, e, e.__traceback__)))
        return {
            "scrap_status": "fail",
            "error": str(e),
        }

    def check_necessary_property(self):
        if not self.scrap_folder_name:
            raise ValueError("scrap_folder_name is None!")

        if not self.target_list:
            raise ValueError("target_list is None!")

        if not self.scrap_time:
            raise ValueError("scrap_time is None!")

    @abstractmethod
    async def browser_login():
        ...

    @property
    def target_list(self):
        if not self._target_list:
            raise ValueError("target_list is None")
        return self._target_list

    @target_list.setter
    def target_list(self, target_list: List[str]):
        if not isinstance(target_list, list) and not isinstance(target_list, tuple):
            raise TypeError("target_list is not list[str] type")
        self._target_list = target_list

    async def execute_sub_processors(self):
        sub_processors = await self.allocate_target_to_sub_processor()
        await asyncio.gather(*sub_processors)

    async def allocate_target_to_sub_processor(self):
        pages = [await self.browser.create_page() for _ in range(self.num_processor)]

        job = ListSeparator.split(self.target_list, self.num_processor)

        sub_processors = [
            self.sub_processor(pages[i], job[i]) for i in range(self.num_processor)
        ]
        return sub_processors

    async def sub_processor(self, page: PageController, job: List[str]):
        self.init_sub_scraper(page)
        await self.execute_sub_processor_scrap(job)

    @abstractmethod
    def init_sub_scraper(self, page: PageController):
        pass

    async def execute_sub_processor_scrap(self, jobs: List):
        retry = 2
        status = "fail"
        for job in jobs:
            for _ in range(retry):
                try:
                    status, data = await self.execute_sub_scraper(job)
                    await self.save_data_to_temp(data)
                    break

                except Exception as e:
                    status = await self.handle_scrap_error(job, e)
                    await self.reopen_page()

            scrap_temp_template = self.set_scrap_status_temp_template(job, status)
            await self.save_scrap_status_to_temp(scrap_temp_template)

        await self.sub_scraper.page_controller.close_page()

    async def execute_sub_scraper(self, job: str):
        self.sub_scraper.allocate_job(job)
        return await self.sub_scraper.execute()

    @abstractmethod
    async def save_data_to_temp(self, data):
        pass

    async def handle_scrap_error(self, job: str, e: Exception):
        print(f"scrap_error: {job} 실패")
        print("".join(format_exception(None, e, e.__traceback__)))
        return f"failed: {str(e)}"

    async def reopen_page(self):
        return await self.sub_scraper.reopen_new_page()

    def set_scrap_status_temp_template(self, job: str, status: str):
        return ScrapStatusBase(job=job, status=status)

    async def save_scrap_status_to_temp(self, template: ScrapStatusBase):
        await self.TempFile.append_temp_file("scrap_status", template.model_dump())

    def set_scrap_time(self):
        self.scrap_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return self.scrap_time

    async def create_scrap_report(self):
        temp_scrap_status = await self.load_temp_scrap_data()
        report_data = self.create_report_template(temp_scrap_status)
        await self.Report.create_report_with_scrap_time_as_file_name(
            report_data=report_data
        )

    async def load_temp_scrap_data(self) -> List:
        data = await self.TempFile.load_temp_file("scrap_status")
        if isinstance(data, tuple):
            return list(data)

        if isinstance(data, dict):
            return [data]

        raise TypeError("temp_scrap_data is not list or dict")

    @abstractmethod
    def create_report_template(self, temp_scrap_status: List) -> ScrapReportDataBase:
        pass

    @property
    def scrap_folder_name(self):
        if not self._scrap_folder_name:
            raise ValueError("scrap_folder_name is not set")
        return self._scrap_folder_name

    @scrap_folder_name.setter
    def scrap_folder_name(self, scrap_folder_name: str):
        self._scrap_folder_name = scrap_folder_name

    @abstractmethod
    async def save_scrap_data(self):
        pass

    def _save_parquet(self, path: str, data: List):
        pd.DataFrame(data).drop_duplicates().to_parquet(path=path, compression="gzip")
        return True


class PlatformScrapStatus(ScrapStatusBase):
    platform_type: str


class PlatformScraper(Scraper):
    def __init__(
        self,
        temp_path: str,
        report_path: str,
    ):
        super().__init__(
            temp_path,
            report_path,
        )

    def late_binding(
        self,
        browser: PlatformBrowserController,
        sub_scraper: SubScraper,
        num_processor: int,
        platform_type: str,
    ):
        self.browser = browser
        self.num_processor = num_processor
        self.sub_scraper = sub_scraper
        self.platform_type = platform_type

    async def browser_login(self):
        await self.browser.login()


class ShopScraper(Scraper):
    def __init__(
        self,
        path: str,
        scrap_type: str,
    ):
        super().__init__(
            os.path.join(path, "_temp"),
            os.path.join(path, "_report"),
        )
        self.scrap_type = scrap_type
        self.path = path

    def late_binding(
        self,
        browser: BrowserController,
        sub_scraper: SubScraper,
        num_processor: int,
        shop_name: str,
    ):
        self.browser = browser
        self.num_processor = num_processor
        self.sub_scraper = sub_scraper
        self.shop_name = shop_name

    # concrete_method
    def browser_login(self):
        pass

    # concrete_method
    def init_sub_scraper(self, page: PageController):
        return self.sub_scraper.late_binding(page)

    # concrete_method
    async def save_data_to_temp(self, data: List):
        await self._save_card_data_to_temp(data)

    async def _save_card_data_to_temp(self, card_data: List):
        if card_data:
            await self._save_data_to_temp(card_data)

    async def _save_data_to_temp(self, card_data: List):
        await self.TempFile.append_temp_file(self.scrap_type, card_data)

    # concrete_method
    def create_report_template(self, temp_scrap_status: List) -> ScrapReportDataBase:
        return ScrapReportDataBase(
            scrap_time=self.scrap_time,
            num_of_plan=len(temp_scrap_status),
            num_processor=self.num_processor,
            job=temp_scrap_status,
        )

    # concrete_method
    async def save_scrap_data(self):
        self._create_shop_folder()
        list_data = await self.TempFile.load_temp_file(self.scrap_type)

        preprocessed_data = self.preprocess_data(list_data)
        self.save_preprocessed_data(preprocessed_data)
        return self.scrap_time

    def _create_shop_folder(self):
        folder_path = self._generate_shop_folder_path()
        self.TempFile.create_folder(folder_path)

    def _generate_shop_folder_path(self):
        return os.path.join(self.path, self.shop_name)

    @abstractmethod
    def preprocess_data(self, data: List[Dict]) -> List[Dict]:
        pass

    @abstractmethod
    def save_preprocessed_data(self, data: List[Dict]):
        pass
