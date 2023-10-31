from sqlalchemy.ext.asyncio import AsyncSession
from router.order.utils import (
    get_user_order_count,
    create_order_history_into_db,
    create_order_row_into_db,
    get_order_history_from_db,
    get_order_row_from_db,
)

from model.db_model import (
    OrderHistoryRequestSchema,
    OrderRowSchmea,
    OrderHistoryInDBSchema,
    OrderRowInDBSchmea,
)
from model.auth_model import TokenData
from datetime import datetime
from typing import List


async def test_create_order_history(
    db: AsyncSession, order_history: OrderHistoryRequestSchema, user: TokenData
):
    """주문 내역 생성"""
    order_count = await get_user_order_count(db)
    order_id = f"OH-{user.user_id}-{order_count}"
    order_history.user_id = user.user_id
    order_history_in_db = OrderHistoryInDBSchema(
        **order_history.model_dump(),
        order_id=order_id,
        user_order_number=order_count,
        ordered_at=datetime.now(),
    )
    if await create_order_history_into_db(order_history_in_db, db):
        return {"orderId": order_id}
    else:
        raise Exception("주문내역 생성 실패")


async def test_create_order_row(
    db: AsyncSession, order_id: str, order_rows: List[OrderRowSchmea], user_id: str
):
    """
    주문 상세내역 생성
    주문 내역과 구분한 이유는 orderHistory가 성공적으로 생성되었는지 확인하기 위함
    """
    order_row_in_db_list = []
    for order_row in order_rows:
        order_row_in_db_list.append(OrderRowInDBSchmea(**order_row.model_dump(), order_id=order_id))
    if await create_order_row_into_db(order_row_in_db_list, db):
        return {"message": "success"}
    else:
        raise Exception("주문상세내역 생성 실패")


async def test_get_order_history(db: AsyncSession, user: TokenData):
    """주문 내역 조회"""
    order_history = await get_order_history_from_db(db, user.user_id)
    return order_history


async def test_get_order_row(db: AsyncSession, order_id: str):
    """주문 상세내역 조회"""
    order_row = await get_order_row_from_db(db, order_id)
    return order_row
