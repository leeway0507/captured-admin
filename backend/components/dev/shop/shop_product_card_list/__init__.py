import os
import asyncio
from itertools import chain
from datetime import datetime
from typing import List
from traceback import format_exception

import pandas as pd
from pydantic import BaseModel

from env import dev_env


from model.db_model_shop import ShopProductCardSchema
from ..currency import Currency

from .list_scraper import ShopListScrapMachine as ScrapMachine
from .list_module_factory import ShopListModuleFactory as F
from .schema import ListScrapData

from ...utils.scrap_report import ScrapReport, ScrapMeta
from ...utils.browser_controller import BrowserController as B, PageController as P
from ...utils.temp_file_manager import TempFileManager
from ...utils.util import split_size


class PreProcessData(BaseModel):
    shop_product_size: str
    shop_product_card_id: int
    kor_product_size: str
    product_id: str
    available: bool = True
    updated_at: datetime


class ListScrapResult(BaseModel):
    shop_name: str
    brand_name: str
    status: str


class ShopListMain:
    def __init__(
        self, n_p: int, browser_controller: B, module_factory: F, shop_name: str
    ):
        self.module_factory = module_factory
        self.reporter = ScrapReport("shop_list")
        self.tfm = TempFileManager("shop_list")
        self.browser_controller = browser_controller
        self.path = dev_env.SHOP_PRODUCT_LIST_DIR
        self.num_process = n_p
        self.shop_name = shop_name

    async def main(self, brand_name_list: str):
        self.tfm.init_temp_file()

        scrap_list = await self.extract_scrap_list(brand_name_list)
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
            self.reporter.create_new_report(save_time, self.shop_name)
            scrap_name = f"{save_time}"
            return {"scrap_status": "success", "scrap_name": scrap_name}

        except Exception as e:
            print("shop_product_card_list scrap error")
            print("".join(format_exception(None, e, e.__traceback__)))
            return {
                "scrap_status": "fail",
                "error": str(e),
                "scrap_log": scrap_log,
            }

    async def extract_scrap_list(self, brand_name: str):
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

    async def sub_process(self, page_controller: P, job: List[str]):
        log = []

        for brand_name in job:
            module = getattr(self.module_factory, self.shop_name)()

            for i in range(2):
                try:
                    card_data = await ScrapMachine(page_controller, module).execute(
                        brand_name
                    )
                    if card_data:
                        preprocess_data = _preprocess_list_data(card_data)
                        serialized_data = [x.model_dump() for x in preprocess_data]

                        await self.tfm.save_temp_file(
                            "product_card_list", serialized_data
                        )
                    log.append(
                        ListScrapResult(
                            shop_name=self.shop_name,
                            brand_name=brand_name,
                            status=f"success : {len(card_data)} 개",
                        )
                    )
                    break
                except Exception as e:
                    print(f"scrap_error: {self.shop_name}-{brand_name}-{i+1} 실패")
                    print("".join(format_exception(None, e, e.__traceback__)))
                    if i == 1:
                        log.append(
                            ListScrapResult(
                                shop_name=self.shop_name,
                                brand_name=brand_name,
                                status=str(e),
                            )
                        )

                    await page_controller.reopen_new_page()
                    continue
        await page_controller.close_page()
        return log

    async def save_scrap_result_to_parquet(self):
        time_now = datetime.now().strftime("%y%m%d-%H%M%S")
        list_data = await self.tfm.load_temp_file("product_card_list")

        if isinstance(list_data, tuple):
            """
            여러 브랜드 수집 시 list_data type은 tuple임.
            브랜드 하나 수집 시 list_data type은 list임.
            """
            from itertools import chain

            list_data = list(chain(*list_data))

        save_path = os.path.join(self.path, self.shop_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)

        file_path = os.path.join(save_path, f"{time_now}.parquet.gzip")
        pd.DataFrame(list_data).drop_duplicates(subset="shop_product_name").to_parquet(
            path=file_path, compression="gzip"
        )

        return time_now


def _preprocess_list_data(
    cards_info: List[ListScrapData],
) -> List[ShopProductCardSchema]:
    currency = Currency()

    # currency
    lst = []
    for card in cards_info:
        price = card.price

        _, curr_name, origin_price = currency.get_price_info(price)

        (_, _, us_price) = currency.change_currency_to_custom_usd(price)

        (_, _, kor_price) = currency.change_currency_to_buying_won(price)

        lst.append(
            ShopProductCardSchema(
                original_price_currency=curr_name,
                original_price=origin_price,
                us_price=us_price,
                kor_price=int(round(kor_price, -3)),
                updated_at=datetime.now().replace(microsecond=0),
                **card.model_dump(),
            )
        )
    return lst
