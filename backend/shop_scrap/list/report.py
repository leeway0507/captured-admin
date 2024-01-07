from components.file_manager import ScrapReportDataBase
from components.abstract_class.report import PlatformReport


class ShopListReportData(ScrapReportDataBase):
    brand_name: str
    shop_name: str


class ShopListReport(PlatformReport):
    ## self.save_report()

    async def create_report_template(self) -> ScrapReportDataBase:
        scrap_config = await self.load_scrap_config()
        scrap_status = await self.load_scrap_status()

        return ShopListReportData(
            scrap_time=scrap_config["scrap_time"],
            num_of_plan=scrap_config["num_of_plan"],
            num_processor=scrap_config["num_processor"],
            shop_name=scrap_config["shop_name"],
            brand_name=scrap_config["brand_name"],
            job=list(scrap_status),
        )
