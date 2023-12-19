from typing import List, Protocol
from playwright.async_api import Page
from bs4 import Tag


from .schema import ListConfig, ListScrapData


class ShopListModule(Protocol):
    def __name__(self) -> str:
        ...

    def config(self) -> ListConfig:
        ...

    def get_url(self, brand_name) -> str:
        ...

    async def extract_card_html(self, page) -> List[Tag] | None:
        ...

    def extract_info(self, card: Tag, brand_name: str) -> ListScrapData:
        ...

    async def get_next_page(self, page, page_num: int) -> bool:
        ...


class PlayWrightShopListModule(Protocol):
    def __name__(self) -> str:
        ...

    def config(self) -> ListConfig:
        ...

    def get_url(self, brand_name) -> str:
        ...

    async def extract_card_html(self, page) -> List[Tag] | None:
        ...

    def extract_info(self, card: Tag, brand_name: str) -> ListScrapData:
        ...

    async def get_next_page(self, page: Page, page_num: int) -> bool:
        ...


class SeleniumListModule(Protocol):
    def __name__(self) -> str:
        ...

    def config(self) -> ListConfig:
        ...

    def get_url(self, brand_name) -> str:
        ...

    async def extract_card_html(self, page) -> List[Tag] | None:
        ...

    def extract_info(self, card: Tag, brand_name: str) -> ListScrapData:
        ...

    async def get_next_page(self, page, page_num: int) -> bool:
        ...


### FACTORY ###


class ShopListModuleFactory:
    def consortium(self) -> ShopListModule:
        ...

    def seven_store(self) -> ShopListModule:
        ...

    def a_few_store(self) -> ShopListModule:
        ...


class PwShopListModuleFactory(ShopListModuleFactory):
    def consortium(self) -> PlayWrightShopListModule:
        from ..shop_list.consortium import PwConsortiumList

        return PwConsortiumList()

    def seven_store(self) -> PlayWrightShopListModule:
        from ..shop_list.seven_store import PwSevenStoreList

        return PwSevenStoreList()

    def a_few_store(self) -> PlayWrightShopListModule:
        from ..shop_list.a_few_store import PwAfewStoreList

        return PwAfewStoreList()


# class SePageModuleFactory(ShopPageModuleFactory):
#     async def consortium(self) -> SeleniumPageModule:
#         return SeConsortiumPage()
