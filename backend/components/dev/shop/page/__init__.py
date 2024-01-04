"""Shop Product Card Page Main"""

import os

from datetime import datetime
from typing import List, Dict

from model.db_model_shop import ShopProductSizeSchema

from components.dev.scraper import ShopScraper
from components.dev.utils.browser_controller import BrowserController
from components.dev.sub_scraper import SubScraper
from components.dev.shop.size_converter import convert_size


class ShopPageData(ShopProductSizeSchema):
    product_id: str
    available: bool = True


class ShopPageScraper(ShopScraper):
    def __init__(
        self,
        num_processor: int,
        path: str,
        browser_controller: BrowserController,
        sub_scraper: SubScraper,
        shop_name: str,
        scrap_type: str = "product_card_page",
    ):
        super().__init__(
            path,
            browser_controller,
            num_processor,
            sub_scraper,
            scrap_type,
            shop_name,
        )

    def preprocess_data(self, list_data: List[Dict]) -> List[Dict]:
        update_time = datetime.now().replace(microsecond=0)
        list_data = self._adaptor(list_data)

        lst = []
        for card in list_data:
            for size in card["size"]:
                lst.append(
                    ShopPageData(
                        shop_product_size=size["shop_product_size"],
                        kor_product_size=str(convert_size(size["kor_product_size"])),
                        shop_product_card_id=card["shop_product_card_id"],
                        product_id=card["product_id"],
                        updated_at=update_time,
                    ).model_dump()
                )

        return lst

    def _adaptor(self, list_data) -> List:
        if isinstance(list_data, tuple):
            """
            여러 브랜드 수집 시 list_data type은 tuple임.
            브랜드 하나 수집 시 list_data type은 list임.
            """
            from itertools import chain

            list_data = list(chain(*list_data))

        if isinstance(list_data, Dict):
            return [list_data]

        if isinstance(list_data, List):
            return list_data

        raise Exception(f"list_data type is not Dict or List: {type(list_data)}")

    def save_preprocessed_data(self, list_data: List[Dict]):
        folder_path = self._generate_shop_folder_path()

        size_path = os.path.join(folder_path, f"{self.scrap_time}-size.parquet.gzip")
        self._save_size_data_to_parquet(size_path, list_data)
        prodct_id_path = os.path.join(
            folder_path, f"{self.scrap_time}-product-id.parquet.gzip"
        )
        self._save_product_id_data_to_parquet(prodct_id_path, list_data)

    def _save_size_data_to_parquet(self, file_path: str, list_data: List[Dict]):
        size_schema = [ShopPageData(**row).model_dump() for row in list_data]
        self._save_parquet(file_path, size_schema)

    def _save_product_id_data_to_parquet(self, file_path: str, list_data: List[Dict]):
        product_id_Schema = {}
        for row in list_data:
            key = row["shop_product_card_id"]
            value = row["product_id"]
            if value not in product_id_Schema.values():
                product_id_Schema[key] = value

        l = []
        for k, v in product_id_Schema.items():
            l.append(
                {
                    "shop_product_card_id": k,
                    "product_id": v,
                }
            )

        self._save_parquet(file_path, l)
