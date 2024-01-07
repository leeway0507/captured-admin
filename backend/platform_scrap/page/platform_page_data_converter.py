import os
import pandas as pd

from typing import Protocol, List, Dict
from itertools import chain
from datetime import datetime
from components.file_manager import ScrapTempFile

from model.kream_scraping import KreamProductDetailSchema
from model.db_model_kream import (
    KreamProductIdBridgeSchmea,
    KreamTradingVolumeSchema,
    KreamBuyAndSellSchema,
)


class PlatformPageStrategy(Protocol):
    def preprocess(self, data: List[Dict]) -> pd.DataFrame:
        ...

    def get_temp_file_name(self) -> str:
        ...

    def get_save_file_name(self) -> str:
        ...


class PlatformPageStrategyFactory:
    @staticmethod
    def product_detail() -> PlatformPageStrategy:
        return ProductDetail()

    @staticmethod
    def product_bridge() -> PlatformPageStrategy:
        return ProductBridge()

    @staticmethod
    def trading_volume() -> PlatformPageStrategy:
        return TradingVolume()

    @staticmethod
    def buy_and_sell() -> PlatformPageStrategy:
        return BuyAndSell()


class ProductDetail:
    def preprocess(self, data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return pd.DataFrame(
            [
                KreamProductDetailSchema(**row).model_dump()  # type: ignore
                for row in df.to_dict("records")
            ]
        )

    def get_temp_file_name(self) -> str:
        return "product_detail"

    def get_save_file_name(self) -> str:
        return "product_detail"


class ProductBridge:
    def preprocess(self, data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return pd.DataFrame(
            [
                KreamProductIdBridgeSchmea(**row).model_dump()  # type: ignore
                for row in df.to_dict("records")
            ]
        )

    def get_temp_file_name(self) -> str:
        return "product_detail"

    def get_save_file_name(self) -> str:
        return "product_bridge"


class TradingVolume:
    def preprocess(self, data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return pd.DataFrame(
            [
                KreamTradingVolumeSchema(**row).model_dump()  # type: ignore
                for row in df.to_dict("records")
            ]
        )

    def get_temp_file_name(self) -> str:
        return "trading_volume"

    def get_save_file_name(self) -> str:
        return "trading_volume"


class BuyAndSell:
    def preprocess(self, data: List[Dict]) -> pd.DataFrame:
        df_list = [pd.DataFrame(i) for i in data]
        df = pd.concat(df_list)

        # filter
        df = df[(df["sell"] != "0") | (df["buy"] != "0")]

        # columns
        df = df.reset_index()
        df = df.rename(columns={"index": "kream_product_size"})
        df["updated_at"] = datetime.now().replace(microsecond=0)

        return pd.DataFrame(
            [KreamBuyAndSellSchema(**row).model_dump() for row in df.to_dict("records")]  # type: ignore
        )

    def get_temp_file_name(self) -> str:
        return "buy_and_sell"

    def get_save_file_name(self) -> str:
        return "buy_and_sell"


class PlatformPageDataConverter:
    def __init__(
        self,
        path: str,
        scrap_folder_name: str,
        file_name: str,
    ) -> None:
        self.scrap_folder_path = os.path.join(path, scrap_folder_name)
        self.file_name = file_name
        self.TempFile = ScrapTempFile(os.path.join(path, "_temp"))
        self._strategy = None

    @property
    def strategy(self):
        if not self._strategy:
            raise Exception("strategy is not set")
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: PlatformPageStrategy):
        self._strategy = strategy

    async def save_data(self):
        temp_file = await self.load_temp_file_data()
        preprocessed_df = self.strategy.preprocess(temp_file)
        self.save_to_parquet(preprocessed_df)
        return {"status": "success"}

    async def load_temp_file_data(self):
        temp_file_name = self.strategy.get_temp_file_name()
        file = await self.TempFile.load_temp_file(temp_file_name)
        return self._adaptor(file)

    def _adaptor(self, file) -> List[Dict]:
        if isinstance(file[0], List):
            return list(chain(*file))

        if isinstance(file[0], dict):
            return [f for f in file]

        raise Exception(f"invalid file type : {type(file)}")

    def save_to_parquet(self, df: pd.DataFrame):
        data_type = self.strategy.get_save_file_name()
        file_name = f"{self.file_name}-{data_type}.parquet.gzip"
        file_path = os.path.join(self.scrap_folder_path, file_name)
        return df.to_parquet(file_path, compression="gzip")
