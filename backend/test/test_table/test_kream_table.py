import pytest
from table.table_kream import KreamTable

pytestmark = pytest.mark.asyncio(scope="module")


# anyio settings do not remove
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def Kream():
    table = KreamTable(max_day=35)
    yield table


# @pytest.mark.anyio
# async def test_get_kream_prod_card(Kream: KreamTable):
#     strategy = "productId"
#     content = "DB3021"
#     result = await Kream.get_kream_prod_card(strategy, content)
#     print(result)
#     assert isinstance(result, list)


# @pytest.mark.anyio
# async def test_get_buy_and_sell(Kream: KreamTable):
#     prodId = "DB3021"
#     result = await Kream.get_buy_and_sell(prodId)
#     assert isinstance(result, list)


@pytest.mark.anyio
async def test_base_date(Kream: KreamTable):
    print(Kream._base_date())


# @pytest.mark.anyio
# async def test_get_trading_volume(Kream: KreamTable):
#     """
#     최신 수집한 데이터로 테스트 해야함.
#     trading volume 추출 시 현재 기준 max_day를
#     뺀 날짜까지를 기준으로 필터링하기 때문
#     """
#     prodId = "DB3021"
#     result = await Kream.get_trading_volume(prodId)
#     print(result[-1])
#     assert isinstance(result, list)


@pytest.mark.anyio
async def test_preprocess_trading_volume(Kream: KreamTable):
    prodId = "DB3021"
    volume_data = await Kream.get_trading_volume(prodId)
    result = await Kream.preprocess_trading_volume(volume_data)
    # print(result.iloc[0])


@pytest.mark.anyio
async def test_get_market_price_info(Kream: KreamTable):
    prodId = "DB3021"
    result = await Kream.get_market_price_info(prodId)
    print(result["baseDate"])
    print(result["data"])
