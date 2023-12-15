from typing import Optional
import os
from pathlib import Path


from sqlalchemy import select, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from db.dev_db import session_local as dev_session, conn_engine, sessionmaker
from db.production_db import session_local as prod_session
from db.tables_shop import ShopProductSizeTable, ShopProductCardTable
from db.tables_production import ProductInfoTable, SizeTable

from env import prod_env


async def get_shop_product_size_table():
    db = dev_session()
    stmt = select(ShopProductSizeTable)
    result = await db.execute(stmt)
    result = result.scalars().all()
    await db.close()  # type: ignore
    return [row.to_dict() for row in result]


async def get_shop_product_card_table():
    db = dev_session()
    # candidate == 2 : 사이즈 수집 상태인 데이터
    stmt = select(ShopProductCardTable).where(ShopProductCardTable.candidate == 2)
    result = await db.execute(stmt)
    result = result.scalars().all()
    await db.close()  # type: ignore
    return [row.to_dict() for row in result]


async def get_product_info_table():
    db = prod_session()
    # deploy == 1 : 판매중인 데이터
    stmt = select(ProductInfoTable).where(ProductInfoTable.deploy == 1)
    result = await db.execute(stmt)
    result = result.scalars().all()
    await db.close()  # type: ignore
    return [row.to_dict() for row in result]


async def save_raw_data():
    path = prod_env.PRODUCTION_SIZE_BATCH
    assert isinstance(path, str), "path is not str"

    data = await get_shop_product_size_table()
    shop_product_size_table = pd.DataFrame(data)

    #### Batch Date 설정 ####
    batch_date = (
        shop_product_size_table["updated_at"]
        .sort_values()
        .tail(1)
        .iloc[0]
        .strftime("%Y%m%d-%H%M%S")
    )
    print("batch_date : ", batch_date)
    create_folder(path, batch_date)
    #### Batch Date 설정 ####

    shop_product_size_table.to_parquet(
        os.path.join(path, batch_date, "shop_product_size_table.parquet.gzip"),
        index=False,
        compression="gzip",
    )
    print("shop_product_size_table 저장 성공")

    data = await get_shop_product_card_table()
    shop_product_card_table = pd.DataFrame(data)
    shop_product_card_table.to_parquet(
        os.path.join(path, batch_date, "shop_product_card_table.parquet.gzip"),
        index=False,
        compression="gzip",
    )
    print("shop_product_card_table 저장 성공")

    data = await get_product_info_table()
    product_info_table = pd.DataFrame(data)
    product_info_table.to_parquet(
        os.path.join(path, batch_date, "product_info_table.parquet.gzip"),
        index=False,
        compression="gzip",
    )
    print("shop_product_info_table 저장 성공")
    return {"message": "success"}


def preprocess_data(batch_date: Optional[str] = None):
    path = prod_env.PRODUCTION_SIZE_BATCH
    assert isinstance(path, str), "path is not str"

    if batch_date is None:
        path, batch_date = get_last_batch_folder()

    product_info_table = pd.read_parquet(
        os.path.join(path, batch_date, "product_info_table.parquet.gzip"),
    )

    shop_product_card_table = pd.read_parquet(
        os.path.join(path, batch_date, "shop_product_card_table.parquet.gzip"),
    )

    shop_product_size_table = pd.read_parquet(
        os.path.join(path, batch_date, "shop_product_size_table.parquet.gzip"),
    )

    sku_prod_id = product_info_table[["sku", "product_id"]]
    prod_id_sh_prod_id = shop_product_card_table[["product_id", "shop_product_card_id"]]
    sku_prod_id_sh_pro_id = pd.merge(
        prod_id_sh_prod_id, sku_prod_id, on="product_id", how="inner"
    )
    print("sku product_id shop_product_card_id Map 생성 완료")

    size_table = pd.merge(
        sku_prod_id_sh_pro_id,
        shop_product_size_table,
        on="shop_product_card_id",
        how="left",
    )

    size_table: pd.DataFrame = size_table[["sku", "kor_product_size", "updated_at"]]  # type: ignore
    size_table = size_table.drop_duplicates(subset=["sku", "kor_product_size"])
    size_table["available"] = 1
    print("size_table 생성 완료")

    size_table.rename(columns={"kor_product_size": "size"}, inplace=True)

    size_table.to_parquet(
        os.path.join(path, batch_date, "update_to_prod_size_table.parquet.gzip"),
        compression="gzip",
    )
    print(f"size_table 저장 완료 : {path}/{batch_date}")


