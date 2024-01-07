from typing import List
from components.file_manager import ScrapReportDataBase
from components.abstract_class.report import PlatformReport


class ShopListReportData(ScrapReportDataBase):
    shop_name: str


class ShopPageReport(PlatformReport):
    ## self.save_report()

    async def create_report_template(self) -> ScrapReportDataBase:
        scrap_config = await self.load_scrap_config()
        scrap_status = await self.preprocessed_scrap_status()

        return ShopListReportData(
            scrap_time=scrap_config["scrap_time"],
            num_of_plan=scrap_config["num_of_plan"],
            num_processor=scrap_config["num_processor"],
            shop_name=scrap_config["shop_name"],
            job=scrap_status,
        )

    async def preprocessed_scrap_status(self) -> List:
        scrap_status = await self.load_scrap_status()
        l = []
        for value in scrap_status:
            job, status = value.values()
            target_data = eval(job)
            l.append({**target_data, "status": status})
        return l
