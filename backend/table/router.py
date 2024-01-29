from typing import Dict, Any
from .table_candidate import CandidateTable
from .table_production import ProductionTable
from .table_size import SizeTable
from .table_kream import KreamTable
from fastapi import APIRouter, Request
from model.shop_model import updateShopProductCardSchema
from model.db_model_production import ProductInfoSchema

# /api/table/
table = APIRouter()

candidate_table = CandidateTable()
production_table = ProductionTable()
size_table = SizeTable()
kream_table = KreamTable()


@table.get("/candidate")
async def get_candidate_table(searchType: str, content: str):
    return await candidate_table.get(searchType, content.replace("%20", " "))


@table.patch("/candidate")
async def patch_candidate_table(shopProductCardId: int, column: str, content: str):
    return await candidate_table.patch(shopProductCardId, column, content)


@table.put("/candidate")
async def put_candidate_table(request: Request):
    json_dict = await request.json()
    shopProductCardId = json_dict["shopProductCardId"]
    value = updateShopProductCardSchema(**json_dict["value"])
    return await candidate_table.put(shopProductCardId, value.model_dump())


@table.delete("/candidate/{shopProductCardId}")
async def delete_candidate_table(shopProductCardId: int):
    return await candidate_table.delete(shopProductCardId)


@table.get("/production")
async def get_production_table(page: int):
    return await production_table.get(page=page)


@table.post("/production")
async def post_production_table(data: ProductInfoSchema):
    return await production_table.post(data)


@table.patch("/production")
async def patch_production_table(sku: int, column: str, value: str):
    return await production_table.patch(sku, column, value)


@table.patch("/production/image/{sku}")
def production_table_update_image(sku: int, fileName: str):
    return production_table.update_image(str(sku), fileName)


@table.patch("/production/thumbnail-meta")
def production_table_update_thumbnail():
    return production_table.update_thumbnail_meta()


@table.put("/production")
async def put_production_table(data: ProductInfoSchema):
    del data.size

    return await production_table.put(data.model_dump())


@table.put("/production/image/{sku}")
def production_table_upload_image(sku: int):
    return production_table.upload_image(str(sku))


@table.put("/production/thumbnail")
def production_table_upload_thumbnail():
    return production_table.upload_thumbnail()


@table.delete("/production/{sku}")
async def delete_production_table(sku: int):
    return await production_table.delete(sku)


@table.get("/size/{shopProductCardId}")
async def get_size_table(shopProductCardId: str):
    return await size_table.get(shopProductCardId)


@table.get("/kream/product/{type}/{content}")
async def get_kream_table(type: str, content: str):
    return await kream_table.get_kream_prod_card(type, content)


@table.get("/kream/market-price/{productId}")
async def get_market_price_info(productId: str):
    return await kream_table.get_market_price_info(productId)
