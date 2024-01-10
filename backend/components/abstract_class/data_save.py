import os
from typing import List, Dict
from abc import ABC, abstractmethod

import pandas as pd

from components.file_manager import ScrapTempFile


class DataSave(ABC):
    def __init__(self, path: str):
        self.path = path
        self.TempFile = ScrapTempFile(os.path.join(path, "_temp"))

    async def load_scrap_config(self) -> Dict:
        return await self.TempFile.load_temp_file("scrap_config")

    @abstractmethod
    async def init_config(self):
        ...

    @abstractmethod
    def folder_path(self) -> str:
        ...

    @abstractmethod
    def file_path(self) -> str:
        ...

    def _save_parquet(self, path: str, data: List):
        pd.DataFrame(data).drop_duplicates().to_parquet(path=path, compression="gzip")
        return True

    def create_folder(self):
        return self.TempFile.create_folder(self.folder_path())

    def _adaptor(self, file) -> List[Dict]:
        if isinstance(file, dict):
            return [file]

        if isinstance(file[0], List):
            from itertools import chain

            return list(chain(*file))

        if isinstance(file[0], dict):
            return [f for f in file]

        raise Exception(f"list_data type is not Dict or List: {type(file)}")
