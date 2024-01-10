import os
import pytest
from shop_scrap.page.target_extractor import TargetExractor, load_target_strategy

current_path = __file__.rsplit("/", 1)[0]


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def Target(test_session):
    yield TargetExractor(test_session)


@pytest.mark.anyio
async def test_all_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("all")
    value = "2"
    data = await Target.extract_data(value)

    assert len(data) == 2


@pytest.mark.anyio
async def test_product_id_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("product_id")
    value = "bd7633,DB3021"
    data = await Target.extract_data(value)

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_shop_product_card_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("shop_product_card")
    value = "116,142"
    data = await Target.extract_data(value)

    # 142번은 품절이기 때문
    assert len(data) == 1


@pytest.mark.anyio
async def test_shop_name_strategy(Target: TargetExractor):
    Target.strategy = load_target_strategy("shop_name")
    value = "consortium"
    data = await Target.extract_data(value)

    assert isinstance(data[0], dict)
