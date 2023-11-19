import json
from dotenv import dotenv_values

config = dotenv_values(".env.dev")


def create_last_update_shop_detail_log(scrap_time: str):
    """product_card_list log 생성"""

    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    temp_path = path + "_temp/"

    with open(temp_path + "scrap_page_result.json", "r") as f:
        process_result = json.load(f)

    log = {
        "scrap_time": scrap_time,
        **process_result,
    }

    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    result_path = path + "_scrap-result/"

    with open(result_path + scrap_time + ".json", "w") as f:
        f.write(json.dumps(log, indent=4, default=str))


def get_product_page_result(scrap_time: str):
    """scrap 결과 조회"""
    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    result_path = path + "_scrap-result/"

    with open(result_path + scrap_time + ".json", "r") as f:
        scrap_result = json.load(f)

    return scrap_result


def update_product_page_result(scrap_time: str, key, value):
    path = config["SHOP_PRODUCT_PAGE_DIR"]
    assert path, "SHOP_PRODUCT_PAGE_DIR is not defined in .env"
    result_path = path + "_scrap-result/"

    with open(result_path + scrap_time + ".json", "r") as f:
        scrap_result = json.load(f)
        scrap_result[key] = value

    with open(result_path + scrap_time + ".json", "w") as f:
        f.write(json.dumps(scrap_result, default=str))

    return scrap_result
