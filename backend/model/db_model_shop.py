"""pydantic Schemas"""
import re
from typing import Optional

from pydantic import BaseModel, field_validator
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ShopInfoSchema(BaseModel):
    """ShopInfoTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # id
    shop_name: str
    shop_url: str
    tax_reduction_rate: Optional[float] = None
    del_agc_tax_reduction_rate: Optional[float] = None
    dome_ship_price: Optional[int] = None
    intl_ship_price: Optional[int] = None
    from_us_shipping: Optional[bool] = None
    is_ddp: Optional[bool] = None
    country: Optional[str] = None
    updated_at: datetime

    @field_validator("shop_name")
    def convert_to_lower(cls, value):
        return value.lower()


class ShopInBrandSchema(BaseModel):
    """ShopInBrandTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    # id
    shop_name: str
    brand_name: str
    brand_url: str
    updated_at: datetime

    @field_validator("shop_name", "brand_name")
    def convert_to_lower(cls, value):
        return value.lower()


class ShopProductCardSchema(BaseModel):
    """ShopProductCardTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    shop_product_name: str
    shop_product_img_url: str
    product_url: str
    shop_name: str
    brand_name: str
    product_id: Optional[str] = None
    kor_price: int
    us_price: float
    original_price_currency: str
    original_price: float
    sold_out: Optional[bool] = False
    candidate: Optional[bool] = False
    updated_at: datetime

    @field_validator("shop_name", "brand_name", "shop_product_name")
    def convert_to_lower(cls, value):
        return value.lower()

    @field_validator("product_id")
    def convert_to_upper(cls, value):
        if value is None:
            return None
        return value.upper()


class ShopProductSizeSchema(BaseModel):
    """ShopProductSizeTable schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # size_id
    shop_product_card_id: str
    shop_product_size: str
    kor_product_size: str
    available: bool
    updated_at: datetime
