"""size_scrap Router"""

from fastapi import APIRouter
from .utils import *

size_batch_router = APIRouter()


@size_batch_router.put("/update-batch")
async def update_batch_api():
    """사이즈 수집 결과를 production size Table에 반영"""
    return await update_batch()


@size_batch_router.get("/save-raw-data-for-size-batch")
async def save_raw_data_for_size_batch():
    """production size table에 반영할 데이터 다운로드"""
    return await save_raw_data()


@size_batch_router.get("/preprocess-data-for-size-batch")
def preprocess_data_to_size_table():
    """production size table에 반영할 데이터 전처리"""
    return preprocess_data()


@size_batch_router.put("/update-size-table-to-db")
async def update_size_table_to_db(batch_name: Optional[str] = None):
    """batch_name결과 production size table에 반영"""
    return await update_size_table(batch_name)


@size_batch_router.put("/update-dev-db-table")
async def update_dev_db_table():
    """production 테이블 정보를 dev 테이블에 동기화"""
    return await update_dev_db()
