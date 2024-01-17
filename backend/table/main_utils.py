from typing import Tuple, Dict, Optional
import json

from sqlalchemy import and_, func, select, text

from db.tables_production import ProductInfoTable, SizeTable

from model.db_model_production import ProductInfoSchema, ProductInfoDBSchema
from model.product_model import ProductResponseSchema
from .main_filter import (
    create_order_by_filter,
    create_filter_query_dict,
    get_page_idx,
)
from db.production_db import prod_session_local as session_local

from sqlalchemy.ext.asyncio import AsyncSession


async def get_production_table_data(
    sort_by: str = "최신순",
    category: Optional[str] = None,
    category_spec: Optional[str] = None,
    brand: Optional[str] = None,
    intl: Optional[str] = None,
    price: Optional[str] = None,
    size_array: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
) -> ProductResponseSchema:
    request_filter = {
        "sort_by": sort_by,
        "category": category,
        "category_spec": category_spec,
        "brand": brand,
        "intl": intl,
        "price": price,
        "size_array": size_array,
    }

    page_idx = await get_page_idx(**request_filter, limit=limit)

    current_cursor, last_page = await get_page_cursor(page, page_idx)

    if current_cursor == -1:
        """필터 결과 없음"""
        return ProductResponseSchema(data=[], currentPage=0, lastPage=last_page)

    filter = create_filter_query_dict(**request_filter)
    sort_type, column, order_by = create_order_by_filter(request_filter.get("sort_by"))

    # group_by
    group_by = SizeTable.sku
    if "size_array" in filter.keys():
        group_by = ProductInfoTable.sku

    db = session_local()
    result = await db.execute(
        select(ProductInfoTable, func.group_concat(SizeTable.size).label("size"))
        .join(SizeTable, ProductInfoTable.sku == SizeTable.sku)
        .where(
            *filter.values(),
            column < current_cursor,
            SizeTable.available == 1,
            ProductInfoTable.deploy != -1,
        )
        .group_by(group_by)
        .order_by(*order_by)
        .limit(limit)
    )
    await db.close()  # type: ignore

    data = [
        ProductInfoDBSchema(**row[0].to_dict(), size=row[1]).model_dump(by_alias=True)
        for row in result
    ]
    return ProductResponseSchema(data=data, currentPage=page, lastPage=last_page)


async def get_page_cursor(
    page: int, page_idx: Dict[int, int | str]
) -> Tuple[int | str, int]:
    """page index에서 페이지에 해당하는 sku를 추출"""

    # 제품이 없는 경우
    if not page_idx:
        return -1, 0

    # 마지막 페이지보다 큰 값을 요구할 경우 경우
    last_page = max(page_idx.keys())
    if page > last_page:
        return -1, last_page

    # print("page_idx 정상적으로 기입되는지 확인 ", "page : ", page, "page_index : ", page_idx)
    return page_idx[page], last_page
