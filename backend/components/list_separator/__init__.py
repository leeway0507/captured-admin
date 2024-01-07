from typing import List


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
