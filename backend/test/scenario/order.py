from sqlalchemy import select, delete

from test_module.order import *
from variables import (
    get_register_info,
    get_address_info,
    get_order_history_info,
    get_order_rows,
    get_product_info,
)
from scenario.auth import login, register_user_and_address, delete_user, delete_address_force
from scenario.product import (
    delete_product_size_force,
    delete_product_force,
    test_product_create,
    get_last_product,
    test_product_size_create,
)
from model.auth_model import LoginSchema, TokenData, LoginResponseSchema
from model.db_model import OrderHistoryRequestSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db.tables import UserAddressTable, OrderHistoryTable, OrderRowTable


async def order_scenario(db):
    register_info = get_register_info()
    form_data = LoginSchema(email=register_info.email, password=register_info.password)
    order_history = get_order_history_info()
    order_rows = get_order_rows()

    # 주문 내역 생성
    # 주문 내역 조회
    # 거래 아이템 리스트 생성
    # 거래 아이템 리스트 조회

    print("----------order_scenario 준비----------")
    # product 생성
    await test_product_create(db=db, product=get_product_info())

    # 제품 Read
    last_row = await get_last_product(db=db)
    sku = last_row.sku
    assert sku != None, "SKU가 생성되지 않았습니다."

    # 제품 사이즈 생성
    await test_product_size_create(db=db, sku=sku)

    # 유저 생성
    try:
        user_info = await login(db=db, form_data=form_data)
    except:
        await register_user_and_address(
            db=db, register_info=register_info, address_info=get_address_info()
        )
        user_info = await login(db=db, form_data=form_data)

    print("----------order_scenario 시작----------")
    user_token = TokenData(**user_info)
    address = await get_a_single_address(db=db, user=user_token)

    order_history.user_id = user_token.user_id
    order_history.address_id = address.address_id  #

    order_history = await create_order_history(db=db, user=user_token, order_history=order_history)
    order_id = order_history.get("orderId")
    assert order_id, "주문내역 생성 실패"
    await create_order_row(db, order_id, order_rows, user_token.user_id)
    print("----------order_scenario 성공----------")

    await delete_order_row(db=db, order_id=order_id)
    await delete_order_history(db=db, user_id=user_token.user_id)
    await delete_address_force(db=db, user_id=user_token.user_id)
    await delete_user(db=db, user_id=user_token.user_id)
    await delete_product_size_force(db=db)
    await delete_product_force(db=db)
    print("----------order_scenario 종료----------")


# Part --------------------------------------------------------------


async def get_a_single_address(db: AsyncSession, user: TokenData):
    stmt = select(UserAddressTable).where(UserAddressTable.user_id == user.user_id)
    result = await db.execute(stmt)
    address = result.scalars().first()
    return address


async def create_order_history(
    db: AsyncSession, user: TokenData, order_history: OrderHistoryRequestSchema
):
    print("---create_order_history---")
    order_id = await test_create_order_history(db, order_history, user)
    print(order_id)
    check = await test_get_order_history(db=db, user=user)
    print(check[0])
    assert check[0].get("orderId") == order_id.get("orderId"), "생성된 주문내역과 조회된 주문내역이 같아야합니다."
    return check[0]


async def create_order_row(
    db: AsyncSession, order_id: str, order_rows: List[OrderRowSchmea], user_id: str
):
    print("---create_order_row---")
    result = await test_create_order_row(db, order_id, order_rows, user_id)
    print(result)
    order_row_check = await test_get_order_row(db=db, order_id=order_id)
    print(order_row_check)


async def delete_order_history(db: AsyncSession, user_id: str):
    stmt = delete(OrderHistoryTable).where(OrderHistoryTable.user_id == user_id)
    await db.execute(stmt)
    await db.commit()


async def delete_order_row(db: AsyncSession, order_id: str):
    stmt = delete(OrderRowTable).where(OrderRowTable.order_id == order_id)
    await db.execute(stmt)
    await db.commit()
