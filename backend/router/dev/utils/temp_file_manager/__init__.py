import os
import json
from typing import List, Dict, Literal
from itertools import chain
from env import get_path
import aiofiles


class TempFileManager:
    _instances = {}

    def __init__(
        self,
        scrap_type: Literal[
            "shop_page",
            "shop_list",
            "platform_page",
            "platform_list",
        ],
    ):
        self.scrap_type = scrap_type
        self.path = get_path(scrap_type)
        self.temp_path = os.path.join(self.path, "_temp/")

    def __new__(cls, scrap_type: str):
        if scrap_type not in cls._instances:
            instance = super().__new__(cls)
            instance.scrap_type = scrap_type
            cls._instances[scrap_type] = instance
        return cls._instances[scrap_type]

    async def load_temp_file(self, file_name: str):
        file_path = os.path.join(self.temp_path, file_name + ".json")

        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            v = await f.read()
            v = (
                v.replace("null", "None")
                .replace("true", "True")
                .replace("false", "False")
            )
            if v.endswith(","):
                v = v[:-1]
            v = eval(v)
            # return list(chain(*v))
            return v

    def init_temp_file(self):
        file_list = os.listdir(self.temp_path)
        for file in file_list:
            with open(self.temp_path + file, "w") as f:
                f.write("")

    async def save_temp_file(self, file_name: str, data: List | Dict):
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path, exist_ok=True)

        file_path = os.path.join(self.temp_path, file_name + ".json")
        async with aiofiles.open(file_path, "a") as f:
            await f.write(json.dumps(data, ensure_ascii=False, default=str) + ",")
