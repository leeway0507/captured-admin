import os
from typing import List, Dict, Any
import pandas as pd


def save_to_parquet(path: str, file_name: str, scrap_data: List[Dict[str, Any]]):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, f"{file_name}.parquet.gzip")
    pd.DataFrame(scrap_data).drop_duplicates().to_parquet(
        path=file_path, compression="gzip"
    )
    return True


class ListSeparator:
    @classmethod
    def split(cls, target_list: List, group_num: int) -> List[List]:
        group_size, rest = divmod(len(target_list), group_num)

        if rest == 0:
            output = cls.split_rest_zero(target_list, group_size)

        else:
            output = cls.split_rest_not_zero(target_list, group_size)

        return output

    @staticmethod
    def split_rest_zero(target_list: List, group_size: int) -> List[List]:
        output = [
            target_list[idx : idx + group_size]
            for idx in range(0, len(target_list), group_size)
        ]
        return output

    @staticmethod
    def split_rest_not_zero(target_list: List, group_size: int) -> List[List]:
        group_size += 1
        output = [
            target_list[idx * group_size : (idx + 1) * group_size]
            for idx in range(len(target_list) // group_size)
        ]
        output.append(target_list[(len(target_list) // group_size) * group_size :])
        return output
