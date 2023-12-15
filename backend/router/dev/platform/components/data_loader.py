import pandas as pd
import os
from typing import Dict, List, Optional
from env import dev_env
from enum import Enum

default_path = "router/dev/kream/data/detail/"


def get_last_scrap_date(path: str) -> str:
    """가장 최근에 생성된 날짜를 이름을 가져온다."""
    file_names = os.listdir(path)
    file_names.sort()
    d = file_names[-1]
    return d.rsplit("-", 1)[0]


#####################


class LoadType(Enum):
    PRODUCT_CARD_LIST = ["product_card_list", dev_env.PLATFORM_PRODUCT_LIST_DIR]
    PRODUCT_DETAIL = ["product_detail", dev_env.PLATFORM_PRODUCT_PAGE_DIR]
    PRODUCT_BRIDGE = ["product_bridge", dev_env.PLATFORM_PRODUCT_PAGE_DIR]
    TRADING_VOLUME = ["trading_volume", dev_env.PLATFORM_PRODUCT_PAGE_DIR]
    BUY_AND_SELL = ["buy_and_sell", dev_env.PLATFORM_PRODUCT_PAGE_DIR]


def loader(
    type: LoadType,
    brand: str,
    scrap_date: Optional[str] = None,
    sample: int = 10,
):
    file_type, path = type.value
    if not scrap_date:
        scrap_date = get_last_scrap_date(path)
    data = load_file(path, brand, scrap_date, file_type)
    return template(data, sample)


def load_file(path, brand: str, scrap_date: str, type: str):
    file_name = f"{scrap_date}-{type}.parquet.gzip"
    file_path = os.path.join(path, brand, file_name)
    return pd.read_parquet(file_path).to_dict("records")


def template(data: List[Dict], sample: int):
    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {
        "len": len(kream_id_list),
        "kream_id_list": kream_id_list,
        "data": data[:sample],
    }
