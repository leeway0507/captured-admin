from typing import List, Dict
from router.product import utils as product_utils
from router.production import utils as admin_utils
from sqlalchemy.ext.asyncio import AsyncSession
from model.product_model import RequestFilterSchema
from typing import Optional
from model.db_model import ProductInfoSchema, ProductInfoDBSchema, SizeSchema


async def test_get_filtered_item_list(
    db: AsyncSession,
    page: int,
    filter: Optional[RequestFilterSchema] = None,
):
    """리스트 불러오기"""
    return await product_utils.get_category(db, page, filter)


async def test_get_a_single_product(db: AsyncSession, sku: int) -> ProductInfoSchema:
    """제품 정보 불러오기"""
    result = await product_utils.get_product(sku=sku, db=db)
    if result is None:
        raise Exception("제품 정보가 없습니다.")
    return result


def test_get_init_meta():
    return product_utils.get_init_meta_data()


async def create_product(product: ProductInfoSchema, db: AsyncSession):
    """제품 생성"""
    product.sku = await admin_utils.create_new_sku(db)
    search_info = product.brand + " " + product.product_name + " " + product.product_id
    price = product.price
    sku = product.sku
    price_desc_cursor = str(price).zfill(7) + str(sku).zfill(5)
    price_asc_cursor = str(100000000000 - int(price_desc_cursor))

    product_info_db = ProductInfoDBSchema(
        search_info=search_info,
        price_desc_cursor=price_desc_cursor,
        price_asc_cursor=price_asc_cursor,
        **product.model_dump(),
    )

    if await admin_utils.create_product(db, product_info_db):
        return {"message": "success"}
    else:
        raise Exception("제품 등록 실패. 다시 시도해주세요.")


async def update_product(product_in_db: ProductInfoDBSchema, db: AsyncSession):
    """제품 수정"""
    if await admin_utils.update_product(db=db, product=product_in_db):
        return {"message": "success"}
    else:
        raise Exception("제품 업데이트에 실패했습니다. 다시 시도해주세요.")


async def delete_product(product: ProductInfoSchema, db: AsyncSession):
    """제품 삭제"""
    if product.sku == None:
        raise Exception("제품정보에 SKU가 존재하지 않아 삭제할 수 없습니다.")
    if await admin_utils.delete_product(db, product.sku):
        return {"message": "success"}
    else:
        raise Exception("제품 삭제에 실패했습니다. 다시 시도해주세요.")


async def create_size(db: AsyncSession, sku: int, size: List[str]):
    """사이즈 생성"""
    if await admin_utils.create_size(db, sku, size):
        return {"message": "success"}
    else:
        raise Exception("사이즈 등록 실패. 다시 시도해주세요.")


async def update_size(db: AsyncSession, size_list: List[Dict[str, str]]):
    """사이즈 수정"""
    if await admin_utils.update_size(db, size_list):
        return {"message": "success"}
    else:
        raise Exception("사이즈 수정 실패. 다시 시도해주세요.")


async def delete_size(db: AsyncSession, sku: int):
    """사이즈 삭제"""
    if await admin_utils.delete_size(db, sku):
        return {"message": "success"}
    else:
        raise Exception("사이즈 삭제 실패. 다시 시도해주세요.")
