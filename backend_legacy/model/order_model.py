"""pydantic Schemas"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from typing import List, Optional
from datetime import datetime


class OrderRowRequestchmea(BaseModel):
    """OrderRowTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    order_id: str
    sku: int
    size: str
    quantity: int


class OrderHistoryRequestSchema(BaseModel):
    """OrderHistoryTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    payment_key: str
    order_id: str
    ordered_at: datetime
    order_total_price: int
    payment_method: str
    payment_info: Optional[str] = None  # hash # 카드번호 & 계좌번호 등..


class OrderInfoBeforePaymentSchema(BaseModel):
    """SizeTable Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    order_id: str
    address_id: str
    order_total_price: int
    order_rows: List[OrderRowRequestchmea]


class OrderHistoryResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    order_id: str
    user_order_number: int
    ordered_at: datetime
    order_status: str = "배송준비"  # 배송준비/배송중/배송완료/반품중/취소요청/환불완료
    payment_status: str = "승인완료"  # 승인대기/승인완료/결제취소
    address_id: str
    order_total_price: int
    payment_method: str


class OrderRowResponseSchema(OrderRowRequestchmea):
    brand: str
    product_name: str
    product_id: str
    price: int
    shipping_fee: int
    intl: bool
