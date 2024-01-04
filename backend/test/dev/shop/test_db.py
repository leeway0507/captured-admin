# import pytest
# from db.connection import conn_engine

# # TODO: admin DB 연결하기
# from db.dev_db import session_local


# from components.dev.shop.load_scrap_result import get_scrap_size_product_id_dict
# from components.dev.shop.update_to_db import update_product_id_by_shop_product_card_id


# @pytest.mark.asyncio
# async def test_update_product_id_by_shop_product_card_id():
#     data = get_scrap_size_product_id_dict("231226-112531")
#     async with session_local() as session:  # type: ignore
#         product_id_info = data.get("data")
#         result = await update_product_id_by_shop_product_card_id(
#             session, product_id_info
#         )

#     print(result)
