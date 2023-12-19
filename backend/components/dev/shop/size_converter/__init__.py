import os
import pandas as pd
import re


def _load_foot_size():
    abs_path = "/Users/yangwoolee/repo/stock_scraping/codes/"
    assert os.path.exists(abs_path), f"절대 경로가 잘못되었습니다. {abs_path}"
    foot_size = pd.read_csv(
        abs_path + "data/size/foot_size.csv", index_col=0, dtype=str
    )
    return foot_size


foot_size = _load_foot_size()
eu_list = {
    "35",
    "35 2/3",
    "36",
    "36 2/3",
    "37 1/3",
    "38",
    "38 2/3",
    "39 1/3",
    "40",
    "40 2/3",
    "41 1/3",
    "42",
    "42 2/3",
    "43 1/3",
    "44",
    "44 2/3",
    "45 1/3",
    "46",
    "46 2/3",
    "47 1/3",
    "48",
    "48 2/3",
    "49 1/3",
}


def convert_size(size: str):
    try:
        if size in ["-", None, "nan"]:
            print("size is None")
            return "-"

        # 신발 사이즈
        if "UK" in size:
            var = re.sub(r".*?([\d.]+).*", r"\1", size)
            mask = foot_size[foot_size["UK"] == var]
            return size if mask.empty else int(mask["KOR"].tolist()[0])

        if "US" in size:
            var = re.sub(r".*?([\d.]+).*", r"\1", size)
            mask = foot_size[foot_size["US"] == var]
            return size if mask.empty else int(mask["KOR"].tolist()[0])

        if "IT" in size:
            size_name = size.replace("IT", "").strip()
            mask = foot_size[foot_size["EU"] == size_name]
            return size if mask.empty else int(mask["KOR"].tolist()[0])

        if size in eu_list:
            mask = foot_size[foot_size["EU"] == size]
            return size if mask.empty else int(mask["KOR"].tolist()[0])

        size_lower = size.lower().strip()

        if size_lower == "large":
            return "L"
        if size_lower == "medium":
            return "M"
        if size_lower == "small":
            return "S"
        if size_lower == "x-small":
            return "XS"
        if size_lower in {"x-large", "x large"}:
            return "XL"
        if size_lower in {"xx-large", "2xl"}:
            return "XXL"
        if size_lower in {"xxx-large", "3xl"}:
            return "XXXL"
        if size_lower in {"one size", "onesize", "os"}:
            return "ONE SIZE"

        return size_lower.upper()
    except Exception as e:
        # 교훈 : try-except를 쓸 때 에러가 발생하는 위치를 정확히 출력하자, 그렇지 않으면 디버깅 지옥이 된다.
        print("size_converting_error : ", e)
        return size
