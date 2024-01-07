import os
import pytest
from platform_scrap.list.main import PlatformListMain

current_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def KreamList():
    yield PlatformListMain(current_path)


@pytest.mark.anyio
async def test_PlatformList(KreamList: PlatformListMain):
    await KreamList.init_pw_kream_scraper(
        target_list=["the north face"], num_processor=1
    )
    await KreamList.execute()
