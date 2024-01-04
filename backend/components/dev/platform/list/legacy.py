"""Kream List Scrap Main"""
import os
from datetime import datetime

from ...utils.util import save_to_parquet, split_size
from ...utils.browser_controller import PageController as P
from ...utils.scrap_report import ScrapReport, ScrapMeta
from ...utils.file_manager.file_manager import ScrapTempFile

from ..platform_browser_controller import PlatformBrowserController as PB
from .sub_scraper_factory import PlatformListModule as M
from .scraper import PlatformListScrapMachine as ScrapMachine
from env import dev_env

from traceback import format_exception
from itertools import chain
from typing import List
from pydantic import BaseModel
import asyncio


class ScrapList(BaseModel):
    brand_name: str
    brand_url: str


class ListScrapResult(BaseModel):
    platform_type: str
    brand_name: str
    status: str


class PlatformListMain:
    def __init__(
        self,
        n_p: int,
        browser_controller: PB,
        module: M,
        min_volume=100,
        min_wish=50,
        platform_type="kream",
    ):
        self.num_process = n_p
        self.module = module
        self.reporter = ScrapReport("platform_list")
        self.tfm = ScrapTempFile("platform_list")
        self.browser_controller = browser_controller
        self.path = dev_env.PLATFORM_PRODUCT_LIST_DIR
        self.min_volume = min_volume
        self.min_wish = min_wish
        self.platform_type = platform_type

    async def main(self, brand_name: str):
        self.brand_name = brand_name
        self.tfm.init_temp_file()
        scrap_list = await self.extract_scrap_list(brand_name)

        await self.browser_controller.login()
        scrap_log = await self.execute_sub_scraper(scrap_list)

        # parquet로 저장 전 수집 상태 json 형태로 저장(파일 저장 에러 시 복구 목적)
        self.reporter.save_temp_report(
            ScrapMeta(
                num_of_plan=len(scrap_log),
                num_process=self.num_process,
                scrap_log=scrap_log,
            )
        )
        try:
            save_time = await self.save_scrap_result_to_parquet()
            self.reporter.create_new_report(save_time, self.platform_type)
            scrap_name = f"{save_time}"
            return {"scrap_status": "success", "scrap_name": scrap_name}

        except Exception as e:
            print("platform_product_card_list scrap error")
            print("".join(format_exception(None, e, e.__traceback__)))
            return {
                "scrap_status": "fail",
                "error": str(e),
                "scrap_log": scrap_log,
            }

    async def extract_scrap_list(self, brand_name: str) -> List[str]:
        return brand_name.split(",")

    async def execute_sub_scraper(
        self, scrap_brand_list: List[str]
    ) -> list[ListScrapResult]:
        P_list = [
            await self.browser_controller.create_page_controller()
            for _ in range(self.num_process)
        ]
        job = split_size(scrap_brand_list, self.num_process)
        co_list = [self.sub_process(P_list[i], job[i]) for i in range(self.num_process)]
        result = await asyncio.gather(*co_list)
        return list(chain(*result))

    async def sub_process(
        self, page_controller: P, job: List[str]
    ) -> List[ListScrapResult]:
        log = []

        for brand_name in job:
            try:
                card_data = await ScrapMachine(page_controller, self.module).execute(
                    brand_name, self.min_volume, self.min_wish
                )
                if card_data:
                    serialized_data = [x.model_dump() for x in card_data]
                    await self.tfm.save_temp_file("product_card_list", serialized_data)
                log.append(
                    ListScrapResult(
                        platform_type=self.module.__name__(),
                        brand_name=brand_name,
                        status=f"success : {len(card_data)} 개",
                    )
                )
            except Exception as e:
                print(f"scrap_error: {self.module.__name__()}-{brand_name} 실패")
                print("".join(format_exception(None, e, e.__traceback__)))
                log.append(
                    ListScrapResult(
                        platform_type=self.module.__name__(),
                        brand_name=brand_name,
                        status=str(e),
                    )
                )
        await page_controller.close_page()
        return log

    async def save_scrap_result_to_parquet(self):
        time_now = datetime.now().strftime("%y%m%d-%H%M%S")
        save_path = os.path.join(self.path, self.platform_type)
        file_name = time_now + "-product_card_list"
        list_data = await self.tfm.load_temp_file("product_card_list")
        save_to_parquet(save_path, file_name, list_data)

        return time_now
