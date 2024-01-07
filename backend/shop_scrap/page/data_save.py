from typing import List, Dict
from datetime import datetime
import os

from components.abstract_class.data_save import DataSave
from model.db_model_shop import ShopProductSizeSchema
from ..utils.size_converter import convert_size


class ShopPageData(ShopProductSizeSchema):
    product_id: str
    available: bool = True


class ShopPageDataSave(DataSave):
    def __init__(self, path: str):
        super().__init__(path)

    def folder_path(self):
        return os.path.join(self.path, self.shop_name)

    def file_path(self):
        file_name = self.scrap_time + ".parquet.gzip"
        file_path = os.path.join(self.folder_path(), file_name)
        return file_path

    async def save_scrap_data(self):
        await self.init_config()
        super().create_folder()
        list_data = await self.load_scrap_data()
        preprocessed_data = self.preprocess_data(list_data)
        self.save_preprocessed_data(preprocessed_data)

    async def init_config(self):
        config = await super().load_scrap_config()

        self.shop_name = config["shop_name"]
        self.scrap_time = config["scrap_time"]

    async def load_scrap_data(self):
        return await self.TempFile.load_temp_file("product_card_page")

    def preprocess_data(self, list_data: List[Dict]) -> List[Dict]:
        update_time = datetime.now().replace(microsecond=0)
        list_data = super()._adaptor(list_data)

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

    def save_preprocessed_data(self, list_data: List[Dict]):
        folder_path = self.folder_path()

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
