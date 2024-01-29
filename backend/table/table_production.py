from typing import Dict, List
from db.tables_production import ProductInfoTable
from db.production_db import ProdDB
from . import main_utils
from model.db_model_production import ProductInfoDBSchema, ProductInfoSchema
from components.image_resize import ImageResizeManager, S3ThumbnailUploader
from sqlalchemy import update, insert, select
from components.env import prod_env


class ProductionTable:
    def __init__(self) -> None:
        self.prod_db = ProdDB()
        self.image_manager = ImageResizeManager(prod_env.PRODUCT_IMAGE_DIR)
        self.thumbnail_uploader = S3ThumbnailUploader(prod_env.PRODUCT_THUMBNAIL_DIR)

    async def get(self, page: int):
        return await main_utils.get_production_table_data(page=page)

    async def delete(self, sku: int):
        stmt = (
            update(ProductInfoTable)
            .where(ProductInfoTable.sku == sku)
            .values(deploy=-1)
        )
        return await self.prod_db.execute_and_commit(stmt)

    async def put(self, value: Dict):
        stmt = (
            update(ProductInfoTable)
            .where(ProductInfoTable.sku == value["sku"])
            .values(**value)
        )
        return await self.prod_db.execute_and_commit(stmt)

    async def patch(self, sku: int, column: str, value: str) -> None:
        stmt = (
            update(ProductInfoTable)
            .where(ProductInfoTable.sku == sku)
            .values({column: value})
        )
        return await self.prod_db.execute_and_commit(stmt)

    async def post(self, value: ProductInfoSchema):
        sku = await self.create_new_sku()
        value.sku = sku
        value.search_info = f"{value.brand} {value.kor_brand} {value.product_name} {value.kor_product_name} {value.product_id}"
        price = value.price
        price_desc_cursor = str(price).zfill(7) + str(sku).zfill(5)
        price_asc_cursor = str(100000000000 - int(price_desc_cursor))

        new_data = ProductInfoDBSchema(
            price_desc_cursor=price_desc_cursor,
            price_asc_cursor=price_asc_cursor,
            **value.model_dump(),
        )
        stmt = insert(ProductInfoTable).values(new_data.model_dump())
        await self.prod_db.execute_and_commit(stmt)
        return new_data

    async def create_new_sku(self):
        column = ProductInfoTable.sku
        stmt = select(column).order_by(column.desc()).limit(1)
        last_number = await self.prod_db.execute(stmt)
        if last_number == None:
            return 1

        return last_number[0][0] + 1

    def upload_image(self, sku: str):
        return self.image_manager.execute(sku)

    def update_image(self, sku: str, file_name: str):
        return self.image_manager.update_image(sku, file_name)

    def upload_thumbnail(self):
        return self.thumbnail_uploader.upload_all()

    def update_thumbnail_meta(self):
        return self.thumbnail_uploader.update_meta()
