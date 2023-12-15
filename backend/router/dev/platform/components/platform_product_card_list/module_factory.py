from typing import Protocol, List, Any
from bs4 import Tag
from playwright.async_api import Page


class PlatformListModule(Protocol):
    def __name__(self) -> str:
        ...

    def get_url(self, brand_name: str) -> str:
        ...

    def get_card_query(self) -> str:
        ...

    async def get_product_card_list(
        self, card_list: List[Tag], min_volume: int, min_wish: int
    ) -> List[Any]:
        ...


class PlatformListModuleFactory:
    def kream(self) -> PlatformListModule:
        ...

    def stockX(self) -> PlatformListModule:
        ...


class PwPlatformListModuleFactory(PlatformListModuleFactory):
    def kream(self) -> PlatformListModule:
        from .module import PwKreamList

        return PwKreamList()
