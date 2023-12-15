from typing import Dict, Callable, List, Any
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from bs4 import BeautifulSoup
import asyncio
import re
import json

page_log = make_logger(path="logs/page_shop.log", name="AsyncShopPageScraper")


# PageScraper
def raise_timeout_error_page(inner_function: Callable):
    """PageScraper에 대한 Timeout Error를 처리하는 데코레이터"""

    async def wrapper(*arg, **kwargs):
        max_retries = 3
        retry_delay = 1
        for retry_count in range(max_retries + 1):
            try:
                result = await inner_function(*arg, **kwargs)
                return ShopPageOutput(**result)

            except (Exception, PlaywrightTimeoutError) as e:
                if retry_count < max_retries:
                    page_log.error(
                        f'"{retry_count}.... [ {inner_function.__name__} ]  {e}'
                    )
                    await asyncio.sleep(retry_delay)
                else:
                    page_log.error(f'"최종 실패" : [ {inner_function.__name__} ]  {e}')
                    return {"sizes": [], "product_id": ""}

    return wrapper


class AsyncShopPageScraper:
    """쇼핑몰 정보를 Async로 가져오는 클래스"""

    def scraper_dict(self) -> Dict[str, Callable]:
        """쇼핑몰 별 스크랩 함수를 담은 딕셔너리"""
        return {
            "thehipstore": self.scrap_thehipstore,
            "oneblockdown": self.scrap_oneblockdown,
            "nakedcph": self.scrap_nakedcph,
            "nittygrittystore": self.scrap_nittygrittystore,
            "18montrose": self.scrap_18montrose,
            "afew-store": self.scrap_afew_store,
            "allikestore": self.scrap_allikestore,
            "crossoverconceptstore": self.scrap_crossoverconceptstore,
            "sevenstore": self.scrap_sevenstore,
            "hanon-shop": self.scrap_hanon_shop,
            "consortium": self.scrap_consortium,
            "end_clothing": self.scrap_end_clothing,
            # -----------------
            # "club21": self.scrap_club21,
            # "cettire": self.scrap_cettire,
            # "footpatrol": self.scrap_footpatrol,
            # "oallery": self.scrap_oallery,
            # "upforward": self.scrap_upforward,
        }

    @raise_timeout_error_page
    async def scrap_thehipstore(self, page: Page, url: str) -> Dict[str, Any]:
        local_page = await self._load_page(page, url)
        sizes = await local_page.query_selector(
            '//div[contains(@id,"productSizeStock")]'
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all("button")
            sizes = [size.text.strip() for size in sizes]
        else:
            print(sizes)
            sizes = []

        product_id_text = await local_page.query_selector('//p[@id="editor-notes"]')
        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            product_id = re.search(r"(?i)style code\s*:\s*(\w+)", product_id_text)
            assert product_id, f"thehipstore - product_id에 대한 regex가 잘못되었을 수 있음."
            product_id = product_id.group(1).split(" ")[0].replace(".", "-")
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_oneblockdown(self, page: Page, url: str) -> Dict[str, Any]:
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//div[contains(@class,"special-select")]'
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all(name="option")
            sizes = [size.text.strip() for size in sizes]
        else:
            sizes = []

        return {"sizes": sizes, "product_id": "Do Not Update"}

    @raise_timeout_error_page
    async def scrap_nakedcph(self, page: Page, url: str) -> Dict[str, Any]:
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//div[contains(@class,"dropdown-menu")]',
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all(class_="dropdown-item")
            sizes = [
                size.text.strip() for size in sizes if "disabled" not in size["class"]
            ]
        else:
            sizes = []

        product_id_text = await local_page.query_selector(
            '//div[contains(@class,"list-group")]',
        )
        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            product_id = product_id_text.split("\n")[-1]

        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_nittygrittystore(self, page: Page, url: str) -> Dict[str, Any]:
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//tbody[contains(@class,"Styles.tiles")]',
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all("td")
            sizes = [size.text for size in sizes]
        else:
            sizes = []

        return {"sizes": sizes, "product_id": "Do Not Update"}

    @raise_timeout_error_page
    async def scrap_18montrose(self, page: Page, url: str) -> Dict[str, Any]:
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//div[contains(@id,"divSize")]',
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all("a")
            sizes = [size.text.strip().split("(")[0] for size in sizes]
        else:
            sizes = []

        return {"sizes": sizes, "product_id": "-"}

    @raise_timeout_error_page
    async def scrap_afew_store(self, page: Page, url: str) -> Dict[str, Any]:
        local_page = await self._load_page(page, url)

        sizes = await page.query_selector('//div[contains(@class,"size-picker")]')

        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all("a")
            sizes = [
                size.text for size in sizes if "disabled" not in size.get("class", [])
            ]
        else:
            sizes = []

        product_id_text = await local_page.query_selector("//*[@id='content-details']")
        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            text_list = product_id_text.split(" ")
            product_id_idx = text_list.index("Style") + 1
            product_id = text_list[product_id_idx]

        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_crossoverconceptstore(self, page: Page, url: str) -> Dict[str, Any]:
        """
        crossoverconceptstore에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str, Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//fieldset[contains(@name,"Size")]',
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all("label")
            if sizes:
                sizes = [
                    size.text
                    for size in sizes
                    if "disabled" not in size.get("class", [])
                ]
            else:
                sizes = []
        else:
            sizes = []

        product_id_text = await local_page.query_selector(
            '//div[@class="product-block"][4]'
        )
        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            product_id = re.search(r"(?i)style code\s*:\s*(\w+)", product_id_text)
            assert (
                product_id
            ), f"crossoverconceptstore - product_id에 대한 regex가 잘못되었을 수 있음."
            product_id = product_id.group(1).split(" ")[0]
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_club21(self, page: Page, url: str) -> Dict[str, Any]:
        """
        club21에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str, Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//fieldset[contains(@name,"Size")]',
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all("label")
            sizes = [
                size.text for size in sizes if "disabled" not in size.get("class", [])
            ]
        else:
            sizes = []

        product_id_text = await local_page.query_selector("//textarea[last()]")
        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            product_id = json.loads(product_id_text)
            product_id = product_id.get("barcode", "-").split("/00/")[0]
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_upforward(self, page: Page, url: str) -> Dict[str, Any]:
        """
        upforward에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str,Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//fieldset[contains(@name,"Size")]',
        )
        if sizes:
            sizes = await sizes.inner_html()
            soup = BeautifulSoup(sizes, "html.parser")
            sizes = soup.find_all("label")
            sizes = [size.text for size in sizes]
        else:
            sizes = []

        return {"sizes": sizes, "product_id": "-"}

    @raise_timeout_error_page
    async def scrap_sevenstore(self, page: Page, url: str) -> Dict[str, Any]:
        """
        sevenstore에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str,Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//div[contains(@class, "sizes-scroll-wrapper")]',
        )
        if sizes:
            sizes = await sizes.inner_text()
            sizes = sizes.replace(" ", "").split("\n")
        else:
            sizes = []

        product_id_text = await local_page.query_selector(
            '//li[contains(@class, "short_description")][last()]',
        )

        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            product_id = product_id_text.split(":")[1].replace(" ", "")
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_cettire(self, page: Page, url: str) -> Dict[str, Any]:
        """
        cettire에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str, Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector(
            '//*[@id="product-detail--size-list"]/div/div[2]/ul'
        )
        if sizes:
            soup = BeautifulSoup(await sizes.inner_html(), "html.parser")
            sizes = soup.find_all("li")
            sizes = [
                size.span.text for size in sizes if size.span and "품절" not in size.text
            ]
        else:
            sizes = []

        product_id_text = await local_page.query_selector(
            '//*[@id="main-page-container"]/main/div[2]/div[1]/div[2]/div[last()]/div[2]',
        )
        if product_id_text:
            product_id_text = await product_id_text.inner_html()
            product_id = (
                product_id_text.split("디자이너 모델 번호")[1]
                .replace(":", "")
                .split("<br>")[0]
                .split("</div>")[0]
                .strip()
            )
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_oallery(self, page: Page, url: str) -> Dict[str, Any]:
        """
        oallery에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str,Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        size_list = await local_page.query_selector_all(
            "//*[@class ='c-product-options_item_inner']/div[not(@class ='is-not-available')]",
        )
        sizes = []
        for size in size_list:
            class_text: str = await size.get_attribute("class")  # type: ignore
            if "is-not-available" in class_text:
                continue
            else:
                s = await size.inner_text()
                sizes.append(s)

        return {"sizes": sizes, "product_id": "-"}

    @raise_timeout_error_page
    async def scrap_end_clothing(self, page: Page, url: str) -> Dict[str, Any]:
        """
        end_clothing에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str, Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        size_list = await local_page.query_selector('//*[@data-test-id="Size__List"]')
        if size_list:
            size_list = await size_list.inner_text()
            sizes = [
                size for size in size_list.split("\n") if "Out of Stock" not in size
            ]
        else:
            sizes = []

        product_id_text = local_page.url
        product_id = product_id_text.split("-")[-1].split(".")[0].upper()

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_consortium(self, page: Page, url: str) -> Dict[str, Any]:
        """
        consortium에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str, Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        size_list = await local_page.query_selector('//*[@data-label-text="Shoe Size"]')
        if size_list:
            size_list = await size_list.inner_text()
            sizes = [
                size for size in size_list.split("\n") if "Out of Stock" not in size
            ][1:]
        else:
            sizes = []

        product_id_text = await local_page.query_selector('//*[@id="detailsPanel"]/div')
        if product_id_text:
            product_id_text = await product_id_text.inner_text()
            product_id = product_id_text.split("*")[-1].split(" ")[-1].rstrip("\n")
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_footpatrol(self, page: Page, url: str) -> Dict[str, Any]:
        """
        footpatrol에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str, Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        sizes = await local_page.query_selector('//*[@id="productSizeStock"]')
        if sizes:
            sizes = await sizes.inner_text()
            sizes = sizes.split(" ")
            sizes = ["UK " + size for size in sizes]
        else:
            sizes = []

        product_id_text = await local_page.query_selector(
            '//*[@id="itemInfo"]/ul/li[1]/ul'
        )
        if product_id_text:
            product_id_text = await product_id_text.inner_html()
            product_id = product_id_text.split("|")[-1].split("\n")[0].split(" ")[1]
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_hanon_shop(self, page: Page, url: str) -> Dict[str, Any]:
        """
        hanon_shop에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str,Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        size_list = await local_page.query_selector_all(
            "//variant-radios/fieldset/input[not(@disabled)]"
        )

        sizes = []
        for size in size_list:
            s = await size.get_attribute("value")
            sizes.append(s)
        sizes = [size.split(" : ")[0] for size in sizes]

        product_id = await local_page.query_selector(
            f"(//*[contains(@class, 'variant-sku')])"
        )
        if product_id:
            product_id = await product_id.inner_html()
            product_id = product_id.split(" ")[2]
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    @raise_timeout_error_page
    async def scrap_allikestore(self, page: Page, url: str) -> Dict[str, Any]:
        """
        allikestore에 대한 Scraper

            Args:
                page (Page): Playwright Page
                url (str): 제품 URL

            Returns:
                Dict[str,Any]: [sizes, product_id]
        """
        local_page = await self._load_page(page, url)

        size_list = await local_page.query_selector(
            f'//*[@class="product-form__input__options"]'
        )
        product_id = await local_page.query_selector('//*[@class="product__title"]/p')

        sizes = []
        if size_list:
            size_list = await size_list.inner_text()
            size_list = size_list.split("\n")
            for i in size_list:
                if i == "Variant sold out or unavailable":
                    sizes.pop()
                    continue
                sizes.append(i)

        if product_id:
            product_id = await product_id.inner_html()
            product_id = product_id.strip()
        else:
            product_id = "-"

        return {"sizes": sizes, "product_id": product_id}

    async def _load_page(self, page: Page, url):
        """페이지 로드"""
        await page.goto(url)
        await page.wait_for_load_state(state="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)
        await asyncio.sleep(1)
        return page
