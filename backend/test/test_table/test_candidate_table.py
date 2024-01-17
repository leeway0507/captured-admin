import pytest
from table.table_candidate import CandidateTable
from db.dev_db import admin_session_local
from sqlalchemy import select
from db.tables_shop import ShopProductCardTable

pytestmark = pytest.mark.asyncio(scope="module")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def Candidate():
    table = CandidateTable()
    yield table


@pytest.mark.anyio
async def test_patch_shop_product_card(Candidate: CandidateTable):
    card_id = 1

    await Candidate.patch(
        card_id, "shop_product_name", "candle-no-2-green-jasmine-ybzaa-m84001-vab"
    )

    d = await Candidate._shop_card_list("shop", "consortium")

    assert d[0]["shopProductCardId"] == card_id
    assert d[0]["shopProductName"] == "candle-no-2-green-jasmine-ybzaa-m84001-vab"


@pytest.mark.anyio
async def test_load_table_shop(Candidate: CandidateTable):
    data = await Candidate._shop_card_list("shop", "consortium")

    assert isinstance(data[0], dict)


@pytest.mark.anyio
async def test_get(Candidate: CandidateTable):
    data = await Candidate._shop_card_list("brand", "adidas")

    assert isinstance(data[0], dict)

    prod_id_list = Candidate._product_id_list(data)

    assert isinstance(prod_id_list[0], str)

    kream_match_info = await Candidate._kream_match_info(prod_id_list)

    assert isinstance(kream_match_info, list)
    if len(kream_match_info) > 0:
        assert isinstance(kream_match_info[0], str)


@pytest.mark.anyio
async def test_buying_currency(Candidate: CandidateTable):
    currency = Candidate._buying_currency()

    assert set(currency.keys()) == {"update", "data"}
