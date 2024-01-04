import pandas as pd
import os
from typing import Dict, List, Optional
from env import dev_env
from enum import Enum

default_path = "router/dev/kream/data/detail/"


#####################


class LoadType(Enum):
    PRODUCT_CARD_LIST = ["product_card_list", dev_env.PLATFORM_PRODUCT_LIST_DIR]
    PRODUCT_DETAIL = ["product_detail", dev_env.PLATFORM_PRODUCT_PAGE_DIR]
    PRODUCT_BRIDGE = ["product_bridge", dev_env.PLATFORM_PRODUCT_PAGE_DIR]
    TRADING_VOLUME = ["trading_volume", dev_env.PLATFORM_PRODUCT_PAGE_DIR]
    BUY_AND_SELL = ["buy_and_sell", dev_env.PLATFORM_PRODUCT_PAGE_DIR]


class PlatformDataLoader:
    def __init__(
        self,
        path: str,
        brand: str,
        platform: str,
        scrap_date: str,
        sample: int = 10,
    ):
        self.file_type = None
        self.path = path
        self.brand = brand
        self.platform = platform
        self.sample = sample
        self.scrap_date = scrap_date

    @staticmethod
    def get_last_scrap_date_name(product_card_list_path: str) -> str:
        """가장 최근에 생성된 데이터명을 가져온다."""
        file_names = os.listdir(product_card_list_path)
        file_names.sort()
        last_scrap_file_name = file_names[-1]
        file_name = last_scrap_file_name.rsplit("-", 1)[0]
        return file_name

    def load(self, file_type: str):
        self.file_type = file_type
        data = self.load_file()
        return self.set_template(data)

    def load_file(self):
        file_name = f"{self.scrap_date}-{self.file_type}.parquet.gzip"
        file_path = os.path.join(self.path, self.brand, file_name)
        return pd.read_parquet(file_path).to_dict("records")

    def set_template(self, data):
        kream_id_list = self.get_unique_kream_id(data)
        return {
            "len": len(kream_id_list),
            "kream_id_list": kream_id_list,
            "data": data[: self.sample],
        }

    def get_unique_kream_id(self, data):
        return list(set(map(lambda x: x.get("kream_id"), data)))
