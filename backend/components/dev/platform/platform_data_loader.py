# import os
# import pandas as pd
# from typing import Optional

# #####################


# class PlatformDataLoader:
#     def __init__(
#         self,
#     )

#     def late_binding(
#         self,
#         brand: str,
#         platform: str,
#         file_type: str,
#         scrap_date: Optional[str] = None,
#         sample: int = 10,
#     ):
#         self.brand = brand
#         self.platform = platform
#         self.sample = sample
#         self.file_type = file_type

#         if scrap_date:
#             self.scrap_date = scrap_date
#         else:
#             self.scrap_date = self.get_last_scrap_date_name()

#     def get_last_scrap_date_name(self) -> str:
#         """가장 최근에 생성된 데이터명을 가져온다."""
#         file_names = os.listdir(self.path)
#         file_names.sort()
#         last_scrap_file_name = file_names[-1]
#         file_name = last_scrap_file_name.rsplit("-", 1)[0]
#         return file_name

#     def load(self):
#         data = self.load_file()
#         return self.set_template(data)

#     def load_file(self):
#         file_name = f"{self.scrap_date}-{self.file_type}.parquet.gzip"
#         file_path = os.path.join(self.path, self.brand, file_name)
#         return pd.read_parquet(file_path).to_dict("records")

#     def set_template(self, data):
#         kream_id_list = self.get_unique_kream_id(data)
#         return {
#             "len": len(kream_id_list),
#             "kream_id_list": kream_id_list,
#             "data": data[: self.sample],
#         }

#     def get_unique_kream_id(self, data):
#         return list(set(map(lambda x: x.get("kream_id"), data)))
