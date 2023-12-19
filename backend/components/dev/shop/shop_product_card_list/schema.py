from typing import List, Optional
from pydantic import BaseModel


class ListConfig(BaseModel):
    scroll_on: bool = False
    reverse_not_found_result: bool = False
    page_reload_after_cookies: bool = False
    cookie_button_xpath: List[str] = []
    not_found_xpath: str
    wait_until_load: int = 2000
    max_scroll: int = 10


class ListScrapData(BaseModel):
    shop_name: str
    brand_name: str = ""
    shop_product_name: str
    shop_product_img_url: str
    product_url: str
    product_id: Optional[str] = None
    price: str
