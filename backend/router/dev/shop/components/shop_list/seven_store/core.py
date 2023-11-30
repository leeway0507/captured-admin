from ..scrap_module import *
from playwright.async_api import expect

# async def seven_store_product_list(
#     page: Page, brand_name: str, brand_url: str, **_kwargs
# ):
#     return await _scrap_seven_store(page, brand_name, brand_url)


async def get_seven_store_list(
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

    return await ScrapModule.scrap_list_logic(
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


async def get_seven_store_page(
    page: Page, shop_name: str, search_url: str
) -> Dict[str, Any]:
    """
    consortium에 대한 Scraper

        Args:
            page (Page): Playwright Page
            url (str): 제품 URL

        Returns:
            Dict[str, Any]: [sizes, product_id]
    """

    async def get_size_info(page: Page) -> List[Dict[str, Any]]:
        await expect(page.get_by_text("Sizes")).to_be_visible(timeout=10000)

        size_query = await page.query_selector_all(
            '//div[contains(@class, "size-wrapper")]',
        )

        size_list = [await s.inner_text() for s in size_query]

        if not size_list:
            return [{"shop_product_size": "-", "kor_product_size": "-"}]

        l = []
        for s in size_list:
            kor_size = s
            try:
                if float(s) < 15:
                    kor_size = "UK " + s
            except:
                pass
            l.append({"shop_product_size": s, "kor_product_size": kor_size})

        return l

    async def get_product_id(page) -> str:
        product_id_text = await page.query_selector(
            '//meta[contains(@name, "description")]',
        )

        try:
            product_id_text = await product_id_text.get_attribute("content")
            product_id = product_id_text.split(":")[1].replace(" ", "")
        except:
            product_id = "-"

        return product_id.upper()

    return await ScrapModule.scrap_page_logic(
        page=page,
        search_url=search_url,
        shop_name=shop_name,
        get_size_info=get_size_info,
        get_product_id=get_product_id,
        cookie_xpath=[],
    )
