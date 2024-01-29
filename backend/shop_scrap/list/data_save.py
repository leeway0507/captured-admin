from typing import List, Dict
from datetime import datetime
import os

import pandas as pd

from components.abstract_class.data_save import DataSave
from components.currency import Currency
from model.db_model_shop import ShopProductCardSchema


class ShopListDataSave(DataSave):
    def __init__(self, path: str):
        super().__init__(path)
        self.currency = Currency()

    async def init_config(self):
        config = await self.load_scrap_config()

        self.shop_name = config["shop_name"]
        self.scrap_time = config["scrap_time"]

    def folder_path(self):
        return os.path.join(self.path, self.shop_name)

    def file_path(self):
        file_name = self.scrap_time + ".parquet.gzip"
        file_path = os.path.join(self.folder_path(), file_name)
        return file_path

    async def load_scrap_data(self):
        return await self.TempFile.load_temp_file("product_card_list")

    async def save_scrap_data(self):
        await self.init_config()
        self.create_folder()
        list_data = await self.load_scrap_data()
        preprocessed_data = self.preprocess_data(list_data)
        self.save_preprocessed_data(preprocessed_data)

    def preprocess_data(self, list_data: List[Dict]) -> List[Dict]:
        list_data = self._adaptor(list_data)

        # currency
        lst = []
        for card in list_data:
            price = card["price"]

            _, curr_name, origin_price = self.currency.get_price_info(price)

            (_, _, us_price) = self.currency.change_currency_to_custom_usd(price)

            (_, _, kor_price) = self.currency.change_currency_to_buying_won(price)

            lst.append(
                ShopProductCardSchema(
                    original_price_currency=curr_name,
                    original_price=origin_price,
                    us_price=us_price,
                    kor_price=int(round(kor_price, -3)),
                    updated_at=datetime.now().replace(microsecond=0),
                    **card,
                )
            )

        return self._drop_duplicates_preprocess_data(lst)

    def _adaptor(self, list_data) -> List:
        if isinstance(list_data, tuple):
            """
            여러 브랜드 수집 시 list_data type은 tuple임.
            브랜드 하나 수집 시 list_data type은 list임.
            """
            from itertools import chain

            list_data = list(chain(*list_data))

        return list_data

    def _drop_duplicates_preprocess_data(self, list_data: List[ShopProductCardSchema]):
        serialized_data = [data.model_dump() for data in list_data]
        return pd.DataFrame(serialized_data).drop_duplicates().to_dict("records")

    def save_preprocessed_data(self, data: List[Dict]):
        file_path = os.path.join(self.folder_path(), f"{self.scrap_time}.parquet.gzip")

        self._save_parquet(file_path, data)
