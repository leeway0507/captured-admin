import os

from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
from pydantic import BaseModel


from model.db_model_shop import ShopProductCardSchema
from ..currency import Currency


from components.dev.scraper import ShopScraper


class ListScrapData(BaseModel):
    shop_name: str
    brand_name: str = ""
    shop_product_name: str
    shop_product_img_url: str
    product_url: str
    product_id: Optional[str] = None
    price: str


class PreProcessData(BaseModel):
    shop_product_size: str
    shop_product_card_id: int
    kor_product_size: str
    product_id: str
    available: bool = True
    updated_at: datetime


class ShopListScraper(ShopScraper):
    def __init__(
        self,
        path: str,
        scrap_type: str = "shop_card_list",
    ):
        super().__init__(
            path,
            scrap_type,
        )

    def preprocess_data(self, list_data: List[Dict]) -> List[Dict]:
        currency = Currency()
        list_data = self._adaptor(list_data)

        # currency
        lst = []
        for card in list_data:
            price = card["price"]

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
        folder_path = self._generate_shop_folder_path()
        file_path = os.path.join(folder_path, f"{self.scrap_time}.parquet.gzip")

        self._save_parquet(file_path, data)
