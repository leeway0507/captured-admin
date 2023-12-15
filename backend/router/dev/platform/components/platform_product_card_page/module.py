from ....utils.browser_controller import PageController as P
from bs4 import Tag
from typing import List, Dict, Any, Tuple
from datetime import datetime
from model.kream_scraping import KreamProductDetailSchema
from playwright.async_api import Page
from env import dev_env

from bs4 import BeautifulSoup, Tag
from datetime import date, timedelta
import pandas as pd


class PwKreamPage:
    def __init__(self):
        self.path = dev_env.PLATFORM_PRODUCT_PAGE_DIR

    def __name__(self) -> str:
        return "kream"

    def get_url(self, platform_sku: str) -> str:
        return f"https://kream.co.kr/products/{platform_sku}"

    async def get_product_detail(self, page: Page, platform_sku: int) -> Dict[str, Any]:
        soup_list = await self.get_soup_all(page, ".detail-box")

        d_list = [
            soup.get_text(strip=True, separator="|").split("|") for soup in soup_list
        ]

        title = await page.query_selector("p.title")
        assert title, "get_product_detail : p.title is None."
        kream_product_name = await title.inner_text()

        review = await page.query_selector(".product_detail_item_title.reviews")
        assert review, "get_product_detail : review is None"
        review = await review.inner_text()
        review = review.split(" ")
        if len(review) == 1:
            review = "0"
        else:
            review = review[-1].strip()

        img_url = await page.query_selector(".picture.product_img")
        assert img_url, "get_product_detail : img_url is None"
        img_url = BeautifulSoup(await img_url.inner_html(), "html.parser")
        kream_product_img_url = img_url.find("img")["src"]  # type:ignore

        brand = await page.query_selector(
            "div.product-branding-feed-container > div > div > div > span "
        )
        assert brand, "get_product_detail : brand is None"
        brand = await brand.inner_text()

        wish = await page.query_selector(".wish_count_num")
        assert wish, "get_product_detail : wish is None"
        wish = await wish.inner_text()

        return {
            "kream_id": platform_sku,
            "kream_product_img_url": kream_product_img_url,
            "kream_product_name": kream_product_name,
            "brand_name": brand,
            "retail_price": d_list[0][1],
            "product_id": d_list[1][1],
            "product_release_date": d_list[2][1],
            "color": d_list[3][1],
            "wish": convert_str_to_int(wish),
            "review": convert_str_to_int(review),
            "updated_at": datetime.now().replace(microsecond=0),
        }

    async def get_buy_and_sell(self, page: Page, platform_sku: int):
        """sell과 buy 정보를 가져오는 함수"""
        sell = await page.query_selector(
            "//div[contains(@class, 'btn_wrap')]/div/button[1]"
        )
        assert sell, "판매 버튼이 잡히지 않음"
        await sell.click()

        sell_list = await self._buy_and_sell(page, f"sell : {platform_sku}")

        await page.go_back()
        await page.wait_for_selector(
            "//div[contains(@class, 'btn_wrap')]/div/button[2]"
        )
        await page.wait_for_timeout(1)

        buy = await page.query_selector(
            "//div[contains(@class, 'btn_wrap')]/div/button[2]"
        )
        assert buy, "구매 버튼이 잡히지 않음"
        await buy.click()
        buy_list = await self._buy_and_sell(page, f"buy : {platform_sku}")
        await page.go_back()

        return {"kream_id": platform_sku, "sell": sell_list, "buy": buy_list}

    async def _buy_and_sell(self, page, info: str):
        await page.wait_for_selector(
            '//li[contains(@class, "select_item")]', timeout=5000
        )

        select_list = await page.query_selector_all(
            '//li[contains(@class, "select_item")]'
        )
        if not select_list:
            raise Exception(f"ask 또는 bid의 select_list가 잡히지 않음 : {info}")

        select = {}
        for i in select_list:
            s = await i.query_selector('span[class="size"]')
            assert s, "size가 잡히지 않음"
            size = await s.inner_text()
            size = size.replace(" ", "")

            p = await i.query_selector('span[class="price"]')
            assert p, "price가 잡히지 않음"
            price = await p.inner_text()
            price = price.replace(",", "")

            if price == "판매입찰" or price == "구매입찰":
                price = 0
            select.update({size: price})

        return select

    # ==========================
    # product_volume ===========
    # ==========================

    async def get_product_volume(
        self, page: Page, platform_sku: int, max_scrap_days: int = 10, **_kwargs
    ) -> Tuple[str, List[List[str]]]:
        start_date = self._get_start_date(platform_sku, limit_days=max_scrap_days)
        if date.today() == start_date:
            print("당일 업데이트가 되었음")
            return "success", []

        return await self._scrap_trading_volume_from(page, start_date, platform_sku)

    def _get_start_date(self, platform_sku: int, limit_days: int = 10) -> date:
        """
        trading volume에서 마지막 업데이트 된 날짜 추출

        Args:
            platform_sku (str): platform_sku
            limit_days (int, optional): 최소 업데이트 날짜. Defaults to 10.

        Returns:
            date: 업데이트 날짜(10일 초과 시 오늘로부터 10일 전 날짜 반환)
        """

        today = date.today()

        max_scrap_days = timedelta(days=limit_days)

        last_update = None

        # TODO:DB 업데이트 시 사용하기
        # query = f"""
        #     SELECT trading_date
        #     FROM `kream_trading_volume`
        #     WHERE platform_sku = '{platform_sku}'
        #     LIMIT 1
        #     """
        # last_update = execute_query(query)

        if last_update:
            last_update_day = datetime.strptime(last_update[0][0], "%y/%m/%d").date()

            if today > last_update_day + max_scrap_days:
                # 당일 기준 최대 10일 전까지 업데이트
                return today - max_scrap_days
            else:
                return last_update_day

        return today - max_scrap_days

    async def _scrap_trading_volume_from(
        self, page: Page, target_date: date, platform_sku: int, **_kwargs
    ) -> Tuple[str, List]:
        volume_btn = "a[class='btn outlinegrey full medium']"
        await page.wait_for_selector(volume_btn, timeout=5000)

        trading_volume_button = await page.query_selector(volume_btn)

        assert trading_volume_button, "trading_volume_button not found"
        await trading_volume_button.click()

        price_btn = "div[class='price_body']"
        try:
            await page.wait_for_selector(price_btn, timeout=5000)
        except Exception as e:
            print(f"{platform_sku} : 체결내역 더보기가 없는 제품으로 추정")
            return "failed", []

        modal = await page.query_selector(price_btn)
        assert modal, "modal not found"

        # scroll until target_date
        i = 0
        start = 0
        end = 1
        while start < end and i <= 10:
            i += 1
            start = end
            await page.wait_for_timeout(1000)
            end = await page.evaluate(
                "Array.from(document.querySelectorAll('.list_txt.is_active')).length"
            )
            date_str: str = await page.evaluate(
                f"Array.from(document.querySelectorAll('.list_txt.is_active')).slice(-1)[0].innerText"
            )
            date_str = date_str.replace("빠른배송", "").strip()
            last_date = datetime.strptime(date_str, "%y/%m/%d").date()

            # print(f"platform_sku:{platform_sku},last_date : {last_date}, target_date : {target_date}, end : {end}")

            if target_date < last_date:
                scroll_eval = "(async () => { document.querySelector('.price_body').scrollBy(0, 3000); })()"
                await page.evaluate(scroll_eval)
            else:
                break

        volumes = await self.get_soup_all(page, ".body_list")
        body_list = self._extract_volume_data_from(volumes)

        df = pd.DataFrame(
            body_list,
            columns=["kream_product_size", "price", "lightening", "trading_at"],
        )
        df["kream_id"] = platform_sku

        target_date_str = target_date.strftime("%y/%m/%d")
        result = df[df["trading_at"] >= target_date_str].to_dict("records")

        if len(df) > 0 and len(result) > 0:
            return "success", result

        if len(df) > 0 and len(result) == 0:
            return "no_trading_volume", []

        return "failed", []

    def _extract_volume_data_from(self, body_list: List) -> List[List]:
        """
        크롤링 결과 리스트에서 거래량 추출

        Args:
            body_list (List): 크롤링 결과 리스트

        Returns:
            List: 크롤링 결과 리스트로 반환
        """

        def preprocess_items(tags) -> List:
            x = []
            for tag in tags.find_all(class_="list_txt"):
                x.append(tag.text.strip())

            if "빠" in x[2]:
                return [x[0], x[1], True, x[2].replace("빠른배송", "").strip()]
            else:
                return [x[0], x[1], False, x[2].strip()]

        return [preprocess_items(tags) for tags in body_list]

    async def get_soup_all(self, page: Page, value: str) -> List[Tag]:
        await page.wait_for_timeout(2000)
        e_list = await page.query_selector_all(value)
        if len(e_list) == 0:
            return []
        return [BeautifulSoup(await e.inner_html(), "html.parser") for e in e_list]


def convert_str_to_int(value: str) -> int:
    """문자열을 숫자로 변환"""

    if "거래" in value:
        value = value.replace("거래", "").replace(" ", "")

    if "만" in value:
        value = value.replace("만", "")
        return int(float(value) * 10000)

    value = value.replace(",", "")
    return int(value)
