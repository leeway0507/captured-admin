"""Kream Page Scrap Main"""
import os


from typing import List, Dict


from ...scraper import PlatformScraper, ScrapReportDataBase

from components.dev.utils.browser_controller import PageController

from .platform_page_data_converter import (
    PlatformPageDataConverter,
    PlatformPageStrategyFactory as fac,
)


class PageScrapReportData(ScrapReportDataBase):
    product_detail: List
    trading_volume: List
    buy_and_sell: List
    platform_type: str


class PlatformPageScraper(PlatformScraper):
    def __init__(
        self,
        path: str,
    ):
        super().__init__(
            temp_path=os.path.join(path, "_temp"),
            report_path=os.path.join(path, "_report"),
        )
        self.path = path

    # concrete_method
    def init_sub_scraper(self, page: PageController):
        return self.sub_scraper.late_binding(page)

    # concrete_method
    async def save_data_to_temp(self, data: dict):
        for data_type, card_data in data.items():
            await self.TempFile.append_temp_file(data_type, card_data)

    # concrete_method
    async def reopen_page(self):
        return await self.sub_scraper.reopen_new_page()

    # concrete_method
    def create_report_template(
        self, temp_scrap_status: List[Dict]
    ) -> ScrapReportDataBase:
        return PageScrapReportData(
            scrap_time=self.scrap_time,
            num_of_plan=len(temp_scrap_status),
            num_processor=self.num_processor,
            job=self._get_params_list(temp_scrap_status),
            product_detail=self._get_product_detail(temp_scrap_status),
            trading_volume=self._get_trading_volume(temp_scrap_status),
            buy_and_sell=self._get_buy_and_sell(temp_scrap_status),
            platform_type=self.platform_type,
        )

    def _get_params_list(self, temp_scrap_status: List):
        return [status["job"] for status in temp_scrap_status]

    def _get_product_detail(self, temp_scrap_status: List):
        return [status["status"]["product_detail"] for status in temp_scrap_status]

    def _get_trading_volume(self, temp_scrap_status: List):
        return [status["status"]["trading_volume"] for status in temp_scrap_status]

    def _get_buy_and_sell(self, temp_scrap_status: List):
        return [status["status"]["buy_and_sell"] for status in temp_scrap_status]

    # concrete_method
    async def save_scrap_data(self):
        self._create_scrap_folder()

        data_converter = PlatformPageDataConverter(
            self.path, self.scrap_folder_name, self.scrap_time
        )

        data_converter.strategy = fac.product_detail()
        await data_converter.save_data()

        data_converter.strategy = fac.product_bridge()
        await data_converter.save_data()

        data_converter.strategy = fac.trading_volume()
        await data_converter.save_data()

        data_converter.strategy = fac.buy_and_sell()
        await data_converter.save_data()

    def _create_scrap_folder(self):
        page_path = os.path.join(self.path, self.scrap_folder_name)
        self.TempFile.create_folder(page_path)
