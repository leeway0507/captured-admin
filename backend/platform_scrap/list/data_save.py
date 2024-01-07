import os
from components.abstract_class.data_save import DataSave


class PlatformListDataSave(DataSave):
    def __init__(self, path: str):
        super().__init__(path)

    async def init_config(self):
        config = await self.load_scrap_config()

        self.platform_type = config["platform"]
        self.scrap_time = config["scrap_time"]

    def folder_path(self):
        return os.path.join(self.path, self.platform_type)

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
        self._save_parquet(self.file_path(), list_data)
