from typing import List, Any, Dict, Tuple
from datetime import datetime, date, timedelta

import pandas as pd

from bs4 import BeautifulSoup, Tag

from components.dev.utils.browser_controller import PageController
from components.dev.sub_scraper import SubScraper


class PwKreamPageSubScraper(SubScraper):
    def __name__(self) -> str:
        return "kream"

    # concrete_method
    def late_binding(self, page_controller: PageController):
        self.page_controller = page_controller
        self.page = page_controller.get_page()

    # concrete_method
    async def execute(self):
        await self.go_to_card_page()

        page_detail_status, page_detail_data = await self.scrap_product_detail()
        await self.page_controller.sleep_until(2000)

        buy_and_sell_status, buy_and_sell_data = await self.scrap_buy_and_sell()
        await self.page_controller.sleep_until(2000)

        trading_volume_status, trading_volume_data = await self.scrap_trading_volume()

        return {
            "status": {
                "page_detail": page_detail_status,
                "buy_and_sell": buy_and_sell_status,
                "trading_volume": trading_volume_status,
            },
            "data": {
                "page_detail": page_detail_data,
                "buy_and_sell": buy_and_sell_data,
                "trading_volume": trading_volume_data,
            },
        }

    def get_url(self) -> str:
        return f"https://kream.co.kr/products/{self.job}"

    async def go_to_card_page(self):
        url = self.get_url()
        await self.page_controller.go_to(url)

    # ==========================
    # product_detail ===========
    # ==========================

    async def scrap_product_detail(self) -> Tuple[str, Dict]:
        product_details = await self._scrap_product_details()
        kream_product_name = await self._scrap_product_title()
        review = await self._scrap_review()
        kream_product_img_url = await self._scrap_product_img_url()
        brand = await self._scrap_brand()
        wish = await self._scrap_wish()

        return (
            "success",
            {
                "kream_id": self.job,
                "kream_product_img_url": kream_product_img_url,
                "kream_product_name": kream_product_name,
                "brand_name": brand,
                "retail_price": product_details[0][1],
                "product_id": product_details[1][1],
                "product_release_date": product_details[2][1],
                "color": product_details[3][1],
                "wish": convert_str_to_int(wish),
                "review": review,
                "updated_at": datetime.now().replace(microsecond=0),
            },
        )

    async def _scrap_product_details(self):
        soup_list = await self.get_soup_all(".detail-box")

        return [
            soup.get_text(strip=True, separator="|").split("|") for soup in soup_list
        ]

    async def _scrap_product_title(self) -> str:
        title = await self.page.locator("p.title").first.text_content()
        return title if title else "No Title"

    async def _scrap_review(self):
        review = await self.page.locator(
            ".product_detail_item_title.reviews"
        ).text_content()
        return self._preprocess_review(review) if review else 0

    def _preprocess_review(self, raw_review: str):
        review = raw_review.strip().split(" ")
        if len(review) == 1:
            review = 0
        else:
            review = review[-1].strip()
        return int(review)

    async def _scrap_product_img_url(self):
        img_url = await self.page.locator(".picture.product_img").first.inner_html()
        soup = BeautifulSoup(img_url, "html.parser")
        return soup.find("img")["src"]  # type:ignore

    async def _scrap_brand(self):
        brand = await self.page.locator(
            "div.product-branding-feed-container > div > div > div > span "
        ).text_content()

        return brand if brand else "No brand"

    async def _scrap_wish(self):
        wish = await self.page.locator(".wish_count_num").first.text_content()
        return wish if wish else "No wish"

    # ==========================
    # buy_and_sell =============
    # ==========================

    async def scrap_buy_and_sell(self) -> Tuple:
        """sell과 buy 정보를 가져오는 함수"""

        sell_list = await self._scrap_sell()
        await self.page.go_back()

        await self.page.wait_for_timeout(1)

        buy_list = await self._scrap_buy()
        await self.page.go_back()

        return (
            "success",
            {"kream_id": self.job, "sell": sell_list, "buy": buy_list},
        )

    async def _scrap_sell(self):
        sell = await self.page.query_selector(
            "//div[contains(@class, 'btn_wrap')]/div/button[1]"
        )
        assert sell, "판매 버튼이 잡히지 않음"
        await sell.click()

        return await self._scrap_buy_and_sell_page(f"sell : {self.job}")

    async def _scrap_buy(self):
        buy = await self.page.query_selector(
            "//div[contains(@class, 'btn_wrap')]/div/button[2]"
        )
        assert buy, "구매 버튼이 잡히지 않음"
        await buy.click()
        return await self._scrap_buy_and_sell_page(f"buy : {self.job}")

    async def _scrap_buy_and_sell_page(self, info: str):
        await self.page.wait_for_selector(
            '//li[contains(@class, "select_item")]', timeout=5000
        )

        select_list = await self.page.query_selector_all(
            '//li[contains(@class, "select_item")]'
        )
        if not select_list:
            raise Exception(f"ask 또는 bid의 select_list가 잡히지 않음 : {info}")

        select = {}
        for i in select_list:
            s = await i.query_selector('span[class="size"]')
            assert s, "size가 잡히지 않음"
            size = await s.inner_text()
            # TODO: buy_and_sell 수집 시 문자열 중간의 공백이 제거되는 문제 발생 replace(" ","")를
            # strip()으로 변경, 문제 발생 시 다시 replace(" ","")로 변경
            size = size.strip()

            p = await i.query_selector('span[class="price"]')
            assert p, "price가 잡히지 않음"
            price = await p.inner_text()
            price = price.replace(",", "")

            if price == "판매입찰" or price == "구매입찰":
                price = "0"
            select.update({size: price})

        return select

    # ==========================
    # product_volume ===========
    # ==========================

    async def scrap_trading_volume(
        self, limit_days: int = 10
    ) -> Tuple[str, List[List[str]]]:
        self._set_target_date(limit_days=limit_days)

        if self._scrap_date_is_today():
            return "success", []

        return await self._scrap_trading_volume()

    def _set_target_date(self, limit_days: int = 10) -> date:
        """
        trading volume에서 마지막 업데이트 된 날짜 추출

        Args:
            self.job (str): self.job
            limit_days (int, optional): 최소 업데이트 날짜. Defaults to 10.

        Returns:
            date: 업데이트 날짜(10일 초과 시 오늘로부터 10일 전 날짜 반환)
        """

        today = date.today()
        max_scrap_days = timedelta(days=limit_days)

        # TODO:DB 업데이트 시 사용하기
        last_update = None
        # query = f"""
        #     SELECT trading_date
        #     FROM `kream_trading_volume`
        #     WHERE self.job = '{self.job}'
        #     LIMIT 1
        #     """
        # last_update = execute_query(query)

        if last_update:
            last_update_day = datetime.strptime(last_update[0][0], "%y/%m/%d").date()

            if today > last_update_day + max_scrap_days:
                # 당일 기준 최대 10일 전까지 업데이트
                self.target_date = today - max_scrap_days
                return self.target_date
            else:
                self.target_date = last_update_day
                return self.target_date

        self.target_date = today - max_scrap_days
        return self.target_date

    def _scrap_date_is_today(self) -> bool:
        if date.today() == self.target_date:
            return True
        return False

    async def _scrap_trading_volume(self) -> Tuple[str, List]:
        await self._click_trading_volume_button_element()

        if not await self._is_trading_volume_loaded():
            return self._failed_status()

        await self._scroll_until()
        return await self._extract_trading_volume()

    async def _click_trading_volume_button_element(self):
        volume_btn = "a[class='btn outlinegrey full medium']"
        await self.page.wait_for_selector(volume_btn, timeout=5000)
        await self.page.locator(volume_btn).click()

    async def _is_trading_volume_loaded(self):
        price_btn = "div[class='price_body']"
        try:
            await self.page.wait_for_selector(price_btn, timeout=5000)
            return True
        except Exception as e:
            print(f"{self.job} : 체결내역 더보기가 없는 제품으로 추정")
            return False

    def _failed_status(self):
        return "failed:can't scrap trading_volume", []

    async def _scroll_until(self):
        # scroll until target_date
        scroll_count = 0
        transaction_count_prev = 0
        transaction_count_curr = 1
        last_date = None
        while transaction_count_prev < transaction_count_curr and scroll_count <= 10:
            scroll_count += 1
            transaction_count_prev = transaction_count_curr
            await self.page.wait_for_timeout(1000)

            transaction_count_curr = await self._get_trading_volume_count()
            last_date = await self._get_last_date_trading_volume()

            if self.target_date < last_date:
                await self._scroll_trading_volume_page()
            else:
                break
        return {
            "scroll_count": scroll_count,
            "last_date": last_date,
        }

    async def _get_trading_volume_count(self):
        return await self.page.evaluate(
            "Array.from(document.querySelectorAll('.list_txt.is_active')).length"
        )

    async def _get_last_date_trading_volume(self) -> date:
        last_date = await self.page.evaluate(
            f"Array.from(document.querySelectorAll('.list_txt.is_active')).slice(-1)[0].innerText"
        )
        last_date = last_date.replace("빠른배송", "").strip()
        return datetime.strptime(last_date, "%y/%m/%d").date()

    async def _scroll_trading_volume_page(self):
        scroll_eval = "(async () => { document.querySelector('.price_body').scrollBy(0, 3000); })()"
        await self.page.evaluate(scroll_eval)

    async def _extract_trading_volume(self):
        scrap_result, filtered_result = await self._extract_data_from_html()

        if len(scrap_result) > 0 and len(filtered_result) > 0:
            return "success", filtered_result

        if len(scrap_result) > 0 and len(filtered_result) == 0:
            return f"success:no_trading_volume", []

        return self._failed_status()

    async def _extract_data_from_html(self):
        volumes = await self.get_soup_all(".body_list")
        data = self._extract_volume_data_from(volumes)

        scrap_data = self._scrap_trading_volume_data(data)
        filtered_data = self._filter_trading_volume_data(scrap_data)

        return scrap_data, filtered_data

    def _scrap_trading_volume_data(self, data: List):
        df = pd.DataFrame(
            data,
            columns=["kream_product_size", "price", "lightening", "trading_at"],
        )
        df["kream_id"] = self.job
        return df

    def _filter_trading_volume_data(self, df: pd.DataFrame) -> List[Dict]:
        target_date_str = self.target_date.strftime("%y/%m/%d")
        return df[df["trading_at"] >= target_date_str].to_dict("records")

    def _extract_volume_data_from(self, body_list: List) -> List[List]:
        """
        크롤링 결과 리스트에서 거래량 추출

        Args:
            body_list (List): 크롤링 결과 리스트

        Returns:
            List: 크롤링 결과 리스트로 반환
        """

        def preprocess_items(tags: Tag) -> List:
            x = []
            for tag in tags.find_all(class_="list_txt"):
                x.append(tag.text.strip())

            if "빠른배송" in x[2]:
                return [x[0], x[1], True, x[2].replace("빠른배송", "").strip()]
            else:
                return [x[0], x[1], False, x[2].strip()]

        return list(map(lambda tags: preprocess_items(tags), body_list))

    async def get_soup_all(self, value: str) -> List[Tag]:
        await self.page.wait_for_timeout(2000)
        e_list = await self.page.query_selector_all(value)
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
