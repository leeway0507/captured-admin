from typing import Protocol, List, Any, Dict, Tuple
from bs4 import Tag
import playwright.async_api as pw
import playwright.sync_api as spw
from .module import PwKreamPage


class PlatformPageModule(Protocol):
    def __name__(self) -> str:
        ...

    def get_url(self, platform_sku: str) -> str:
        ...

    async def get_product_detail(self, page: pw.Page, platform_sku) -> Dict[str, Any]:
        ...

    async def get_buy_and_sell(self, page, platform_sku) -> Dict[str, Any]:
        ...

    async def get_product_volume(
        self, page, platform_sku
    ) -> Tuple[str, List[List[str]]]:
        ...


class PlatformPageModuleFactory:
    def kream(self) -> PlatformPageModule:
        ...

    def stockX(self) -> PlatformPageModule:
        ...


class PwPlatformPageModuleFactory(PlatformPageModuleFactory):
    def kream(self) -> PwKreamPage:
        return PwKreamPage()
