import pandas as pd
import os
from dotenv import dotenv_values

config = dotenv_values(".env.dev")

list_path = config["SHOP_PRODUCT_LIST_DIR"]
assert list_path, "SHOP_PRODUCT_LIST_DIR is None"


def get_last_scrap_date(path: str) -> str:
    """가장 최근에 생성된 날짜를 이름을 가져온다."""
    file_names = os.listdir(path)
    file_names.sort()
    d = file_names[-1]
    return d.split(".parquet")[0]


#####################


def get_last_scrap_product_dict(shop_name: str):
    path = list_path + shop_name + "/"
    last_scrap = get_last_scrap_date(path)
    return get_scrap_product_dict(shop_name, last_scrap)


#####################


def get_scrap_product_dict(shop_name: str, scrap_date: str):
    path = list_path + shop_name + "/"
    file_name = f"{scrap_date}.parquet.gzip"
    data = pd.read_parquet(path + file_name).to_dict(orient="records")

    product_id_list = list(set(map(lambda x: x.get("product_id"), data)))
    return {
        "len": len(data),
        "product_id_list": product_id_list,
        "data": data,
    }


page_path = config["SHOP_PRODUCT_PAGE_DIR"]
assert page_path, "SHOP_PRODUCT_PAGE_DIR is None"


def get_last_scrap_size_dict():
    path = page_path
    last_scrap = get_last_scrap_date(path)
    return get_scrap_size_dict(last_scrap)


def get_scrap_size_dict(scrap_date: str):
    df = pd.read_parquet(page_path + scrap_date + "-size" + ".parquet.gzip")

    return {
        "len": len(df),
        "data": df.to_dict("records"),
        "unique_id": df["shop_product_card_id"].unique().tolist(),
    }


def get_scrap_size_product_id_dict(scrap_date: str):
    df = pd.read_parquet(page_path + scrap_date + "-product-id" + ".parquet.gzip")

    ## update_product_id_by_shop_product_card_id 매서드에 맞추기 위해 이름을 key, value로 변경
    df.rename(
        columns={"shop_product_card_id": "key", "product_id": "value"}, inplace=True
    )

    return {
        "len": len(df),
        "data": df.to_dict("records"),
        "unique_id": df["key"].unique().tolist(),
    }
