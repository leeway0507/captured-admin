import pandas as pd
import os
from dotenv import dotenv_values

config = dotenv_values(".env.dev")

default_path = config["SHOP_PRODUCT_CARD_LIST_DIR"]
assert default_path, "SHOP_PRODUCT_CARD_LIST_DIR is None"


def get_last_scrap_date(path: str) -> str:
    """가장 최근에 생성된 날짜를 이름을 가져온다."""
    file_names = os.listdir(path)
    file_names.sort()
    d = file_names[-1]
    return d.split(".parquet")[0]


#####################


def get_last_scrap_product_dict(shop_name: str):
    path = default_path + shop_name + "/"
    last_scrap = get_last_scrap_date(path)
    return get_scrap_product_dict(shop_name, last_scrap)


#####################


def get_scrap_product_dict(shop_name: str, scrap_date: str):
    path = default_path + shop_name + "/"
    file_name = f"{scrap_date}.parquet.gzip"
    data = pd.read_parquet(path + file_name).to_dict(orient="records")

    product_id_list = list(set(map(lambda x: x.get("product_id"), data)))
    return {
        "len": len(data),
        "product_id_list": product_id_list,
        "data": data,
    }
