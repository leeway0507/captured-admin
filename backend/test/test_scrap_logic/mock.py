from components.dev.utils.browser_controller import BrowserController, PageController
from components.dev.shop.page.candidate_extractor import (
    CandidateExtractor,
    SearchType,
    schema,
)
from typing import List, Any


class MockCandidateExtractor:
    async def extract_data(self, search_type: SearchType, value: str) -> List[schema]:
        ...


class MockBrowserController:
    @classmethod
    async def create(cls) -> "BrowserController":
        ...

    async def create_page_controller(self) -> PageController:
        ...

    async def load_cookies(self) -> None:
        ...

    async def close_browser(self) -> None:
        ...
