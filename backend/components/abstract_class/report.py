import os
from typing import List, Dict, Tuple
from components.file_manager import ScrapReport, ScrapReportDataBase, ScrapTempFile
from abc import ABC, abstractmethod


class PlatformReport(ABC):
    def __init__(self, path):
        self.path = path
        self.TempFile = ScrapTempFile(os.path.join(path, "_temp"))
        self.Report = ScrapReport(os.path.join(path, "_report"))

    # concrete_method

    async def load_scrap_config(self) -> Dict:
        return await self.TempFile.load_temp_file("scrap_config")

    async def load_scrap_status(self) -> List:
        temp_file = await self.TempFile.load_temp_file("scrap_status")
        if isinstance(temp_file, tuple):
            return list(temp_file)

        if isinstance(temp_file, dict):
            return [temp_file]

        raise Exception(
            f"tempfile should be tuple or dict. current : {type(temp_file)}"
        )

    @abstractmethod
    async def create_report_template(self) -> ScrapReportDataBase:
        ...

    async def save_report(self):
        template = await self.create_report_template()

        self.Report.report_file_name = template.scrap_time

        await self.Report.create_report_with_scrap_time_as_file_name(
            report_data=template
        )
