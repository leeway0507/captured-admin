# import pytest
# from .mock import MockBrowserController, MockCandidateExtractor

# from components.dev.shop.shop_product_card_page.page_module_factory import (
#     PwShopPageModuleFactory,
# )
# from components.dev.shop.shop_product_card_page import ShopPageMain

# import os
# import sys

# pytest_plugins = ("pytest_asyncio",)


# @pytest.mark.asyncio
# async def test_save_parquet():
#     """
#     GIVEN : SCRAPER 데이터 수집결과 임시 파일에 저장 완료
#     WHEN : 임시파일 전처리 및 parquet 파일 생성
#     THEN : 기본 data path에 맞게 parquet 파일 저장
#     """
#     # GIVEN
#     page_logic = ShopPageMain(
#         1, MockBrowserController(), PwShopPageModuleFactory(), MockCandidateExtractor()
#     )

#     # WHEN
#     time_now = await page_logic.save_scrap_result_to_parquet()

#     # THEN
#     size_file_name = time_now + "-size.parquet.gzip"
#     product_id_file_name = time_now + "-product-id.parquet.gzip"
#     size_file_path = os.path.join(page_logic.path, size_file_name)
#     product_id_file_path = os.path.join(page_logic.path, product_id_file_name)
#     size_file = os.path.isfile(size_file_path)
#     product_id_file = os.path.isfile(product_id_file_path)

#     assert size_file and product_id_file

#     os.remove(size_file_path)
#     os.remove(product_id_file_path)
