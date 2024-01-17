# import pytest
# from admin.backend.table import table_utils

# pytestmark = pytest.mark.asyncio(scope="module")


# # anyio settings do not remove
# @pytest.fixture(scope="session")
# def anyio_backend():
#     return "asyncio"


# @pytest.mark.anyio
# async def test_load_shop_info():
#     x = await table_utils.load_shop_info()
#     assert isinstance(x[0], dict)
