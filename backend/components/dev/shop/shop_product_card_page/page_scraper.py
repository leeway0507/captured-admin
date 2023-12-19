from .page_module_factory import ShopPageModule
from ...utils.browser_controller import PageController as P


class ShopPageScrapMachine:
    def __init__(self, page_controller: P, shop_page_module: ShopPageModule):
        self.page_controller = page_controller
        self.shop_module = shop_page_module
        self.shop_name = shop_page_module.__name__()

    async def execute(self, url: str):
        # go_to page
        await self.page_controller.go_to(url)

        # deal with cookies
        cookie_button_xpath = self.shop_module.get_cookie_button_xpath()
        if cookie_button_xpath:
            await self.page_controller.deal_with_cookies(cookie_button_xpath)

        # scrap size and product_id
        page = await self.page_controller.get_page()
        size_info = await self.shop_module.get_size_info(page)
        product_id = await self.shop_module.get_product_id(page)
        return {"size_info": size_info, "product_id": product_id}
