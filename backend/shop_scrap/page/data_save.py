from typing import List, Dict
from datetime import datetime
import os

from components.abstract_class.data_save import DataSave
from model.db_model_shop import ShopProductSizeSchema
from ..utils.size_converter import convert_size
from components.currency import Currency


class ShopPageData(ShopProductSizeSchema):
    product_id: str
    original_price: str
    available: bool = True


class ShopPageDataSave(DataSave):
    def __init__(self, path: str):
        super().__init__(path)

        self.currency = Currency()

    def folder_path(self):
        return os.path.join(self.path, self.scrap_time)

    def file_path(self):
        file_name = self.scrap_time + ".parquet.gzip"
        file_path = os.path.join(self.folder_path(), file_name)
        return file_path

    async def save_scrap_data(self):
        await self.init_config()
        super().create_folder()
        scrap_data = await self.load_scrap_data()
        preprocessed_data = self.filter_data(scrap_data)
        self.save_preprocessed_data(preprocessed_data)

    async def init_config(self):
        config = await super().load_scrap_config()
        self.scrap_time = config["scrap_time"]

    async def load_scrap_data(self):
        return await self.TempFile.load_temp_file("product_card_page")

    def filter_data(self, scrap_data: List[Dict]) -> List[Dict]:
        update_time = datetime.now().replace(microsecond=0)
        scrap_data = super()._adaptor(scrap_data)

        lst = []
        for card in scrap_data:
            for size in card["size"]:
                lst.append(
                    ShopPageData(
                        shop_product_size=size["shop_product_size"],
                        kor_product_size=str(convert_size(size["kor_product_size"])),
                        shop_product_card_id=card["shop_product_card_id"],
                        product_id=card["card_info"]["product_id"],
                        original_price=card["card_info"]["original_price"],
                        updated_at=update_time,
                    ).model_dump()
                )

        return lst

    def save_preprocessed_data(self, list_data: List[Dict]):
        folder_path = self.folder_path()

        size_path = os.path.join(folder_path, f"shop_scrap_page_size_data.parquet.gzip")
        self._save_size_data_to_parquet(size_path, list_data)

        card_info_path = os.path.join(
            folder_path, f"shop_scrap_page_card_data.parquet.gzip"
        )
        self._save_card_info_data_to_parquet(card_info_path, list_data)

    def _save_size_data_to_parquet(self, file_path: str, list_data: List[Dict]):
        size_schema = [ShopPageData(**row).model_dump() for row in list_data]
        self._save_parquet(file_path, size_schema)

    def _save_card_info_data_to_parquet(self, file_path: str, list_data: List[Dict]):
        product_id_Schema = {}
        for row in list_data:
            key = row["shop_product_card_id"]
            product_id = row["product_id"]
            if product_id not in product_id_Schema.values():
                product_id_Schema[key] = {
                    "product_id": row["product_id"],
                    "original_price": row["original_price"],
                    "updated_at": row["updated_at"],
                }

        l = []
        for k, values in product_id_Schema.items():
            price_info = self._get_price_info(values["original_price"])
            l.append(
                {
                    "shop_product_card_id": k,
                    "product_id": values["product_id"],
                    "updated_at": values["updated_at"],
                    **price_info,
                }
            )

        self._save_parquet(file_path, l)

    def _get_price_info(self, price: str):
        _, curr_name, origin_price = self.currency.get_price_info(price)
        (_, _, us_price) = self.currency.change_currency_to_custom_usd(price)
        (_, _, kor_price) = self.currency.change_currency_to_buying_won(price)

        return {
            "original_price_currency": curr_name,
            "original_price": origin_price,
            "us_price": us_price,
            "kor_price": int(round(kor_price, -3)),
        }
