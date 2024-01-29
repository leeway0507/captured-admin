import os
import json
from typing import Dict, List

from env import dev_env

from .page.sub_scraper_factory import ShopPageSubScraperFactory
from .list.sub_scraper_factory import ShopListSubScraperFactory


def get_scrapable_page_module_list():
    method_list = [m for m in dir(ShopPageSubScraperFactory) if not m.startswith("__")]
    return method_list


def get_scrapable_list_module_list():
    method_list = [m for m in dir(ShopListSubScraperFactory) if not m.startswith("__")]
    return method_list


def get_brand_name(shop_name: str) -> List:
    brand_dict = _load_brand(shop_name)
    brand_list = brand_dict.get("brand_list")
    assert isinstance(brand_list, list), f"{shop_name}'s brand_list is None"
    return brand_list


def _load_brand(shop_name: str) -> Dict:
    path = dev_env.SHOP_LIST_DIR
    file_path = os.path.join(path, shop_name, "brand_list.json")

    # TODO: shop 별 브랜드 리스트를 만들어야함.
    with open(file_path, "r") as f:
        brand_dict = json.load(f)
    return brand_dict