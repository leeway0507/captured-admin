import re
from datetime import datetime

from pydantic import ConfigDict, BaseModel, field_validator
from pydantic.alias_generators import to_camel


class KreamScrapingBrandSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    kream_id: int
    kream_product_img_url: str
    kream_product_name: str
    brand_name: str
    trading_volume: int
    wish: int
    review: int
    updated_at: datetime


class KreamProductDetailSchema(BaseModel):
    kream_id: int
    kream_product_img_url: str
    kream_product_name: str
    brand_name: str
    product_id: str
    retail_price: int
    product_release_date: datetime
    color: str
    wish: int
    review: int
    updated_at: datetime

    @field_validator("kream_id", mode="before")
    def convert_str_int(cls, value: str):
        return int(value)

    @field_validator("brand_name", "kream_product_name")
    def convert_to_lower(cls, value):
        return value.lower()

    @field_validator("retail_price", mode="before")
    def extract_price(cls, value: str):
        if isinstance(value, int):
            return value
        match = re.search(r"\(([^)]+)\)", value)
        if match:
            value = match.group(1)

        value = re.sub(r"\D", "", value)
        return int(value)

    @field_validator("product_release_date", mode="before")
    def change_str_to_date(cls, value: str):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%y/%m/%d")

    @field_validator("updated_at", mode="before")
    def change_str_to_datetime(cls, value: str):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
