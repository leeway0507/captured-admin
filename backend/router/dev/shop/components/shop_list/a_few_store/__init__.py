# import json
# from typing import List, Dict, Any
# from playwright.async_api import Page

# from ..scrap_module import *


# # async def a_few_store_product_list(
# #     page: Page, brand_name: str, brand_url: str, **_kwargs
# # ):
# #     return await get_a_few_store_product_list(page, brand_name, brand_url)


# async def get_a_few_store_list(
#     page: Page, brand_name: str, search_url: str
# ) -> List[ShopProductCardSchema]:
#     """
#     a_few_store에 대한 리스트 Scraper

#         Args:
#             page (Page): Playwright Page
#             url (str): 제품 리스트 URL

#         Returns:
#             List[Any]: [urls]
#     """

#     ###
#     shop_name = "a_few_store"

#     def get_item_info(card) -> Dict[str, Any]:
#         price = card.find(class_="price").text
#         id = card["id"].replace("findify_", "")
#         return {
#             "shop_product_name": card.img["data-src"].split("/")[-1],
#             "shop_product_img_url": card.img["src"],
#             "product_url": card["href"],
#             "shop_name": shop_name,
#             "brand_name": brand_name,
#             "product_id": id,
#             "kor_price": None,
#             "us_price": None,
#             "original_price_currency": None,
#             "original_price": price,
#             "update_at": None,
#         }

#     async def get_next_page(page, page_num, xpath):
#         button = await page.query_selector(xpath)

#         if not button:
#             return False

#         await button.click()
#         return True

#     return await ScrapModule.scrap_list_logic(
#         page=page,
#         shop_name=shop_name,
#         brand_name=brand_name,
#         search_url=search_url,
#         cookie_xpath='//a[contains(@class, "asdasd")]',
#         product_card_xpath='//div[contains(@class,"findify-components-search--lazy-results")]',
#         card_attr={"attrs": {"class": "product-card"}},
#         next_page_xpath="//button[contains(@class,'findify-components--button btn btn-outline-dark')]",
#         not_found_xpath='//div[contains(@class,"findify-components-search--lazy-results")]',
#         get_item_info=get_item_info,
#         get_next_page=get_next_page,
#         reverse_not_found_result=True,
#         scroll_on=True,
#         wait_time_for_verification=20,
#     )


# class PwAfewStorePage:
#     def __init__(self):
#         self.brand_list = json.loads("./brand_list.json")["data"]

#     def __name__(self) -> str:
#         return "a_few_store"

#     def get_url(self, brand_name) -> str:
#         return self.brand_list.get(brand_name)

#     def get_cookie_button_xpath(self) -> List[str]:
#         return ['//*[@id="CybotCookiebotDialogBodyButtonAccept"]']

#     async def get_size_info(self, page: Page) -> List[Dict[str, Any]]:
#         size_query = await page.query_selector_all("div.input-box>select > option")

#         size_list = [await s.inner_text() for s in size_query]
#         size_list = [size for size in size_list if "Out of Stock" not in size][1:]
#         if not size_list:
#             return [{"shop_product_size": "-", "kor_product_size": "-"}]

#         return [
#             {"shop_product_size": s, "kor_product_size": s.split("-")[0].strip()}
#             for s in size_list
#         ]

#     async def get_product_id(self, page: Page) -> str:
#         product_id_text = await page.query_selector('//*[@id="detailsPanel"]/div')
#         product_id_text = await product_id_text.inner_text()  # type: ignore
#         text = product_id_text.lower()
#         if "product code" in text:
#             product_id = text.split("product code")[1].strip()
#         else:
#             product_id = "-"

#         return product_id.upper()
