import os
import pytest
from pandas import DataFrame
import pandas as pd
from shop_scrap.size_batch.batch_data_processor import SizeBatchProcessor

# from db.dev_db import admin_session_local
# from db.production_db import prod_session_local


current_path = __file__.rsplit("/", 1)[0]
pytestmark = pytest.mark.asyncio(scope="module")
batch_time = "20240117-123456"


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def ComD(test_session):
    processor = SizeBatchProcessor(
        test_session,
        test_session,
        current_path,
        batch_time,
    )

    yield processor


@pytest.mark.anyio
async def test_load_data(ComD: SizeBatchProcessor):
    data = await ComD._shop_size_data()
    assert isinstance(data[0], dict)

    data = await ComD._shop_card_data()
    assert isinstance(data[0], dict)

    data = await ComD._prod_card_data()
    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_create_batch_folder(ComD: SizeBatchProcessor):
    ComD.create_batch_folder()
    assert os.path.exists(os.path.join(current_path, batch_time))


@pytest.mark.anyio
async def test_save_db_data(ComD: SizeBatchProcessor):
    # Then
    await ComD.save_db_data()


@pytest.mark.anyio
async def test_prod_size_data(ComD: SizeBatchProcessor):
    # When
    ComD.load_db_data()

    # Then
    assert isinstance(ComD.shop_size_data_df, DataFrame)
    assert isinstance(ComD.shop_card_data_df, DataFrame)
    assert isinstance(ComD.prod_card_data_df, DataFrame)

    # id map
    id_map = ComD.generate_id_map()

    id_map.to_parquet(
        os.path.join(current_path, batch_time, "test_id_map.parquet.gzip"),
        compression="gzip",
    )

    size_batch_df = pd.merge(
        id_map, ComD.shop_size_data_df, on="shop_product_card_id", how="left"
    )
    size_batch_df.to_parquet(
        os.path.join(
            current_path,
            batch_time,
            "test_size_batch_df.parquet.gzip",
        ),
        compression="gzip",
    )

    ComD.create_prod_size_data()

    assert os.path.exists(
        os.path.join(
            current_path,
            batch_time,
            "prod_size_data.parquet.gzip",
        )
    )


# @pytest.mark.anyio
# async def test_load_db_data_and_size_batch_data(ComD: SizeBatchProcessor):
#     # When
#     ComD.load_db_data()

#     # Then
#     assert isinstance(ComD.shop_size_data_df, DataFrame)
#     assert isinstance(ComD.shop_card_data_df, DataFrame)
#     assert isinstance(ComD.prod_card_data_df, DataFrame)

#     ComD.create_prod_size_data()

#     assert os.path.exists(
#         os.path.join(
#             current_path,
#             batch_time,
#             "prod_size_data.parquet.gzip",
#         )
#     )
