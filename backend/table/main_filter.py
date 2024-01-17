from typing import List, Dict, Any, Optional
from db.tables_production import ProductInfoTable, SizeTable
from db.production_db import prod_session_local as session_local
from sqlalchemy import select


# @alru_cache()
async def get_page_idx(
    limit: int,
    sort_by: str = "최신순",
    category: Optional[str] = None,
    category_spec: Optional[str] = None,
    brand: Optional[str] = None,
    intl: Optional[str] = None,
    price: Optional[str] = None,
    size_array: Optional[str] = None,
):
    sort_type, column, order_by = create_order_by_filter(sort_by)

    filter = create_filter_query_dict(
        category, category_spec, brand, intl, price, size_array
    )
    print("적용된 필터 종류")
    print(filter.keys())

    if "size_array_filter" in filter.keys():
        stmt = (
            select(column)
            .join(SizeTable, ProductInfoTable.sku == SizeTable.sku)
            .where(
                *filter.values(),
                SizeTable.available == 1,
            )
            .group_by(ProductInfoTable.sku)
            .order_by(*order_by)
        )
    else:
        stmt = select(column).where(*filter.values()).order_by(*order_by)
    db = session_local()
    sku_list = await db.execute(stmt)
    sku_list = sku_list.all()
    await db.close()  # type: ignore

    if not sku_list:
        return {}
    page_idx = _get_index_by_sort_type(sort_type, sku_list, limit)
    print("page_idx", page_idx)
    return page_idx


# @lru_cache()
def create_filter_query_dict(
    category: Optional[str] = None,
    category_spec: Optional[str] = None,
    brand: Optional[str] = None,
    intl: Optional[str] = None,
    price: Optional[str] = None,
    size_array: Optional[str] = None,
    *args: Any,
    **kwargs: Any,
):
    f_d = {
        "category_filter": None,
        "category_spec_filter": None,
        "brand_filter": None,
        "intl_filter": None,
        "price_filter": None,
        "size_array_filter": None,
    }

    if category:
        f_d["category_filter"] = ProductInfoTable.category.in_(category.split(","))
    if category_spec:
        f_d["category_spec_filter"] = ProductInfoTable.category_spec.in_(
            category_spec.split(",")
        )
    if brand:
        f_d["brand_filter"] = ProductInfoTable.brand.in_(brand.split(","))
    if intl:
        l = list(map(lambda x: True if x == "해외배송" else False, intl.split(",")))
        f_d["intl_filter"] = ProductInfoTable.intl.in_(l)
    if price:
        l = create_price_range(price)
        f_d["price_filter"] = ProductInfoTable.price.between(l[0], l[1])
    if size_array:
        f_d["size_array_filter"] = SizeTable.size.in_(size_array.split(","))

    filter = {k: v for k, v in f_d.items() if v is not None}
    return filter


def create_order_by_filter(sort_by: str | None = None) -> List:
    """sort_by에 맞는 order_by query 생성"""
    if sort_by == "높은 가격 순":
        return [
            "높은 가격 순",
            ProductInfoTable.price_desc_cursor,
            [ProductInfoTable.price.desc(), ProductInfoTable.sku.desc()],
        ]

    if sort_by == "낮은 가격 순":
        return [
            "낮은 가격 순",
            ProductInfoTable.price_asc_cursor,
            [ProductInfoTable.price.asc(), ProductInfoTable.sku.asc()],
        ]

    # if sort_by == "최신순" or sort_by == "인기순" or not sort_by:
    else:
        return ["최신순", ProductInfoTable.sku, [ProductInfoTable.sku.desc()]]


def create_price_range(price: str) -> List[int]:
    price_list = price.split(",")

    if len(price_list) != 2:
        raise ValueError("price는 2개의 원소를 가져야 합니다.")

    price_list = list(map(int, price_list))

    if not isinstance(price_list[0], int) or not isinstance(price_list[1], int):
        raise ValueError("price의 원소는 int여야 합니다.")

    if price_list == [0, 0]:
        return []

    return sorted(price_list)


def _get_index_by_sort_type(
    sort_type: str, sku_list: List, limit: int
) -> Dict[int, int | str]:
    if len(sku_list) % limit == 0:
        page = len(sku_list) // limit
    else:
        page = len(sku_list) // limit + 1

    if sort_type in ["높은 가격 순", "낮은 가격 순"]:
        # 높은 가격 순 일 땐 12자리?, 낮은 가격 순 일 땐 11자리를 맞춰줘야함.
        # zfill_value = 11 if sort_type == "높은 가격 순" else 11

        zfill_value = 11
        cursor_idx_list = list(map(lambda x: int(x[0]), sku_list))
        return {
            i + 1: str(cursor_idx_list[i * limit] + 1).zfill(zfill_value)
            for i in range(0, page)
        }

    else:
        sku_list = list(map(lambda x: x[0], sku_list))
        return {i + 1: int(sku_list[i * limit] + 1) for i in range(0, page)}
