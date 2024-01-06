from typing import Any, Dict, List, Protocol
import playwright.async_api as pw
from ..shop_list.consortium import PwConsortiumPageSubScraper
from ..shop_list.seven_store import PwSevenStorePage
from ..shop_list.a_few_store import PwAfewStorePage


class ShopPageModule(Protocol):
    def __name__(self) -> str:
        ...

    def get_cookie_button_xpath(self) -> List[str]:
        ...

    async def get_size_info(self, page) -> List[Dict[str, Any]]:
        ...

    async def get_product_id(self, page) -> str:
        ...


class PlayWrightShopPageModule(Protocol):
    def __name__(self) -> str:
        ...

    def get_cookie_button_xpath(self) -> List[str]:
        ...

    async def get_size_info(self, page: pw.Page) -> List[Dict[str, Any]]:
        ...

    async def get_product_id(self, page: pw.Page) -> str:
        ...


class SeleniumPageModule(Protocol):
    def __name__(self) -> str:
        ...

    def get_cookie_button_xpath(self) -> List[str]:
        ...

    async def get_size_info(self, page) -> List[Dict[str, Any]]:
        """page Type  : selenium web driver"""
        ...

    async def get_product_id(self, page) -> str:
        """page Type  : selenium web driver"""
        ...


class ShopPageSubScraperFactory:
    def consortium(self) -> ShopPageModule:
        ...

    def seven_store(self) -> ShopPageModule:
        ...

    def a_few_store(self) -> ShopPageModule:
        ...


class PwShopPageSubScraperFactory(ShopPageSubScraperFactory):
    def consortium(self) -> "PwConsortiumPageSubScraper":
        return PwConsortiumPageSubScraper()

    # def seven_store(self) -> PwSevenStorePage:
    #     return PwSevenStorePage()

    # def a_few_store(self) -> PwAfewStorePage:
    #     return PwAfewStorePage()


# class SePageModuleFactory(ShopPageModuleFactory):
#     async def consortium(self) -> SeleniumPageModule:
#         return SeConsortiumPage()
