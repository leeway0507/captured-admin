import os
from typing import List, Dict, Any
import json
from playwright.async_api import Page


from bs4 import Tag
from env import dev_env
from abc import ABC, abstractmethod


class PwShopList(ABC):
    def __init__(self):
        self.brand_list: List[Dict] = self._load_brand_list()["data"]

    @abstractmethod
    def __name__(self) -> str:
        ...

    def _load_brand_list(self):
        path = os.path.join(dev_env.SHOP_LIST_DIR, self.__name__(), "brand_list.json")
        with open(path) as f:
            return json.load(f)

    def get_url(self, brand_name) -> str:
        for brand in self.brand_list:
            if brand["brand_name"] == brand_name:
                return brand["brand_url"]

        raise Exception(f"brand_name: {brand_name} not found")


class PwShopPage(ABC):
    def __init__(self):
        self.brand_list: List[Dict] = self._load_brand_list()["data"]

    @abstractmethod
    def __name__(self) -> str:
        ...

    def _load_brand_list(self):
        path = os.path.join(dev_env.SHOP_LIST_DIR, self.__name__(), "brand_list.json")
        with open(path) as f:
            return json.load(f)

    def get_url(self, brand_name) -> str:
        for brand in self.brand_list:
            if brand["brand_name"] == brand_name:
                return brand["brand_url"]

        raise Exception(f"brand_name: {brand_name} not found")

    @abstractmethod
    def get_cookie_button_xpath(self) -> List[str]:
        ...

    @abstractmethod
    async def get_size_info(self, page: Page) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    async def get_product_id(self, page: Page) -> str:
        ...
