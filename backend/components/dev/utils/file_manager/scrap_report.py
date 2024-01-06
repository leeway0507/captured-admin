import json
from typing import List, Dict
import aiofiles
from .scrap_temp_file import FileManager


# shop_product_card_list, shop_product_card_page 수집 결과 리포트를 생성, 불러오는 기능을 수행
import os
import json
from typing import Literal, List, Any, Optional, Dict
from env import get_path
from pydantic import BaseModel


class ScrapReportDataBase(BaseModel):
    scrap_time: str
    num_of_plan: int
    num_processor: int
    db_update: bool = False
    job: List


class ScrapReport:
    # ScrapTempFile is a singleton
    _instance = None

    def __init__(self, report_path: str) -> None:
        self.report_path = report_path
        self._report_file_name = ""
        self.report_file_path = ""

    @property
    def report_file_name(self):
        if not self._report_file_name:
            raise ValueError("self.report_name is not set.")
        return self._report_file_name

    @report_file_name.setter
    def report_file_name(self, value: str):
        self._report_file_name = value
        self.report_file_path = os.path.join(self.report_path, value + ".json")

    def __new__(cls, report_path: str):
        """싱글톤 패턴 적용"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._instance.report_path = report_path
        return cls._instance

    def get_report_list(self):
        file_list = os.listdir(self.report_path)
        file_list = [f.split(".json")[0] for f in file_list]
        file_list.sort(reverse=True)
        return file_list

    async def create_report_with_scrap_time_as_file_name(
        self,
        *_file_names,
        report_data: ScrapReportDataBase,
    ):
        FileManager.create_folder(self.report_path)

        file_name = report_data.scrap_time
        if _file_names:
            file_name += "-" + "-".join(_file_names)

        # if external_data:
        #     report_data.update(**external_data)

        save_report_file_path = os.path.join(self.report_path, file_name + ".json")
        return self._save_json(save_report_file_path, report_data.model_dump())

    def _save_json(self, path: str, data: dict):
        with open(path, "w") as f:
            f.write(json.dumps(data, indent=4, default=str, ensure_ascii=False))

    def load_report(self):
        file_path = self.report_file_path
        with open(file_path, "r") as f:
            scrap_result = json.load(f)

        return scrap_result

    def update_report(self, update_value: Dict):
        report = self.load_report()
        report.update(update_value)

        report_file_path = self.report_file_path
        self._save_json(report_file_path, report)

    def delete_report(self):
        file_path = self.report_file_path
        os.remove(file_path)
