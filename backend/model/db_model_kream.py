"""pydantic Schemas"""
import re
from typing import Optional

from pydantic import BaseModel, field_validator
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class KreamProductCardSchema(BaseModel):
    """KreamProductCardTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    kream_id: int
    brand_name: str
    kream_product_name: str
    kream_product_img_url: str
    retail_price: Optional[int] = None
    product_release_date: Optional[datetime] = None
    trading_volume: Optional[int] = None
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

    @field_validator("updated_at", mode="before")
    def change_str_to_datetime(cls, value: str):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


class KreamTradingVolumeSchema(BaseModel):
    """KreamTradingVolumeTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # volume_id: int
    kream_id: int
    kream_product_size: str
    price: int
    lightening: bool
    trading_at: datetime

    @field_validator("trading_at", mode="before")
    def change_str_to_datetime(cls, value: str):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%y/%m/%d")

    @field_validator("price", mode="before")
    def extract_price(cls, value: str):
        if isinstance(value, int):
            return value

        match = re.search(r"\(([^)]+)\)", value)
        if match:
            value = match.group(1)

        value = re.sub(r"\D", "", value)
        return int(value)


class KreamBuyAndSellSchema(BaseModel):
    """KreamBuyAndSellTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # volume_id: int
    kream_id: int
    kream_product_size: str
    buy: int
    sell: int
    updated_at: datetime


class KreamProductIdBridgeSchmea(BaseModel):
    """KreamProductIdBridgeTable Schema"""

    product_id: str
    kream_id: Optional[int] = None

    @field_validator("product_id")
    def convert_to_upper(cls, value):
        return value.upper()
