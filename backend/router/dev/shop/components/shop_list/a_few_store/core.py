from ..scrap_module import *


# async def a_few_store_product_list(
#     page: Page, brand_name: str, brand_url: str, **_kwargs
# ):
#     return await get_a_few_store_product_list(page, brand_name, brand_url)


async def get_a_few_store_list(
    page: Page, brand_name: str, search_url: str
) -> List[ShopProductCardSchema]:
    """
    a_few_store에 대한 리스트 Scraper

        Args:
            page (Page): Playwright Page
            url (str): 제품 리스트 URL

        Returns:
            List[Any]: [urls]
    """

    ###
    shop_name = "a_few_store"

    def get_item_info(card) -> Dict[str, Any]:
        price = card.find(class_="price").text
        id = card["id"].replace("findify_", "")
        return {
            "shop_product_name": card.img["data-src"].split("/")[-1],
            "shop_product_img_url": card.img["src"],
            "product_url": card["href"],
            "shop_name": shop_name,
            "brand_name": brand_name,
            "product_id": id,
            "kor_price": None,
            "us_price": None,
            "original_price_currency": None,
            "original_price": price,
            "update_at": None,
        }

    async def get_next_page(page, page_num, xpath):
        button = await page.query_selector(xpath)

        if not button:
            return False

        await button.click()
        return True

    return await ScrapModule.scrap_list_logic(
        page=page,
        shop_name=shop_name,
        brand_name=brand_name,
        search_url=search_url,
        cookie_xpath='//a[contains(@class, "asdasd")]',
        product_card_xpath='//div[contains(@class,"findify-components-search--lazy-results")]',
        card_attr={"attrs": {"class": "product-card"}},
        next_page_xpath="//button[contains(@class,'findify-components--button btn btn-outline-dark')]",
        not_found_xpath='//div[contains(@class,"findify-components-search--lazy-results")]',
        get_item_info=get_item_info,
        get_next_page=get_next_page,
        reverse_not_found_result=True,
        scroll_on=True,
        wait_time_for_verification=20,
    )
