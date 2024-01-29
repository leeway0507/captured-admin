from pydantic import BaseModel, validator, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel
from typing import List, Optional, Dict

## filter model


class itemArray(BaseModel):
    productType: List[str]
    sizeArray: List[str]


class categorySpec(BaseModel):
    의류: itemArray
    신발: itemArray
    기타: itemArray
    전체: itemArray


class FilterMetaSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    sort_by: List[str]
    category: categorySpec
    brand: List[str]
    intl: List[str]
    price: List[int]


class RequestFilterSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    sort_by: Optional[str] = None
    category: Optional[str] = None
    category_spec: Optional[str] = None
    brand: Optional[str] = None
    intl: Optional[str] = None
    price: Optional[str] = None
    size_array: Optional[str] = None


class ProductResponseSchema(BaseModel):
    data: List[Dict]
    currentPage: int
    lastPage: int


class ProductInfoForTableDataSchema(BaseModel):
    """ProductInfoForTableData Schema"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    sku: int
    product_id: str
    price: int
    shipping_fee: int


class productInfoDraftSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
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


# class ProductInfoForAdminSchema(productInfoDraftSchema):
#     """ProductInfoTable Schema"""

#     model_config = ConfigDict(
#         alias_generator=to_camel,
#         populate_by_name=True,
#     )
#     sku: int
#     deploy: Optional[int] = 0
#     size: Optional[str] = None