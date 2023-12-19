# shop_product_card_list, shop_product_card_page 수집 결과 리포트를 생성, 불러오는 기능을 수행
import os
import json
from typing import Literal, List, Any, Optional, Dict
from env import dev_env
from pydantic import BaseModel


class ScrapMeta(BaseModel):
    num_of_plan: int
    num_process: int
    scrap_log: List
    db_update: bool = False


def get_path(
    report_type: Literal["shop_page", "shop_list", "platform_page", "platform_list"]
):
    match report_type:
        case "shop_page":
            return dev_env.SHOP_PRODUCT_PAGE_DIR

        case "shop_list":
            return dev_env.SHOP_PRODUCT_LIST_DIR

        case "platform_page":
            return dev_env.PLATFORM_PRODUCT_PAGE_DIR

        case "platform_list":
            return dev_env.PLATFORM_PRODUCT_LIST_DIR


class ScrapReport:
    _instances = {}

    def __init__(
        self,
        report_type: Literal[
            "shop_page", "shop_list", "platform_page", "platform_list"
        ],
    ) -> None:
        self.report_type = report_type
        self.path = get_path(report_type)
        self.temp_path = self.path + "_temp/"
        self.report_path = self.path + "_report/"
        self._make_dir(self.temp_path)
        self._make_dir(self.report_path)

    def __new__(cls, report_type):
        if report_type not in cls._instances:
            instance = super().__new__(cls)
            instance.report_type = report_type
            cls._instances[report_type] = instance
        return cls._instances[report_type]

    def _make_dir(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    def get_report_list(self):
        file_list = os.listdir(self.report_path)
        file_list = [x.split(".json")[0] for x in file_list]
        file_list.sort(reverse=True)
        return file_list

    def save_temp_report(self, meta: ScrapMeta):
        with open(self.temp_path + "scrap_result.json", "w") as f:
            f.write(json.dumps(meta.model_dump(), ensure_ascii=False))

    def load_temp_json(self, file_name: str):
        file_path = os.path.join(self.temp_path, file_name)
        with open(file_path, "r") as f:
            return json.load(f)

    def load_temp_report(self, scrap_time: str):
        process_result = self.load_temp_json("scrap_result.json")
        return {"scrap_time": scrap_time, **process_result}

    def create_new_report(
        self, scrap_time: str, *_args, external_data: Optional[Dict] = None
    ):
        log = self.load_temp_report(scrap_time)

        if external_data:
            log.update(**external_data)

        if _args:
            file_name = scrap_time + "-" + "-".join(_args)
        else:
            file_name = scrap_time

        return self.save_report(file_name, log)

    def save_report(self, file_name: str, log: dict):
        with open(self.report_path + file_name + ".json", "w") as f:
            f.write(json.dumps(log, indent=4, default=str, ensure_ascii=False))

    def get_report(self, report_name: str):
        with open(self.report_path + report_name + ".json", "r") as f:
            scrap_result = json.load(f)

        return scrap_result

    def update_report(self, report_name: str, key: str, value: Any):
        with open(self.report_path + report_name + ".json", "r") as f:
            report = json.load(f)
            report[key] = value

        with open(self.report_path + report_name + ".json", "w") as f:
            f.write(json.dumps(report, default=str))

    def delete_report(self, report_name: str):
        if self.report_type == "page":
            return self._delete_page_report(report_name)

        if self.report_type == "list":
            return self._delete_list_report(report_name)

    def _delete_list_report(self, report_name: str):
        os.remove(self.report_path + report_name + ".json")

        # remove parquet file
        file_name, brand_name = report_name.rsplit("-", 1)
        os.remove(self.path + brand_name + "/" + file_name + ".parquet.gzip")

    def _delete_page_report(self, report_name: str):
        os.remove(self.report_path + report_name + ".json")

        # remove parquet file
        file_name, brand_name = report_name.rsplit("-", 1)
        os.remove(self.path + file_name + "-product-id" + ".parquet.gzip")
        os.remove(self.path + file_name + "-size" + ".parquet.gzip")
