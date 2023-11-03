import json 
from typing import Dict
from .load_scrap_result import *
from dotenv import dotenv_values

config = dotenv_values(".env.dev")

def create_last_update_kream_detail_log(scrap_name:str):
    """product_card_list log 생성"""


    load_path = config["KREAM_DETAILS_TEMP_DIR"]
    assert load_path, "KREAM_DETAILS_TEMP_DIR is not defined in .env"

    with open(load_path+'process_result.json','r') as f :
        process_result = json.load(f)



    scrap_time, brand = scrap_name.rsplit("-",1)

    log = {
    'scrap_name':scrap_name,
    'num_process':process_result.get("num_process"),
    'brand':brand,
    'scrap_time':scrap_time,
    'scrap_result':process_result.get("scrap_result"),
    'kream_product_card' :get_last_update_kream_product_card(brand),
    'kream_trading_volume' :get_last_update_kream_trading_volume(brand),
    'kream_buy_and_sell' :get_last_update_kream_buy_and_sell(brand),
    'kream_product_bridge' :get_last_update_kream_product_bridge(brand),
    }

    path = config["KREAM_SCRAP_RESULT_DIR"]
    assert path, "KREAM_SCRAP_RESULT_DIR is not defined in .env"

    with open(path+scrap_name+'.json','w') as f :
        f.write(json.dumps(log,indent=4,default=str))
        

def get_scrap_result(scrap_name:str) : 
    """scrap 결과 조회"""
    path = config["KREAM_SCRAP_RESULT_DIR"]
    assert path, "KREAM_SCRAP_RESULT_DIR is not defined in .env"

    with open(path+scrap_name+'.json','r') as f :
        scrap_result = json.load(f)

    return scrap_result

   


