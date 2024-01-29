import json
import pytest
from shop_scrap.page.target_extractor import TargetExractor, load_target_strategy
from db.dev_db import admin_session_local

current_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Target(test_session):
    # yield TargetExractor(test_session)
    yield TargetExractor(admin_session_local)


@pytest.mark.anyio
async def test_all_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("all")
    value = "2"
    data = await Target.extract_data(value)

    assert len(data) == 2


@pytest.mark.anyio
async def test_product_id_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("productId")
    value = "bd7633,DB3021"
    data = await Target.extract_data(value)

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_shop_product_card_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("shopProductCard")
    value = "116,142"
    data = await Target.extract_data(value)
    assert len(data) in [0, 2]


@pytest.mark.anyio
async def test_shop_name_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("shopName")
    value = "consortium"
    data = await Target.extract_data(value)

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_shop_name_brand_name_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("shopNameBrandName")
    value = json.dumps({"shopName": "consortium", "brandName": "adidas"})
    data = await Target.extract_data(value)

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_last_scrap_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("lastScrap")
    value = "20240124-151900"
    data = await Target.extract_data(value)

    print(data)

    assert isinstance(data[0], dict)
