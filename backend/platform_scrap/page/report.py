import os
from typing import List, Dict
from components.file_manager import ScrapReportDataBase
from components.abstract_class.report import PlatformReport


class PageScrapReportData(ScrapReportDataBase):
    product_detail: List
    trading_volume: List
    buy_and_sell: List
    platform_type: str
    folder_name: str


class PlatformPageReport(PlatformReport):
    def __init__(self, path):
        super().__init__(path)
        self._folder_name = None

    @property
    def folder_name(self):
        if self._folder_name:
            return self._folder_name
        raise (ValueError("folder Name is None"))

    @folder_name.setter
    def folder_name(self, folder_name: str):
        self._folder_name = folder_name

    async def create_report_template(self) -> ScrapReportDataBase:
        scrap_config = await self.load_scrap_config()
        scrap_status = await self.load_scrap_status()
        scrap_status = self.preprocess_scrap_status(scrap_status)

        return PageScrapReportData(
            scrap_time=scrap_config["scrap_time"],
            num_of_plan=len(scrap_status),
            num_processor=scrap_config["num_processor"],
            job=self._get_params_list(scrap_status),
            product_detail=self._get_product_detail(scrap_status),
            trading_volume=self._get_trading_volume(scrap_status),
            buy_and_sell=self._get_buy_and_sell(scrap_status),
            platform_type=scrap_config["platform"],
            folder_name=self.folder_name,
        )

    def preprocess_scrap_status(self, scrap_status: List[Dict]):
        preprocessed_scrap_status = []
        for status in scrap_status:
            try:
                if status["status"]["product_detail"]:
                    preprocessed_scrap_status.append(status)
            except:
                preprocessed_scrap_status.append(
                    {
                        "job": status["job"],
                        "status": {
                            "product_detail": "failed",
                            "buy_and_sell": "failed",
                            "trading_volume": "failed",
                        },
                    }
                )
        return preprocessed_scrap_status

    def _get_params_list(self, scrap_status: List):
        return [status["job"] for status in scrap_status]

    def _get_product_detail(self, scrap_status: List):
        return [status["status"]["product_detail"] for status in scrap_status]

    def _get_trading_volume(self, scrap_status: List):
        return [status["status"]["trading_volume"] for status in scrap_status]

    def _get_buy_and_sell(self, scrap_status: List):
        return [status["status"]["buy_and_sell"] for status in scrap_status]
