from numpy import isin
import pandas as pd
import os 
from model.db_model_kream import KreamProductCardSchema, KreamProductIdBridgeSchmea, KreamTradingVolumeSchema, KreamBuyAndSellSchema


default_path = "router/dev/kream/data/detail/"

def get_last_update_date(path: str) -> str:
    """가장 최근에 생성된 날짜를 이름을 가져온다."""
    file_names = os.listdir(path)
    file_names.sort()
    d = file_names[-1]
    return d.rsplit("-", 1)[0]

#####################

def get_last_update_kream_product_card(brand_name: str,sample:int=10):
    path =default_path+brand_name+"/"
    last_update_datail = get_last_update_date(path)

    path = f"router/dev/kream/data/brand/{brand_name}/"
    last_update_list = get_last_update_date(path)
    return get_kream_product_card(brand_name, last_update_datail,last_update_list,sample)

def get_last_update_kream_product_bridge(brand_name: str,sample:int=10):
    path =default_path+brand_name+"/"
    last_update = get_last_update_date(path)
    return get_kream_product_bridge(brand_name, last_update,sample)

def get_last_update_kream_trading_volume(brand_name: str,sample:int=10):
    path =default_path+brand_name+"/"
    last_update = get_last_update_date(path)
    return get_kream_trading_volume(brand_name, last_update,sample)

def get_last_update_kream_buy_and_sell(brand_name: str,sample:int=10):
    path =default_path+brand_name+"/"
    last_update = get_last_update_date(path)
    return get_kream_buy_and_sell(brand_name, last_update,sample)



#####################

def get_kream_product_card(brand_name: str,scrap_date_detail:str,scrap_date_list:str,sample:int) :
    path = default_path+brand_name+"/"
    file_name = f"{scrap_date_detail}-product_detail.parquet.gzip"
    product_detail = pd.read_parquet(path + file_name)

    path = f"router/dev/kream/data/brand/{brand_name}/"
    file_name = f"{scrap_date_list}-product_card_list.parquet.gzip"
    product_card_list = pd.read_parquet(path + file_name)

    data = pd.merge(product_detail, product_card_list, on="kream_id", how="inner").to_dict(orient="records")
    
    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len":len(kream_id_list),"kream_id_list": kream_id_list,"data": data[:sample]}

def get_kream_product_bridge(brand_name: str,scrap_date:str,sample:int) :
    path = default_path+brand_name+"/"
    file_name = f"{scrap_date}-product_detail.parquet.gzip"

    product_detail = pd.read_parquet(path + file_name)
    data = product_detail[["kream_id", "product_id"]].to_dict(orient="records")
    
    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len":len(kream_id_list),"kream_id_list": kream_id_list,"data": data[:sample]}


def get_kream_trading_volume(brand_name: str,scrap_date:str,sample:int) :
    path = default_path+brand_name+"/"
    file_name = f"{scrap_date}-trading_volume.parquet.gzip"
    data = pd.read_parquet(path + file_name).to_dict(orient="records")

    
    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len":len(kream_id_list),"kream_id_list": kream_id_list,"data": data[:sample]}

def get_kream_buy_and_sell(brand_name: str,scrap_date:str,sample:int) :
    path = default_path+brand_name+"/"
    file_name = f"{scrap_date}-buy_and_sell.parquet.gzip"
    data=pd.read_parquet(path + file_name).to_dict(orient="records")
    
    kream_id_list = list(set(map(lambda x: x.get("kream_id"), data)))
    return {"len":len(kream_id_list),"kream_id_list": kream_id_list,"data": data[:sample]}