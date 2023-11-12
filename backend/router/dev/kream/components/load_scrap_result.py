import pandas as pd
import os

default_path = "router/dev/kream/data/detail/"


def get_last_scrap_date(path: str) -> str:
    """가장 최근에 생성된 날짜를 이름을 가져온다."""
    file_names = os.listdir(path)
    file_names.sort()
    d = file_names[-1]
    return d.rsplit("-", 1)[0]


#####################


def get_last_scrap_kream_product_card_list(brand_name: str, sample: int = 10):
    path = f"router/dev/kream/data/brand/{brand_name}/"
    last_scrap_list = get_last_scrap_date(path)
    return get_kream_product_card_list(brand_name, last_scrap_list, sample)


def get_last_scrap_kream_product_card_detail(brand_name: str, sample: int = 10):
    path = default_path + brand_name + "/"
    last_scrap = get_last_scrap_date(path)
    return get_kream_product_card_detail(brand_name, last_scrap, sample)


def get_last_scrap_kream_product_bridge(brand_name: str, sample: int = 10):
    path = default_path + brand_name + "/"
    last_scrap = get_last_scrap_date(path)
    return get_kream_product_bridge(brand_name, last_scrap, sample)


def get_last_scrap_kream_trading_volume(brand_name: str, sample: int = 10):
    path = default_path + brand_name + "/"
    last_scrap = get_last_scrap_date(path)
    return get_kream_trading_volume(brand_name, last_scrap, sample)


def get_last_scrap_kream_buy_and_sell(brand_name: str, sample: int = 10):
    path = default_path + brand_name + "/"
    last_scrap = get_last_scrap_date(path)
    return get_kream_buy_and_sell(brand_name, last_scrap, sample)


#####################


def get_kream_product_card_list(brand_name: str, list_scrap_date: str, sample: int):
    path = f"router/dev/kream/data/brand/{brand_name}/"
    file_name = f"{list_scrap_date}-product_card_list.parquet.gzip"
    data = pd.read_parquet(path + file_name).to_dict("records")

    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len": len(kream_id_list), "kream_id_list": kream_id_list, "data": data[:sample]}


def get_kream_product_card_detail(brand_name: str, scrap_date: str, sample: int):
    path = default_path + brand_name + "/"
    file_name = f"{scrap_date}-product_detail.parquet.gzip"

    data = pd.read_parquet(path + file_name).to_dict(orient="records")

    # produt_id 제거
    for row in data:
        del row["product_id"]

    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len": len(kream_id_list), "kream_id_list": kream_id_list, "data": data[:sample]}


def get_kream_product_bridge(brand_name: str, scrap_date: str, sample: int):
    path = default_path + brand_name + "/"
    file_name = f"{scrap_date}-product_detail.parquet.gzip"

    product_detail = pd.read_parquet(path + file_name)
    data = product_detail[["kream_id", "product_id"]].to_dict(orient="records")

    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len": len(kream_id_list), "kream_id_list": kream_id_list, "data": data[:sample]}


def get_kream_trading_volume(brand_name: str, scrap_date: str, sample: int):
    path = default_path + brand_name + "/"
    file_name = f"{scrap_date}-trading_volume.parquet.gzip"
    data = pd.read_parquet(path + file_name).to_dict(orient="records")

    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len": len(kream_id_list), "kream_id_list": kream_id_list, "data": data[:sample]}


def get_kream_buy_and_sell(brand_name: str, scrap_date: str, sample: int):
    path = default_path + brand_name + "/"
    file_name = f"{scrap_date}-buy_and_sell.parquet.gzip"
    data = pd.read_parquet(path + file_name).to_dict(orient="records")

    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len": len(kream_id_list), "kream_id_list": kream_id_list, "data": data[:sample]}
