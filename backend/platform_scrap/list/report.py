from components.file_manager import ScrapReportDataBase
from components.abstract_class.report import PlatformReport


class PlatformListReportData(ScrapReportDataBase):
    brand_name: str
    platform_type: str


class PlatformListReport(PlatformReport):
    ## self.save_report()

    async def create_report_template(self) -> ScrapReportDataBase:
        scrap_config = await super().load_scrap_config()
        scrap_status = await super().load_scrap_status()

        return PlatformListReportData(
            scrap_time=scrap_config["scrap_time"],
            num_of_plan=scrap_config["num_of_plan"],
            num_processor=scrap_config["num_processor"],
            platform_type=scrap_config["platform"],
            brand_name=scrap_config["brand_name"],
            job=list(scrap_status),
        )
