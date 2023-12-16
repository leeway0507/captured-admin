import os
import pandas as pd

from typing import Protocol, List, Dict
from itertools import chain
from datetime import datetime
from ....utils.temp_file_manager import TempFileManager
from enum import Enum
from model.kream_scraping import KreamProductDetailSchema
from model.db_model_kream import (
    KreamProductIdBridgeSchmea,
    KreamTradingVolumeSchema,
    KreamBuyAndSellSchema,
)


class PreprocessType(Enum):
    PRODUCT_DETAIL = "product_detail"
    PRODUCT_BRIDGE = "product_bridge"
    TRADING_VOLUME = "trading_volume"
    BUY_AND_SELL = "buy_and_sell"


class ModuleFactory:
    def kream(self) -> "KreamPreprocessModule":
        return KreamPreprocessModule()


class PreprocessModule(Protocol):
    def product_detail(self, data: List[Dict]) -> pd.DataFrame:
        ...

    def product_bridge(self, data: List[Dict]) -> pd.DataFrame:
        ...

    def trading_volume(self, data: List[Dict]) -> pd.DataFrame:
        ...

    def buy_and_sell(self, data: List[Dict]) -> pd.DataFrame:
        ...


class KreamPreprocessModule:
    def product_detail(self, data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return pd.DataFrame(
            [
                KreamProductDetailSchema(**row).model_dump()  # type: ignore
                for row in df.to_dict("records")
            ]
        )

    def product_bridge(self, data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return pd.DataFrame(
            [
                KreamProductIdBridgeSchmea(**row).model_dump()  # type: ignore
                for row in df.to_dict("records")
            ]
        )

    def trading_volume(self, data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(list(chain(*data)))
        return pd.DataFrame(
            [
                KreamTradingVolumeSchema(**row).model_dump()  # type: ignore
                for row in df.to_dict("records")
            ]
        )

    def buy_and_sell(self, data: List[Dict]) -> pd.DataFrame:
        df_list = [pd.DataFrame(i) for i in data]
        df = pd.concat(df_list)

        # filter
        df = df[(df["sell"] != 0) | (df["buy"] != 0)]

        # columns
        df = df.reset_index()
        df = df.rename(columns={"index": "kream_product_size"})
        df["updated_at"] = datetime.now().replace(microsecond=0)

        return pd.DataFrame(
            [KreamBuyAndSellSchema(**row).model_dump() for row in df.to_dict("records")]  # type: ignore
        )


class SaveManager:
    def __init__(
        self,
        path: str,
        file_name: str,
        preprocess_module: PreprocessModule,
        return_data: bool = True,
    ) -> None:
        self.path = path
        self.file_name = file_name
        self.preprocess_module = preprocess_module
        self.return_data = return_data
        self.tfm = TempFileManager("platform_page")
        self._make_dir(path)

    def _make_dir(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    async def save(self, type: PreprocessType):
        module = getattr(self.preprocess_module, type.value)

        if type == PreprocessType.PRODUCT_BRIDGE:
            data = await self.tfm.load_temp_file("product_detail")
        else:
            data = await self.tfm.load_temp_file(type.value)

        pre_processed_data = module(data)

        self.save_data(pre_processed_data, self.path, self.file_name, type.value)
        if self.return_data:
            return pre_processed_data.to_dict("records")
        return {"status": "success"}

    def save_data(self, df: pd.DataFrame, path: str, file_time: str, type: str):
        file_name = f"{file_time}-{type}.parquet.gzip"
        file_path = os.path.join(path, file_name)
        return df.to_parquet(file_path, compression="gzip")
