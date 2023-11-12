from email.policy import default
import json
from typing import Dict
from dotenv import dotenv_values

config = dotenv_values(".env.dev")


def create_last_update_shop_detail_log(shop_name: str, scrap_time: str):
    """product_card_list log 생성"""

    load_path = config["SHOP_SCRAP_TEMP_DIR"]
    assert load_path, "SHOP_SCRAP_TEMP_DIR is not defined in .env"

    with open(load_path + "process_result.json", "r") as f:
        process_result = json.load(f)

    log = {
        "shop_name": shop_name,
        "scrap_time": scrap_time,
        **process_result,
    }

    path = config["SHOP_SCRAP_RESULT_DIR"]
    assert path, "SHOP_SCRAP_RESULT_DIR is not defined in .env"

    scrap_name = scrap_time + "-" + shop_name

    with open(path + scrap_name + ".json", "w") as f:
        f.write(json.dumps(log, indent=4, default=str))


def get_scrap_result(scrap_name: str):
    """scrap 결과 조회"""
    path = config["SHOP_SCRAP_RESULT_DIR"]
    assert path, "SHOP_SCRAP_RESULT_DIR is not defined in .env"

    with open(path + scrap_name + ".json", "r") as f:
        scrap_result = json.load(f)

    return scrap_result


def update_scrap_result(scrap_name, key, value):
    path = config["SHOP_SCRAP_RESULT_DIR"]
    assert path, "SHOP_SCRAP_RESULT_DIR is not defined in .env"

    with open(path + scrap_name + ".json", "r") as f:
        scrap_result = json.load(f)
        scrap_result[key] = value

    with open(path + scrap_name + ".json", "w") as f:
        f.write(json.dumps(scrap_result, default=str))

    return scrap_result
