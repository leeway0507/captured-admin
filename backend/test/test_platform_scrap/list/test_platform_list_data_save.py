import os
import pytest

from test.utils import remove_test_folder
from platform_scrap.list.data_save import PlatformListDataSave

current_path = __file__.rsplit("/", 1)[0]

report_path = os.path.join(current_path, "_report")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def DataSave():
    yield PlatformListDataSave(current_path)


@pytest.mark.anyio
async def test_init_config(DataSave: PlatformListDataSave):
    await DataSave.init_config()

    assert DataSave.platform_type == "kream"


@pytest.mark.anyio
async def test_save_data(DataSave: PlatformListDataSave):
    await DataSave.save_scrap_data()
