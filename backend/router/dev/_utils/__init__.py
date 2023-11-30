from typing import Dict, List, Callable, Sequence
from traceback import format_exception
import pydantic
import pandas as pd


def save_to_parquet(path: str, file_name: str, scrap_data: List[Dict]):
    file_path = f"{path}/{file_name}.parquet.gzip"
    pd.DataFrame(scrap_data).drop_duplicates().to_parquet(
        path=file_path, compression="gzip"
    )
    return True


def split_size(l: List, num_list: int) -> List[List]:
    """
    l: list
    n_l : number of list
    """
    q, r = divmod(len(l), num_list)

    if r > 0:
        # ex 10 | 3
        # 4,4,2
        # l_size = list size
        l_size = len(l) // num_list
        l_size += 1

        output = [l[i * l_size : (i + 1) * l_size] for i in range(num_list - 1)]
        output.append(l[(num_list - 1) * l_size :])

    else:
        # ex 9 | 3
        # 3,3,3
        l_size = len(l) // num_list
        output = [l[i : i + q] for i in range(0, len(l), l_size)]

    return output
