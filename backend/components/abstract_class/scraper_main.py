import os
import asyncio
from traceback import format_exception
from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Dict, Callable
from datetime import datetime

from pydantic import BaseModel

from ..file_manager import ScrapTempFile
from ..list_separator import ListSeparator
from .scraper_sub import SubScraper
from ..browser_handler import ContextHandler, PageHandler, PlatformContextHandler


class ScrapStatusBase(BaseModel):
    job: str
    status: str | Dict | List | Tuple


class Scraper(ABC):
    def __init__(
        self,
        path,
        browser: ContextHandler,
        num_processor: int,
        sub_scraper_class: Callable[..., SubScraper],
    ):
        self.TempFile = ScrapTempFile(os.path.join(path, "_temp"))
        self.browser = browser
        self.num_processor = num_processor
        # TODO:sub_scraper_class말고 sub_scraper_factory로 변경 필요. shop_page main.py 참조
        self.sub_scraper_class = sub_scraper_class
        self.path = path

        self.scrap_time = ""
        self._target_list = []

    @property
    def target_list(self):
        if not self._target_list:
            raise ValueError("target_list is None")
        return self._target_list

    @target_list.setter
    def target_list(self, target_list: List):
        if not isinstance(target_list, list) and not isinstance(target_list, tuple):
            raise TypeError("target_list is not list type")
        self._target_list = target_list

    async def scrap(self):
        try:
            await self.main()

        except Exception as e:
            self.exception_error(e)

    async def main(self):
        await self.init()
        await self.browser_login()
        await self.execute_sub_processors()
        print(f"scrap done")

    def exception_error(self, e: Exception):
        print("shop_product_card_page scrap error")
        print("".join(format_exception(None, e, e.__traceback__)))
        return {
            "scrap_status": "main scraper failed:",
            "error": str(e),
        }

    async def init(self):
        self.init_scrap_time()
        self.TempFile.init()
        self._check_necessary_property()
        await self.save_scrap_config_to_temp_file()

    def init_scrap_time(self):
        self.scrap_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return self.scrap_time

    def _check_necessary_property(self):
        error = []
        if not self.target_list:
            error.append("target_list")

        if error:
            raise ValueError(f"{error} <- please update this values")

    @abstractmethod
    async def save_scrap_config_to_temp_file(self):
        ...

    @abstractmethod
    async def browser_login():
        ...

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

    async def sub_processor(self, page: PageHandler, jobs: List[Any]):
        sub_scraper = self.sub_scraper_class()
        sub_scraper.late_binding(page, **self.set_sub_scraper_params())

        for job in jobs:
            status = await self.execute_job(sub_scraper, job)
            await self.save_scrap_status_to_temp_file(job, status)

        await sub_scraper.page_handler.close_page()

    @abstractmethod
    def set_sub_scraper_params() -> Dict:
        ...

    async def execute_job(self, sub_scraper: SubScraper, job: Any):
        status = "fail"
        retry = 2
        for _ in range(retry):
            try:
                sub_scraper.allocate_job(job)
                status, data = await sub_scraper.execute()
                await self.save_data_to_temp_file(data)
                break

            except Exception as e:
                status = await self.handle_scrap_error(job, e)

        return status

    @abstractmethod
    async def save_data_to_temp_file(self, data):
        pass

    async def handle_scrap_error(self, job: str, e: Exception):
        print(f"scrap_error: {job} 실패")
        print("".join(format_exception(None, e, e.__traceback__)))
        return f"sub scraper failed: {str(e)}"

    async def save_scrap_status_to_temp_file(self, job: str, status: str):
        template = ScrapStatusBase(job=str(job), status=status)
        await self.TempFile.append_temp_file("scrap_status", template.model_dump())