"""pydantic Schemas"""
import re
from typing import Optional

from pydantic import BaseModel, field_validator
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ResponseMarketPrice(BaseModel):
    """kream/product"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    kream_product_size: str
    buy: int
    sell: int
    count: int
    min: int
    median: int
    max: int
    lightening: int
