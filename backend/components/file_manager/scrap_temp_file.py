import json
from typing import List, Dict
import aiofiles
from .file_manager import FileManager


class ScrapTempFile(FileManager):
    _instance = None

    def __init__(self, temp_path: str):
        super().__init__(temp_path)

    def __new__(cls, temp_path: str):
        """싱글톤 패턴 적용"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._instance.path = temp_path  # Initialize context to None
        return cls._instance

    async def append_temp_file(self, file_name: str, data: List | Dict):
        """임시 파일 스택으로 쌓기"""
        self.create_folder(self.path)
        file_path = super()._get_file_path(file_name)

        async with aiofiles.open(file_path, "a") as f:
            await f.write(json.dumps(data, ensure_ascii=False, default=str) + ",")

    async def load_temp_file(self, file_name: str):
        """임시 파일 로드"""
        temp_file_path = super()._get_file_path(file_name)

        async with aiofiles.open(temp_file_path, "r", encoding="utf-8") as f:
            json_style_text = await f.read()
            json_file = self._convert_to_json(json_style_text)
            return json_file

    def _convert_to_json(self, json_text: str):
        json_text = (
            json_text.replace("null", "None")
            .replace("true", "True")
            .replace("false", "False")
        )
        if json_text.endswith(","):
            json_text = json_text[:-1]
        return eval(json_text)
