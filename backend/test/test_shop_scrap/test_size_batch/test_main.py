from typing import List
import pytest
from shop_scrap.size_batch import SizeBatchMain


current_path = __file__.rsplit("/", 1)[0]
scrap_time = "19920507-123456"
# pytestmark = pytest.mark.asyncio(scope="module")


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Batch(test_session):
    batch = SizeBatchMain(current_path, test_session, test_session, test_session)
    await batch.init(batch_size=4, num_processor=4, scrap_time=scrap_time)
    yield batch


# @pytest.mark.anyio
# async def test_logExcution(Batch: SizeBatchMain):
#     await Batch._test_logExcutionResult()


@pytest.mark.anyio
async def test_extract_target_list(Batch: SizeBatchMain):
    data = await Batch.extract_target_list()

    print("target_list")
    print(data)


# @pytest.mark.anyio
# async def test_scrap_candidate_page(Batch: SizeBatchMain):
#     await Batch.scrap_candidate_page()


# @pytest.mark.anyio
# async def test_sync_scrap_data_to_shop_db(Batch: SizeBatchMain):
#     await Batch.sync_scrap_data_to_shop_db()


# @pytest.mark.anyio
# async def test_create_prod_batch_data(Batch: SizeBatchMain):
#     await Batch.create_prod_batch_data()


# @pytest.mark.anyio
# async def test_sync_prod_batch_data_to_prod_db(Batch: SizeBatchMain):
#     await Batch.sync_prod_batch_data_to_prod_db()


# @pytest.mark.anyio
# async def test_execute_size_batch(Batch: SizeBatchMain):
#     await Batch.execute(scrap_time, 2, 2)
