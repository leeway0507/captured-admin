from typing import List, Protocol
from playwright.async_api import Page
from bs4 import Tag

from components.dev.shop.list.sub_scraper import (
    PwShopListSubScraper,
    ListScrapData,
)


### FACTORY ###


class ShopListSubScraperFactory:
    def consortium(self) -> PwShopListSubScraper:
        ...

    def seven_store(self) -> PwShopListSubScraper:
        ...

    def a_few_store(self) -> PwShopListSubScraper:
        ...


class PwShopListSubScraperFactory(ShopListSubScraperFactory):
    def consortium(self) -> PwShopListSubScraper:
        from ..shop_list.consortium import PwConsortiumListSubScraper

        return PwConsortiumListSubScraper()

    # def seven_store(self) -> PwShopListSubScraper:
    #     from ..shop_list.seven_store import PwSevenStoreList

    #     return PwSevenStoreList()

    # def a_few_store(self) -> PwShopListSubScraper:
    #     from ..shop_list.a_few_store import PwAfewStoreList

    #     return PwAfewStoreList()


# class SePageModuleFactory(ShopPageModuleFactory):
#     async def consortium(self) -> SeleniumPageModule:
#         return SeConsortiumPage()
