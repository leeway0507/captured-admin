from typing import List, Dict
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, text

from logs.make_log import make_logger
from db.tables import OrderHistoryTable, OrderRowTable, SizeTable
from db.connection import commit
from model.db_model import OrderHistoryInDBSchema, OrderRowInDBSchmea, SizeSchema
from model.db_model import ProductInfoDBSchema
from db.tables import ProductInfoTable
from sqlalchemy.dialects.mysql import insert

error_log = make_logger("logs/admin/util.log", "admin_router")


async def get_order_history(db: AsyncSession):
    result = await db.execute(select(OrderHistoryTable))
    result = result.all()
    print(result)
    return [OrderHistoryInDBSchema(**row.to_dict()).model_dump(by_alias=True) for row in result]


async def get_order_row(db: AsyncSession):
    result = await db.execute(select(OrderRowTable))
    result = result.all()
    return [OrderRowInDBSchmea(**row.to_dict()).model_dump(by_alias=True) for row in result]


async def create_new_sku(db: AsyncSession):
    column = ProductInfoTable.sku
    last_number = await db.execute(select(column).order_by(column.desc()))
    last_number = last_number.scalar()

    if last_number == None:
        return 1

    return last_number + 1


async def create_product(db: AsyncSession, product: ProductInfoDBSchema):
    query = db.add(ProductInfoTable(**product.model_dump()))
    return await commit(db, query, error_log)


async def update_product(db: AsyncSession, product: ProductInfoDBSchema):
    """제품 업데이트
    -foreign constraint-
    product를 업데이트 하거나 지우기 위해서는 자식 테이블인 size 테이블의 데이터를 제거해야함.
    테이블에 해당 sku 사이즈가 존재하는지 확인하고, 존재하면 삭제 후 다시 생성해야함.
    """

    assert isinstance(product.sku, int), f"sku is None"

    size_rows = await get_size_list(db, product.sku)

    if size_rows:
        await delete_size(db, product.sku)

    if await delete_product(db, product.sku):
        await create_product(db, product)

    if size_rows:
        size_list = [row.size for row in size_rows]
        await create_size(db, product.sku, size_list)
    return True


async def delete_product(db: AsyncSession, sku: int):
    stmt = delete(ProductInfoTable).where(ProductInfoTable.sku == sku)
    query = await db.execute(stmt)
    return await commit(db, query, error_log)


async def get_size_list(db: AsyncSession, sku: int):
    result = await db.execute(f"select * from size where sku = {sku}")
    result = result.all()

    return [SizeSchema(**row) for row in result]


async def create_size(db: AsyncSession, sku: int, size_list: List[str]):
    size_objects = [
        SizeSchema(sku=sku, size=size, updated_at=datetime.now(), available=True).model_dump()
        for size in size_list
    ]
    query = await db.execute(insert(SizeTable).values(size_objects))
    return await commit(db, query, error_log)


async def update_size(db: AsyncSession, size_list: List[Dict[str, str]]):
    stmt = insert(SizeTable).values(size_list)

    update_stmt = stmt.on_duplicate_key_update(
        updated_at=stmt.inserted.updated_at,
        available=stmt.inserted.available,
    )

    query = await db.execute(update_stmt)
    return await commit(db, query, error_log)


async def delete_size(db: AsyncSession, sku: int):
    stmt = delete(SizeTable).where(SizeTable.sku == sku)
    query = await db.execute(stmt)
    return await commit(db, query, error_log)


async def get_category(db:AsyncSession) :
    stmt = select(ProductInfoTable)
    query = await db.execute(stmt)
    result = query.all()
    return [ProductInfoDBSchema(**row[0].to_dict()).model_dump(by_alias=True) for row in result]