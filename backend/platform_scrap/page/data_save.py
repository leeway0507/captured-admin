import os
from components.abstract_class.data_save import DataSave

from .platform_page_data_converter import (
    PlatformPageDataConverter,
    PlatformPageStrategyFactory as fac,
)


class PlatformPageDataSave(DataSave):
    def __init__(self, path: str):
        super().__init__(path)
        self._folder_name = None

    @property
    def folder_name(self):
        if not self._folder_name:
            raise ValueError("floder_name is not set")
        return self._folder_name

    @folder_name.setter
    def folder_name(self, folder_name):
        self._folder_name = folder_name

    async def init_config(self):
        self.check_folder_name_exist()
        config = await self.load_scrap_config()

        self.platform_type = config["platform"]
        self.scrap_time = config["scrap_time"]

        self.data_converter = PlatformPageDataConverter(
            self.path, self.folder_name, self.scrap_time
        )

    def check_folder_name_exist(self):
        return self.folder_name

    def folder_path(self):
        return os.path.join(self.path, self.folder_name)

    def file_path(self):
        file_name = self.scrap_time + ".parquet.gzip"
        file_path = os.path.join(self.folder_path(), file_name)
        return file_path

    async def save_scrap_data(self):
        await self.init_config()
        self.create_folder()

        await self.save_product_detail()
        await self.save_product_bridge()
        await self.save_trading_volume()
        await self.save_buy_and_sell()

    async def save_product_detail(self):
        self.data_converter.strategy = fac.product_detail()
        await self.data_converter.save_data()

    async def save_product_bridge(self):
        self.data_converter.strategy = fac.product_bridge()
        await self.data_converter.save_data()

    async def save_trading_volume(self):
        self.data_converter.strategy = fac.trading_volume()
        await self.data_converter.save_data()

    async def save_buy_and_sell(self) -> None:
        self.data_converter.strategy = fac.buy_and_sell()
        await self.data_converter.save_data()
