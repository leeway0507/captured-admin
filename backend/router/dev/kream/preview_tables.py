import pandas as pd
import os 
from model.db_model_kream import KreamProductCardSchema, KreamProductIdBridgeSchmea, KreamTradingVolumeSchema, KreamBuyAndSellSchema


def get_last_update_date(path: str) -> list:
    """가장 최근에 생성된 날짜를 이름을 가져온다."""
    file_names = os.listdir(path)
    file_names.sort()
    d = file_names[-1]
    return d.rsplit("-", 1)[0]

def get_kream_product_card(brand_name: str) :
    path = f"router/dev/kream/data/detail/{brand_name}/"
    last_update = get_last_update_date(path)
    file_name = f"{last_update}-product_detail.parquet.gzip"
    product_detail = pd.read_parquet(path + file_name)

    path = f"router/dev/kream/data/brand/{brand_name}/"
    last_update = get_last_update_date(path)
    file_name = f"{last_update}-product_card_list.parquet.gzip"
    product_card_list = pd.read_parquet(path + file_name)

    data = pd.merge(product_detail, product_card_list, on="kream_id", how="inner").to_dict(orient="records")
    return [KreamProductCardSchema(**row) for row in data]

def get_kream_product_bridge(brand_name: str) :
    path = f"router/dev/kream/data/detail/{brand_name}/"
    last_update = get_last_update_date(path)
    file_name = f"{last_update}-product_detail.parquet.gzip"
    product_detail = pd.read_parquet(path + file_name)
    data = product_detail[["kream_id", "product_id"]].to_dict(orient="records")
    return [KreamProductIdBridgeSchmea(**row) for row in data]


def get_kream_trading_volume(brand_name: str) :
    path = f"router/dev/kream/data/detail/{brand_name}/"
    last_update = get_last_update_date(path)
    file_name = f"{last_update}-trading_volume.parquet.gzip"
    data = pd.read_parquet(path + file_name).to_dict(orient="records")
    return [KreamTradingVolumeSchema(**row) for row in data]

def get_kream_buy_and_sell(brand_name: str) :
    path = f"router/dev/kream/data/detail/{brand_name}/"
    last_update = get_last_update_date(path)
    file_name = f"{last_update}-buy_and_sell.parquet.gzip"
    data= pd.read_parquet(path + file_name).to_dict(orient="records")
    return [KreamBuyAndSellSchema(**row) for row in data]