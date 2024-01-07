from pprint import pprint
from typing import List, Dict, Any, Optional, Tuple, FrozenSet
import time

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update, func, and_
from sqlalchemy.dialects.mysql import insert

from logs.make_log import make_logger
from db.tables_production import (
    OrderHistoryTable,
    OrderRowTable,
    SizeTable,
    ProductInfoTable,
)
from db.connection import commit
from db.production_db import session_local
from model.db_model_production import (
    OrderHistoryInDBSchema,
    OrderRowInDBSchmea,
    SizeSchema,
    ProductInfoDBSchema,
)
from model.product_model import (
    ProductResponseSchema,
)
from custom_alru import alru_cache
from sqlalchemy.exc import IntegrityError

error_log = make_logger("logs/admin/util.log", "admin_router")


async def get_order_history(db: AsyncSession):
    result = await db.execute(select(OrderHistoryTable))
    result = result.scalars().all()
    print(result)
    return [
        OrderHistoryInDBSchema(**row.to_dict()).model_dump(by_alias=True)
        for row in result
    ]


async def get_order_row(db: AsyncSession):
    result = await db.execute(select(OrderRowTable))
    result = result.all()
    return [
        OrderRowInDBSchmea(**row.to_dict()).model_dump(by_alias=True) for row in result
    ]


async def create_new_sku(db: AsyncSession):
    column = ProductInfoTable.sku
    stmt = select(column).order_by(column.desc()).limit(1)
    last_number = await db.execute(stmt)
    last_number = last_number.scalar()
    if last_number == None:
        return 1

    return last_number + 1


async def create_product(db: AsyncSession, product: ProductInfoDBSchema):
    stmt = insert(ProductInfoTable).values(product.model_dump())
    await db.execute(stmt)
    await db.commit()
    return True


async def update_product(db: AsyncSession, product: ProductInfoDBSchema):
    """제품 업데이트
    -foreign constraint-
    product를 업데이트 하거나 지우기 위해서는 자식 테이블인 size 테이블의 데이터를 제거해야함.
    테이블에 해당 sku 사이즈가 존재하는지 확인하고, 존재하면 삭제 후 다시 생성해야함.
    """

    stmt = (
        update(ProductInfoTable)
        .where(ProductInfoTable.sku == product.sku)
        .values(product.model_dump())
    )
    await db.execute(stmt)
    await db.commit()
    return True


async def delete_product(db: AsyncSession, sku: int):
    assert isinstance(sku, int), f"sku is None"

    size_rows = await get_size_list(db, sku)

    try:
        if size_rows:
            stmt = delete(SizeTable).where(SizeTable.sku == sku)
            await db.execute(stmt)

        stmt = delete(ProductInfoTable).where(ProductInfoTable.sku == sku)
        await db.execute(stmt)
        await db.commit()

    except IntegrityError as ie:
        await db.rollback()
        print(ie)
        return {"message": "IntegrityError", "detail": str(ie)}

    return {"message": "success"}


async def get_size_list(db: AsyncSession, sku: int):
    result = await db.execute(f"select * from size where sku = {sku}")
    result = result.all()

    return [SizeSchema(**row) for row in result]


async def create_size(db: AsyncSession, sku: int, size_list: List[str]):
    size_objects = [
        SizeSchema(
            sku=sku,
            size=size,
            updated_at=datetime.now().replace(microsecond=0),
            available=True,
        ).model_dump()
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


async def get_category(db: AsyncSession):
    result = await db.execute(select(ProductInfoTable))
    result = result.all()
    return [
        ProductInfoDBSchema(**row[0].to_dict()).model_dump(by_alias=True)
        for row in result
    ]


async def update_product_deploy_status(db: AsyncSession, sku: int, status: int):
    stmt = (
        update(ProductInfoTable)
        .where(ProductInfoTable.sku == sku)
        .values(deploy=status)
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "success"}


################ get product List
################ get product List
################ get product List
################ get product List
################ get product List
################ get product List
################ get product List
################ get product List
################ get product List


async def get_init_category(
    page: int, limit: int, db: AsyncSession
) -> ProductResponseSchema:
    page_cursor, last_page = await get_page_cursor(page, limit, db)

    # print(get_page_cursor.cache_info())

    # print("get_init_category")
    # print(page_cursor, last_page)

    # query
    stmt = (
        select(ProductInfoTable)
        .where(and_(ProductInfoTable.sku < page_cursor))
        .order_by(ProductInfoTable.deploy.desc(), ProductInfoTable.sku.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    result = result.scalars().all()

    data = [
        ProductInfoDBSchema(**row.to_dict()).model_dump(by_alias=True) for row in result
    ]

    return ProductResponseSchema(data=data, currentPage=page, lastPage=last_page)


async def get_page_cursor(
    page: int, limit: int, db: AsyncSession, query=None
) -> Tuple[int | str, int]:
    """page index에서 페이지에 해당하는 sku를 추출"""
    start = time.time()

    query = {
        "sort_type": "최신순",
        "cursor_query": "ProductInfoTable.sku",
        "order_by": "(ProductInfoTable.sku.desc(),)",
    }

    page_idx = await create_page_index(limit, str(query))
    end = time.time()
    print(
        f"create_page_index time|| page_cursor:{page_idx}",
        f"{end-start:.4f} ",
        # create_page_index.cache_info(),
    )

    # print("캐시 정보")
    # pprint(create_page_index.cache_info())
    # pprint(create_page_index.get_cache())

    if not page_idx:
        return 0, 0

    last_page = max(page_idx.keys())
    if page > last_page:
        return page_idx[last_page], last_page

    # print("page_idx 정상적으로 기입되는지 확인 ", "page : ", page, "page_index : ", page_idx)
    return page_idx[page], last_page


async def create_page_index(limit: int, query: str):
    local_query = eval(query)
    sort_type = local_query.get("sort_type")
    cursor_query = eval(local_query.get("cursor_query"))
    order_by = eval(local_query.get("order_by"))

    assert sort_type, "sort_type is None"
    assert cursor_query, "cursor_query is None"
    assert order_by, "order_by is None"

    db = session_local()
    sku_list = await db.execute(select(cursor_query).order_by(*order_by))
    sku_list = sku_list.all()
    await db.close()  # type: ignore

    return _get_index_by_sort_type(sort_type, sku_list, limit)


def _get_index_by_sort_type(
    sort_type: str, sku_list: List, limit: int
) -> Dict[int, int | str]:
    if len(sku_list) % limit == 0:
        page = len(sku_list) // limit
    else:
        page = len(sku_list) // limit + 1

    sku_list = list(map(lambda x: x[0], sku_list))
    print("-----_get_index_by_sort_type-----")
    print("sku_list", sku_list)
    return {i + 1: int(sku_list[i * limit] + 1) for i in range(0, page)}