async def update_size_table(batch_date: Optional[str] = None):
    """테스트 안해봄"""
    path = prod_env.PRODUCTION_SIZE_BATCH
    assert isinstance(path, str), "path is not str"

    if batch_date is None:
        path, batch_date = get_last_batch_folder()

    size_table = pd.read_parquet(
        os.path.join(path, batch_date, "update_to_prod_size_table.parquet.gzip"),
    )
    unique_sku = size_table["sku"].unique()

    db: AsyncSession = prod_session()  # type: ignore
    stmt = select(SizeTable).where(SizeTable.sku.in_(unique_sku))
    result = await db.execute(stmt)
    result = result.scalars().all()
    for row in result:
        row.available = 0
        row.updated_at = size_table["updated_at"][0]

    stmt = insert(SizeTable).values(size_table.to_dict("records"))
    stmt = stmt.on_duplicate_key_update(
        available=stmt.inserted.available,
        updated_at=stmt.inserted.updated_at,
    )

    await db.execute(stmt)
    await db.commit()
    await db.close()  # type: ignore
    return {"message": "success"}


async def update_batch():
    await save_raw_data()
    print("save_raw_data 완료")

    preprocess_data()
    print("preprocess_data 완료")

    await update_size_table()
    print("update_size_table 완료")

    return {"message": "success"}


async def update_dev_db():
    path, last_batch_date = get_last_batch_folder()
    size_table = pd.read_parquet(
        os.path.join(path, last_batch_date, "update_to_prod_size_table.parquet.gzip"),
    )
    product_info_table = pd.read_parquet(
        os.path.join(path, last_batch_date, "product_info_table.parquet.gzip"),
    )

    db: AsyncSession = connect_to_captured_dev()  # type: ignore
    stmt = delete(SizeTable)
    await db.execute(stmt)
    print("dev size table delete 완료")
    stmt = delete(ProductInfoTable)
    await db.execute(stmt)
    print("dev product_info table delete 완료")

    stmt = insert(ProductInfoTable).values(product_info_table.to_dict("records"))
    await db.execute(stmt)
    print("dev product_info table insert 완료")

    stmt = insert(SizeTable).values(size_table.to_dict("records"))
    await db.execute(stmt)
    print("dev size table insert 완료")

    await db.commit()
    await db.close()  # type: ignore
    print("update dev db 완료")


def get_last_batch_folder():
    path = prod_env.PRODUCTION_SIZE_BATCH
    assert isinstance(path, str), "path is not str"

    lst = os.listdir(path)
    lst.pop(lst.index("_.ipynb"))
    lst.pop(lst.index(".DS_Store"))
    print("lst : ", lst)
    last_batch_date = lst[0]

    print("last_batch_date : ", last_batch_date)
    return path, last_batch_date


def connect_to_captured_dev():
    DB_USER_NAME = "root"
    DB_PASSWORD = ""
    DB_HOST = "localhost"
    DB_NAME = "captured_dev"
    db_engine = conn_engine(DB_USER_NAME, DB_PASSWORD, DB_HOST, DB_NAME)
    session_local = sessionmaker(bind=db_engine, class_=AsyncSession)  # type: ignore
    return session_local()


def create_folder(root_dir: str, name: str):
    resize_folder = os.path.join(root_dir, name)
    Path(resize_folder).mkdir(parents=True, exist_ok=True)
    return resize_folder
