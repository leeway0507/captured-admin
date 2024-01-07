import os
from typing import List
from components.file_manager import ScrapReportDataBase
from components.abstract_class.report import PlatformReport


class PageScrapReportData(ScrapReportDataBase):
    product_detail: List
    trading_volume: List
    buy_and_sell: List
    platform_type: str


class PlatformPageReport(PlatformReport):
    ## self.save_report()

    async def create_report_template(self) -> ScrapReportDataBase:
        scrap_config = await self.load_scrap_config()
        scrap_status = await self.load_scrap_status()

        return PageScrapReportData(
            scrap_time=scrap_config["scrap_time"],
            num_of_plan=len(scrap_status),
            num_processor=scrap_config["num_processor"],
            job=self._get_params_list(scrap_status),
            product_detail=self._get_product_detail(scrap_status),
            trading_volume=self._get_trading_volume(scrap_status),
            buy_and_sell=self._get_buy_and_sell(scrap_status),
            platform_type=scrap_config["platform"],
        )

    def _get_params_list(self, scrap_status: List):
        return [status["job"] for status in scrap_status]

    def _get_product_detail(self, scrap_status: List):
        return [status["status"]["product_detail"] for status in scrap_status]

    def _get_trading_volume(self, scrap_status: List):
        return [status["status"]["trading_volume"] for status in scrap_status]

    def _get_buy_and_sell(self, scrap_status: List):
        return [status["status"]["buy_and_sell"] for status in scrap_status]
