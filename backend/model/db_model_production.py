"""pydantic Schemas"""


from typing import Optional
from datetime import datetime


from pydantic import BaseModel, validator, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel


from model.order_model import OrderHistoryRequestSchema, OrderRowRequestchmea


class ProductInfoSchema(BaseModel):
    """ProductInfoTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    sku: Optional[int] = None
    brand: str
    product_name: str
    product_id: str
    price: int
    shipping_fee: int
    intl: bool
    color: str  # List[str]
    category: str
    category_spec: str
    img_type: str

    # @validator("size", "color", pre=True)
    @validator("color", pre=True)
    def str_to_list(cls, v: str) -> str:
        """str to list to str"""
        return v.replace(",", "/")


class ProductInfoDBSchema(ProductInfoSchema):
    """ProductInfoTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    ## productInfoSchema는 request, response로 사용 중임.
    ## 이때 size 항목이 포함되는데 productInfoTable은 size 컬럼이 없음. 따라서 exclude로 제거해야함.
    size: Optional[str] = Field(default=None, exclude=True)
    price_desc_cursor: str
    price_asc_cursor: str
    search_info: Optional[str] = None
    deploy: Optional[int] = 0


class SizeSchema(BaseModel):
    """SizeTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    sku: int
    size: str
    available: bool
    updated_at: datetime


class UserSchema(BaseModel):

    """User Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    user_id: str
    email: Optional[EmailStr] = None
    kr_name: str
    email_verification: bool
    sign_up_type: str


class UserIndDBSchema(UserSchema):
    """User Schema in DB"""

    register_at: datetime
    password: Optional[str] = None


class UserAddressSchema(BaseModel):
    """UserAddresTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    address_id: Optional[str] = None  # UA-[user_id]-[0~n]
    kr_name: str
    en_name: str
    custom_id: str
    phone: str
    kr_address: str
    kr_address_detail: str
    en_address: str
    en_address_detail: str


class UserAddressInDBSchema(UserAddressSchema):
    """UserAddresTable Schema"""

    user_id: Optional[str] = None
    permanent: bool = False


class OrderHistoryInDBSchema(OrderHistoryRequestSchema):
    """OrderHistoryTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    address_id: str
    user_id: str
    user_order_number: int
    order_status: str = "배송준비"  # 배송준비/배송중/배송완료/반품중/취소요청/환불완료
    payment_status: str = "승인완료"  # 승인대기/승인완료/결제취소


class OrderRowInDBSchmea(OrderRowRequestchmea):
    """OrderRowTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    order_row_id: Optional[int] = Field(default=None)
    delivery_status: Optional[str] = "배송준비"
    delivery_company: Optional[str] = None
    delivery_number: Optional[str] = None
