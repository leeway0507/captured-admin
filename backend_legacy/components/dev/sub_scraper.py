from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
from components.dev.utils.browser_controller import PageController as P


class SubScraper(ABC):
    def __init__(self):
        self._page_controller = None
        self._job = None

    @abstractmethod
    def __name__(self) -> str:
        pass

    @abstractmethod
    def late_binding(self, page_controller: P):
        pass

    def allocate_job(self, job: Any):
        self.job = job

    @abstractmethod
    async def execute() -> Tuple[str, Dict | List]:
        pass

    async def reopen_new_page(self):
        await self.page_controller.reopen_new_page()

    @property
    def page_controller(self):
        if not self._page_controller:
            raise ValueError("page_controller is None. Please update page_controller")

        return self._page_controller

    @page_controller.setter
    def page_controller(self, page_controller: P):
        self._page_controller = page_controller

    @property
    def job(self):
        if not self._job:
            raise ValueError("job is None. Please update job")
        return self._job

    @job.setter
    def job(self, job: str):
        self._job = job
