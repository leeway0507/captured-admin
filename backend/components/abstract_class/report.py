import os
from typing import List, Dict, Tuple
from components.file_manager import ScrapReport, ScrapReportDataBase, ScrapTempFile
from abc import ABC, abstractmethod


class PlatformReport(ScrapReport):
    def __init__(self, path):
        self.path = path
        super().__init__(report_path=os.path.join(path, "_report"))
        self.TempFile = ScrapTempFile(os.path.join(path, "_temp"))

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

        self.report_file_name = template.scrap_time

        await super().create_report_with_scrap_time_as_file_name(report_data=template)
        return template.scrap_time
