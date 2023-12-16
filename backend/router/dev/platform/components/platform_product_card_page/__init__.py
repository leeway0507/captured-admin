"""Kream List Scrap Main"""
import os
from datetime import datetime

from ..platform_browser_controller import PlatformBrowserController as PB
from .module_factory import PlatformPageModule as M
from .scraper import PlatformPageScrapMachine as ScrapMachine
from env import dev_env

from traceback import format_exception
from itertools import chain
from typing import List, Dict
from pydantic import BaseModel
import asyncio

from .candidate_extractor import CandidateExtractor, PageSearchType
from .save_manager import SaveManager, PreprocessType, ModuleFactory

from ....utils.browser_controller import PageController as P
from ....utils.scrap_report import ScrapReport, ScrapMeta
from ....utils.util import split_size
from ....utils.temp_file_manager import TempFileManager
from ..data_loader import loader, LoadType


class ScrapList(BaseModel):
    brand_name: str
    brand_url: str


class ListScrapResult(BaseModel):
    platform_type: str
    sku: str
    status: str


class PlatformScrapMeta(ScrapMeta):
    plan_list: List[int]
    search_value: str


class PlatformPageMain:
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
        self.reporter = ScrapReport("platform_page")
        self.browser_controller = browser_controller
        self.path = dev_env.PLATFORM_PRODUCT_PAGE_DIR
        self.min_volume = min_volume
        self.min_wish = min_wish
        self.platform_type = platform_type
        self.tfm = TempFileManager("platform_page")

    async def main(self, search_type: PageSearchType, value: str):
        if search_type == PageSearchType.LAST_SCRAP:
            self.scrap_folder = value
        elif search_type == PageSearchType.PRODUCT_ID:
            self.scrap_folder = "product_id"
        elif search_type == PageSearchType.SKU:
            self.scrap_folder = "sku"
        else:
            raise Exception("Invalid Search Type")

        self.tfm.init_temp_file()

        scrap_list = await self.extract_candidate_list(search_type, value)
        await self.browser_controller.login()
        scrap_log = await self.execute_sub_scraper(scrap_list)

        # parquet로 저장 전 수집 상태 json 형태로 저장(파일 저장 에러 시 복구 목적)
        self.reporter.save_temp_report(
            PlatformScrapMeta(
                num_of_plan=len(scrap_list),
                num_process=self.num_process,
                scrap_log=scrap_log,
                plan_list=scrap_list,
                search_value=value,
            )
        )

        try:
            save_time = await self.save_scrap_data()

            self.reporter.create_new_report(
                save_time,
                self.platform_type,
                external_data={
                    "product_detail": loader(
                        LoadType.PRODUCT_DETAIL, self.scrap_folder, save_time
                    ),
                    "product_bridge": loader(
                        LoadType.PRODUCT_BRIDGE, self.scrap_folder, save_time
                    ),
                    "trading_volume": loader(
                        LoadType.TRADING_VOLUME, self.scrap_folder, save_time
                    ),
                    "buy_and_sell": loader(
                        LoadType.BUY_AND_SELL, self.scrap_folder, save_time
                    ),
                },
            )
            scrap_name = f"{save_time}"
            return {"scrap_status": "success", "scrap_name": scrap_name}

        except Exception as e:
            print("scrap_product_detail_main")
            print("".join(format_exception(None, e, e.__traceback__)))
            return {
                "scrap_status": "fail",
                "error": str(e),
                "scrap_log": scrap_log,
            }

    async def extract_candidate_list(
        self, search_type: PageSearchType, value: str
    ) -> List[int]:
        return await CandidateExtractor(
            self.platform_type, search_type, value
        ).extract_candidate()

    async def execute_sub_scraper(
        self, platform_sku_list: List[int]
    ) -> list[ListScrapResult]:
        P_list = [
            await self.browser_controller.create_page_controller()
            for _ in range(self.num_process)
        ]
        job = split_size(platform_sku_list, self.num_process)
        co_list = [self.sub_process(P_list[i], job[i]) for i in range(self.num_process)]
        result = await asyncio.gather(*co_list)

        return list(chain(*result))

    async def sub_process(
        self, page_controller: P, job: List[str]
    ) -> List[ListScrapResult]:
        log = []

        for platform_sku in job:
            module = self.module
            for i in range(2):
                try:
                    status = await ScrapMachine(page_controller, module).execute(
                        platform_sku
                    )
                    log.append(
                        ListScrapResult(
                            platform_type=module.__name__(),
                            sku=str(platform_sku),
                            status=status,
                        )
                    )
                    break
                except Exception as e:
                    print(f"scrap_error: {module.__name__()}-{platform_sku} 실패")
                    print("".join(format_exception(None, e, e.__traceback__)))
                    if i == 1:
                        log.append(
                            ListScrapResult(
                                platform_type=module.__name__(),
                                sku=str(platform_sku),
                                status=str(e),
                            )
                        )
                    await page_controller.reopen_new_page()
                    continue
        await page_controller.close_page()
        return log

    async def save_scrap_data(self):
        save_path = os.path.join(self.path, self.scrap_folder)
        if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)

        save_time = datetime.now().strftime("%y%m%d-%H%M%S")
        preprocess_module = getattr(ModuleFactory(), self.platform_type)()
        manager = SaveManager(save_path, save_time, preprocess_module)

        await manager.save(PreprocessType.PRODUCT_DETAIL)
        await manager.save(PreprocessType.PRODUCT_BRIDGE)
        await manager.save(PreprocessType.TRADING_VOLUME)
        await manager.save(PreprocessType.BUY_AND_SELL)

        return save_time
