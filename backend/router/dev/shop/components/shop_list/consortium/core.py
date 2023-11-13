from ..scrap_module import *


async def consortium_product_list(
    page: Page, brand_name: str, brand_url: str, **_kwargs
):
    return await get_consortium_list(page, brand_name, brand_url)


async def get_consortium_list(
    page: Page, brand_name: str, search_url: str
) -> List[ShopProductCardSchema]:
    """
    consortium에 대한 리스트 Scraper

        Args:
            page (Page): Playwright Page
            url (str): 제품 리스트 URL

        Returns:
            List[Any]: [urls]
    """

    ###
    shop_name = "consortium"

    def get_item_info(card) -> Dict[str, Any]:
        price = card.find(attrs={"class": "special-price"})
        if price:
            price = price.text
        else:
            price = card.find(attrs={"class": "regular-price"}).text
        price = price.replace("\n", "").replace(" ", "").rstrip("")

        shop_product_name = (
            card.a["href"].split("https://www.consortium.co.uk/")[-1].split(".html")[0]
        )

        # product_id 추출
        shop_product_color = card.find("h4", attrs={"class": "product-colour"})
        if shop_product_color:
            shop_product_color_last = (
                shop_product_color.text.replace("(", "")
                .replace(")", "")
                .split("/")[-1]
                .split(" ")[-1]
                .split("-")[-1]
                .lower()
            )
        else:
            shop_product_color_last = None

        def rindex(lst, value):
            lst.reverse()
            i = lst.index(value)
            lst.reverse()
            return len(lst) - i - 1

        product_id = "-"

        if shop_product_color_last in shop_product_name:
            product_id = ""
            idx = rindex(shop_product_name.split("-"), shop_product_color_last) + 1
            product_id = "-".join(shop_product_name.split("-")[idx:])

        return {
            "shop_product_name": shop_product_name,
            "shop_product_img_url": card.img["src"],
            "product_url": card.a["href"],
            "shop_name": shop_name,
            "brand_name": brand_name,
            "product_id": product_id,
            "search_keyword": brand_name,
            "kor_price": None,
            "us_price": None,
            "original_price_currency": None,
            "original_price": price,
            "update_at": None,
        }

    async def get_next_page(page, page_num, xpath):
        button = await page.query_selector(xpath)

        # Consortium Search Engine이 효율적이지 못해 불필요한 데이터가 수집됨.
        # 이를 방지하기 위한 용도임(brand search에는 불필요)
        num = await page.query_selector("//div[@class='page-title']/p")
        if num:
            num = await num.inner_text()
            num = int(num.split(" ")[0])

            if num > 100:
                return False

        if not button:
            return False

        await button.click()
        return True

    return await ScrapModule.scrap_logic(
        page=page,
        shop_name=shop_name,
        brand_name=brand_name,
        search_url=search_url,
        cookie_xpath="#newsletter-modal > a",
        product_card_xpath='//ul[contains(@class,"products-grid")]',
        card_attr={"attrs": {"class": "item"}},
        next_page_xpath="//a[contains(@class,'next i-next')]",
        not_found_xpath='//ul[contains(@class,"products-grid")]',
        get_item_info=get_item_info,
        get_next_page=get_next_page,
        reverse_not_found_result=True,
        scroll_on=True,
    )
