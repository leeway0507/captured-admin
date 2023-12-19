"""Shop Product Card Page Main"""

import asyncio
from itertools import chain
from datetime import datetime
from typing import List, Optional
from traceback import format_exception

from pydantic import BaseModel

from env import dev_env
from model.db_model_shop import ShopProductCardSchema, ShopProductSizeSchema
from ..size_converter import convert_size

from .candidate_extractor import (
    SearchType,
    CandidateExtractor as E,
)

from .page_module_factory import (
    ShopPageModuleFactory as F,
    ShopPageModule,
)
from .page_scraper import ShopPageScrapMachine as PageScrapMachine


from ...utils.browser_controller import BrowserController as B, PageController as P
from ...utils.temp_file_manager import TempFileManager
from ...utils.util import split_size, save_to_parquet
from ...utils.scrap_report import ScrapReport, ScrapMeta


class PreProcessData(BaseModel):
    shop_product_size: str
    shop_product_card_id: int
    kor_product_size: str
    product_id: str
    available: bool = True
    updated_at: datetime


class ScrapResult(BaseModel):
    shop_product_card_id: int
    shop_name: str
    brand_name: str
    url: str
    product_id: Optional[str] = None
    status: str


class ShopPageMain:
    def __init__(
        self, n_p: int, browser_controller: B, module_factory: F, extractor: E
    ):
        self.browser_controller = browser_controller
        self.ModuleFactory = module_factory
        self.reporter = ScrapReport("shop_page")
        self.path = dev_env.SHOP_PRODUCT_PAGE_DIR  # type: ignore
        self.tfm = TempFileManager("shop_page")
        self.E = extractor
        self.num_process = n_p

    async def main(self, search_type: str, value: str):
        self.tfm.init_temp_file()

        scrap_list = await self.extract_scrap_list(search_type, value)
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
            self.reporter.create_new_report(save_time)
            scrap_name = f"{save_time}"
            return {"scrap_status": "success", "scrap_name": scrap_name}

        except Exception as e:
            print("shop_product_card_page scrap error")
            print("".join(format_exception(None, e, e.__traceback__)))
            return {
                "scrap_status": "fail",
                "error": str(e),
                "scrap_log": scrap_log,
            }

    async def extract_scrap_list(self, search_type: str, value: str):
        scraplist = await self.E.extract_data(SearchType(search_type), value)

        if scraplist == []:
            raise ValueError(f"scraplist is Empty : {scraplist}")
        return scraplist

    async def execute_sub_scraper(
        self, scrap_candidate_list: List[ShopProductCardSchema]
    ) -> list[ScrapResult]:
        P_list = [
            await self.browser_controller.create_page_controller()
            for _ in range(self.num_process)
        ]
        job = split_size(scrap_candidate_list, self.num_process)
        co_list = [self.sub_process(P_list[i], job[i]) for i in range(self.num_process)]
        result = await asyncio.gather(*co_list)
        return list(chain(*result))

    async def sub_process(
        self, page_controller: P, job: List[ShopProductCardSchema]
    ) -> list[ScrapResult]:
        log = []

        for page_info in job:
            shop_name = page_info.shop_name
            brand_name = page_info.brand_name
            product_url = page_info.product_url
            shop_product_card_id = page_info.shop_product_card_id
            assert shop_product_card_id, f"{shop_product_card_id} does not exist"

            Module: ShopPageModule = getattr(self.ModuleFactory, shop_name)()
            assert Module, f"{shop_name} does not exist in shop_product_page_dict"

            for i in range(2):
                try:
                    page_data = await PageScrapMachine(page_controller, Module).execute(
                        product_url
                    )

                    preprocess_data = _preporcess_size_data(
                        shop_product_card_id,
                        page_data["size_info"],
                        page_data["product_id"],
                    )

                    serialized_data = [x.model_dump() for x in preprocess_data]
                    await self.tfm.save_temp_file("product_card_page", serialized_data)

                    log.append(
                        ScrapResult(
                            shop_product_card_id=shop_product_card_id,
                            shop_name=shop_name,
                            brand_name=brand_name,
                            url=page_info.product_url,
                            product_id=page_data["product_id"],
                            status="success",
                        )
                    )
                    break

                except Exception as e:
                    print(f"scrap_error: {shop_name}-{brand_name}-{i+1} 실패")
                    print("".join(format_exception(None, e, e.__traceback__)))
                    if i == 1:
                        log.append(
                            ScrapResult(
                                shop_product_card_id=shop_product_card_id,
                                shop_name=shop_name,
                                brand_name=brand_name,
                                url=page_info.product_url,
                                status=str(e),
                            )
                        )

                    await page_controller.reopen_new_page()
                    continue
        await page_controller.close_page()
        return log

    async def save_scrap_result_to_parquet(self):
        time_now = datetime.now().strftime("%y%m%d-%H%M%S")

        raw_data = await self.tfm.load_temp_file("product_card_page")

        if isinstance(raw_data, tuple):
            """
            여러 브랜드 수집 시 list_data type은 tuple임.
            브랜드 하나 수집 시 list_data type은 list임.
            """
            from itertools import chain

            raw_data = list(chain(*raw_data))

        size_schema = [ShopProductSizeSchema(**row).model_dump() for row in raw_data]

        product_id_Schema = {}
        for row in raw_data:
            key = row["shop_product_card_id"]
            value = row["product_id"]
            if value not in product_id_Schema.values():
                product_id_Schema[key] = value

        product_id_Schema_list = [
            {
                "shop_product_card_id": k,
                "product_id": v,
            }
            for k, v in product_id_Schema.items()
        ]

        save_to_parquet(self.path, time_now + "-size", size_schema)
        save_to_parquet(self.path, time_now + "-product-id", product_id_Schema_list)

        return time_now


def _preporcess_size_data(
    shop_product_card_id: int, size_info: List, product_id: str
) -> List[PreProcessData]:
    preprocessed_data = []

    for data in size_info:
        preprocessed_data.append(
            PreProcessData(
                shop_product_size=data["shop_product_size"],
                kor_product_size=str(convert_size(data["kor_product_size"])),
                shop_product_card_id=shop_product_card_id,
                product_id=product_id,
                updated_at=datetime.now().replace(microsecond=0),
            )
        )

    return preprocessed_data
