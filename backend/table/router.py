from typing import Dict
from .table_candidate import CandidateTable
from .table_production import ProductionTable
from .table_size import SizeTable
from fastapi import APIRouter
from model.shop_model import updateShopProductCardSchema
from model.db_model_production import ProductInfoSchema

# /api/table/
table = APIRouter()

candidate_table = CandidateTable()
production_table = ProductionTable()
size_table = SizeTable()


@table.get("/candidate-table")
async def get_candidate_table(searchType: str, content: str):
    return await candidate_table.get(searchType, content.replace("%20", " "))


@table.patch("/candidate-table")
async def patch_candidate_table(shopProductCardId: int, column: str, content: str):
    return await candidate_table.patch(shopProductCardId, column, content)


@table.put("/candidate-table")
async def put_candidate_table(
    shopProductCardId: int, value: updateShopProductCardSchema
):
    return await candidate_table.put(shopProductCardId, value.model_dump())


@table.delete("/candidate-table/{shopProductCardId}")
async def delete_candidate_table(shopProductCardId: int):
    return await candidate_table.delete(shopProductCardId)


@table.get("/production-table")
async def get_production_table(page: int):
    return await production_table.get(page=page)


@table.patch("/production-table")
async def patch_production_table(sku: int, column: str, value: str):
    return await production_table.patch(sku, column, value)


@table.put("/production-table")
async def put_production_table(data: ProductInfoSchema):
    del data.size

    return await production_table.put(data.model_dump())


@table.delete("/production-table/{sku}")
async def delete_production_table(sku: int):
    return await production_table.delete(sku)


@table.get("/size-table/{productId}")
async def get_size_table(productId: str):
    return await size_table.get(productId)
