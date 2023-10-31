import sys

sys.path.append("/Users/yangwoolee/repo/captured/main/backend")
from datetime import datetime
from sqlalchemy import delete


from test_module.product import *
from variables import get_product_info, get_filter
from model.db_model import ProductInfoDBSchema
from db.tables import ProductInfoTable, SizeTable
from sqlalchemy.ext.asyncio import AsyncSession


# test_variables
product_info = get_product_info()
filter = get_filter()


async def product_scenario(db):
    print("----------product_scenario 시작----------")
    # 제품 Create
    await test_product_create(db=db, product=product_info)

    # 제품 Read
    last_row = await get_last_product(db=db)
    sku = last_row.sku
    assert sku != None, "SKU가 생성되지 않았습니다."

    # 제품 사이즈 CRUD
    await test_product_size_create(db=db, sku=sku)
    await test_product_size_update(db=db, sku=sku)
    await test_product_size_delete(db=db, sku=sku)

    # 제품 Update & Delete
    await test_product_size_create(db=db, sku=sku)
    await test_product_update(db=db)

    # 제거
    await delete_product_size_force(db=db)
    await delete_product_force(db=db)
    print("----------product_scenario 종료----------")


# Part --------------------------------------------------------------


async def get_last_product(db: AsyncSession):
    result = await db.execute("select * from product_info order by sku desc limit 1")
    result = result.all()
    return ProductInfoDBSchema(**result[0])


async def get_size_list(db: AsyncSession, sku: int):
    result = await db.execute(f"select * from size where sku = {sku}")
    result = result.all()

    return [SizeSchema(**row) for row in result]


async def test_product_create(db: AsyncSession, product: ProductInfoSchema):
    result = await create_product(product, db=db)
    print(result)

    last_row = await get_last_product(db)

    assert (
        last_row.brand == product_info.brand
        and last_row.product_name == product_info.product_name
        and last_row.product_id == product_info.product_id
    ), f"제품 생성 실패"

    print("----------test_create 성공----------")


async def test_product_size_create(db: AsyncSession, sku: int):
    # test_create_size
    init_size = ["230", "240", "250"]
    await create_size(db=db, sku=sku, size=init_size)
    result = await test_get_a_single_product(db=db, sku=sku)

    assert result.size != None, f"제품 생성 실패"
    size_data = sorted(result.size.split(","))

    assert size_data == init_size, f"제품 사이즈 결과가 다릅니다. : {size_data} \n 실제 사이즈 {init_size}"

    print("----------test_create_size 성공----------")
    return None


async def test_product_size_update(db: AsyncSession, sku: int):
    # test_update_size
    size_list = ["230", "240", "250", "260", "270"]
    size_schema_obj_list = [
        SizeSchema(sku=sku, size=size, updated_at=datetime.now(), available=False).model_dump()
        for size in size_list
    ]
    await update_size(db=db, size_list=size_schema_obj_list)
    size_data = await get_size_list(db=db, sku=sku)
    assert len(size_data) == len(size_list), f"사이즈 업데이트 실패"
    print("----------test_update_size 성공----------")
    return None


async def test_product_size_delete(db: AsyncSession, sku: int):
    # test_delete_size
    await delete_size(db=db, sku=sku)
    size_data = await get_size_list(db=db, sku=sku)
    assert len(size_data) == 0, f"사이즈 삭제 실패"
    print("----------test_delete_size 성공----------")
    return None


async def test_product_update(db: AsyncSession):
    """제품 업데이트 테스트
    -foreign constraint-
    product를 업데이트 하거나 지우기 위해서는 자식 테이블인 size 테이블의 데이터를 제거해야함.
    테이블에 해당 sku 사이즈가 존재하는지 확인하고, 존재하면 삭제 후 다시 생성해야함.
    """

    # 업데이트 테스트
    update_row = await get_last_product(db)
    update_row.brand = "adidas"
    update_row.product_name = "adidas superstar"
    update_row.product_id = "gy7000"
    await update_product(product_in_db=update_row, db=db)

    # 사이즈 복구 되는지 확인
    last_row = await get_last_product(db)
    assert (
        last_row.brand == update_row.brand
        and last_row.product_name == update_row.product_name
        and last_row.product_id == update_row.product_id
    ), f"""제품 수정 실패"""

    assert isinstance(last_row.sku, int), f"""sku is None"""
    size_list = await get_size_list(db=db, sku=last_row.sku)
    assert len(size_list) != 0, f"""사이즈 복구 실패"""

    print("----------product_update 성공----------")


async def delete_product_size_force(db: AsyncSession):
    stmt = delete(SizeTable)
    await db.execute(stmt)
    await db.commit()


async def delete_product_force(db: AsyncSession):
    stmt = delete(ProductInfoTable)
    await db.execute(stmt)
    await db.commit()
