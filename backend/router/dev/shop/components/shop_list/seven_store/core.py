from ..scrap_module import *


async def seven_store_product_list(
    page: Page, brand_name: str, brand_url: str, **_kwargs
):
    return await _scrap_seven_store(page, brand_name, brand_url)


async def _scrap_seven_store(
    page: Page, brand_name: str, search_url: str
) -> List[ShopProductCardSchema]:
    shop_name = "seven_store"

    def get_item_info(card) -> Dict[str, Any]:
        product_name = card.find("a", class_="f-hover-decor").text
        price = card.find(attrs={"data-listing": "price"}).text.split(" RRP")[0]
        return {
            "shop_product_name": product_name + " - " + card["data-nq-product"],
            "shop_product_img_url": card.img["src"],
            "product_url": card.img["data-url"],
            "shop_name": shop_name,
            "brand_name": brand_name,
            "product_id": None,
            "kor_price": None,
            "us_price": None,
            "original_price_currency": None,
            "original_price": price,
            "update_at": None,
        }

    async def get_next_page(page, page_num, xpath):
        return False

    return await ScrapModule.scrap_logic(
        page=page,
        shop_name=shop_name,
        brand_name=brand_name,
        search_url=search_url,
        cookie_xpath='//button[@class="btn btn-level1 accept-all-cookies"]',
        product_card_xpath='//div[contains(@id,"listing-list")]',
        card_attr={"attrs": {"class": "nodecor"}},
        next_page_xpath="//a[contains(@title,'Next Page')]",
        not_found_xpath='//div[contains(@id,"listing-list")]',
        reverse_not_found_result=True,
        get_item_info=get_item_info,
        get_next_page=get_next_page,
        scroll_on=True,
    )
