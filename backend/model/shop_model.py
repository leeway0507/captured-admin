from pydantic import BaseModel, validator, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel
from typing import List, Optional, Dict


class ShopProductId(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    shop_product_card_id: int
    product_id: str


class RequestShopInfo(BaseModel):
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
