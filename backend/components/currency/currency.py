""" currency & Price Calculator """

from typing import Dict, Tuple, Any, Optional
import json
import re

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from components.env import dev_env


class Currency:
    """
    선별 된 아이템에 대한 금액 계산
    """

    def __init__(
        self,
        buy_dir: Optional[str] = None,
        custom_dir: Optional[str] = None,
    ) -> None:
        """
        - 관세 환율, 구매 환율 수집
        - 환율 수집 날짜 조정이 우선 필요하므로 _get_buying_currency 우선 수행
        """
        self.date = datetime.today()
        if buy_dir and custom_dir:
            self.buy_dir = buy_dir
            self.custom_dir = custom_dir
        else:
            path = dev_env.SHOP_CURRENCY_DIR

            self.buy_dir = path + "data/buying_currency.json"
            self.custom_dir = path + "data/custom_currency.json"

        self.buying_curr = self._load_currency(self.buy_dir)
        self.custom_curr = self._load_currency(self.custom_dir)

    def _load_currency(self, dir: str) -> Dict[str, float]:
        """currency 정보 불러오기
        - 환율 수집 날짜 조정이 우선 필요하므로 _get_buying_currency 우선 수행
        """
        i = 0
        while True:
            if i > 4:
                raise RuntimeError("currency API 관련 에러 발생")

            with open(dir, "r") as file:
                json_data = json.load(file)

            if json_data.get("update", "00/01/01") < self.date.strftime("%y/%m/%d"):
                try:
                    self._get_buying_currency_from_API()
                    self._get_custom_currency_from_API()
                except Exception as e:
                    print("환율 불러오기 실패")
                    print(e)

                    print(f"{json_data['update']} 데이터 활용")
                    break

                i += 1
            else:
                break
        return json_data.get("data")

    def get_currency(self) -> Dict:
        """
        수집한 currency 정보 불러오기

        Returns:
            Dict: buying(구매 환율), custom(관세 환율)

        """
        return {"buying": self.buying_curr, "custom": self.custom_curr}

    def _get_buying_currency_from_API(self) -> None:
        """
        - 구매 환율 추출
        - 수출입은행에서 제공하는 API를 활용

        Returns:
            Dict[str,float]: {화폐명 : 환율}

        """
        res = {}
        for i in range(1, 6):
            # 공휴일에는 환율이 존재하지 않으므로 날짜 조정 필요
            params = {
                "authkey": dev_env.SHOP_BUYING_CURRENCY_API_KEY,
                "searchdate": self.date.strftime("%Y%m%d"),
                "data": "AP01",
            }
            res = requests.get(
                "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON",
                params=params,
                timeout=5,
            )
            res = json.loads(res.text)
            if res:
                break

            self.date -= timedelta(days=1)

            if i == 5:
                raise ValueError(
                    f'"{self.date.strftime("%Y%m%d")}" has no currency data.'
                )

        curr_dict = {}
        for d in res:
            if d["cur_unit"] == "JPY(100)":
                curr_dict["JPY"] = round(
                    float(d["deal_bas_r"].replace(",", "")) / 100, 2
                )
            else:
                curr_dict[d["cur_unit"]] = float(d["deal_bas_r"].replace(",", ""))

        if curr_dict in [None, {}]:
            print(f"최신 _구매_ 환율 정보를 업데이트하지 못했습니다.")
            return None

        return self._save_updated_currency(curr_dict, dir=self.buy_dir)

    def _get_custom_currency_from_API(self) -> None:
        """
        - 관세 환율 수집
        - 관세청 API 활용

        Returns:
            Dict[str,float]: {화폐명 : 환율}

        """
        params = {
            "serviceKey": dev_env.SHOP_CUSTOM_CURRENCY_APY_KEY,
            "aplyBgnDt": self.date.strftime("%Y%m%d"),
            "weekFxrtTpcd": "2",
        }
        html = requests.get(
            "http://apis.data.go.kr/1220000/retrieveTrifFxrtInfo/getRetrieveTrifFxrtInfo",
            params=params,
        )

        # 환율 추출
        soup = BeautifulSoup(html.text, "xml")
        curr_dict = {}
        for i in soup.find_all("item"):
            # 화폐 이름
            curr_sgn = i.find("currSgn").text
            # 관세 환율
            fxrt = i.find("fxrt").text
            curr_dict[curr_sgn] = float(fxrt)

        if curr_dict in [None, {}]:
            print(f"최신 _관세_ 환율 정보를 업데이트하지 못했습니다.")
            return None

        return self._save_updated_currency(curr_dict, dir=self.custom_dir)

    def _save_updated_currency(self, updated_currency, dir) -> None:
        """API에서 받은 currency 정보 저장"""

        curr_data = {
            "update": self.date.strftime("%y/%m/%d"),
            "data": updated_currency,
        }
        # 데이터 저장하기
        with open(dir, "w") as file:
            json.dump(curr_data, file)

    def get_price_info(self, price: str) -> Tuple[str, str, float]:
        """
        텍스트에서 환율 정보를 추출

        Args:
            price(str): ex) $100, ₩100,000,000, €100,00

        Returns:
            Tuple[str, str, float]: (화폐 기호, 화폐명, 환율) ex) ["$","USD",100.0]
        """
        curr_dict = {
            "$": "USD",
            "€": "EUR",
            "¥": "JPY",
            "£": "GBP",  # unicode 163
            "￡": "GBP",  # unicode 65505
            "₩": "KRW",
            "원": "KRW",
            "RM": "MYR",
        }
        # 통화 찾기
        curr_char = re.sub(f"[^{''.join(curr_dict.keys())}]", "", price)

        # str_float => float
        l = re.sub("[^0-9,]", "", price.replace(".", ",")).split(",")

        # len(l) == 1 ex) $80 or $8
        if len(l) > 1 and len(l[-1]) < 3:
            f = "".join(l[:-1])
            curr_float = f + "." + l[-1]
        else:
            curr_float = "".join(l)
        return curr_char, curr_dict[curr_char], float(curr_float)

    def _calc_custom_fee(
        self, price: str, intl_shipment: str, country: str, custom_rate: float = 0.1
    ) -> Tuple[float, str, str, float]:
        """
        price + intl_shipment USD로 계산 후 관세 부과 여부 검토

        Args:
            price(str): 물품가격  ex) $100, ₩100,000,000, €100,00
            intl_shipment(str): 배송비 ex) $100, ₩100,000,000, €100,00
            country(str): 배송 국가 ex) US, EU..

        Returns:
            Tuple[float, str, str, float]: (관세(KRW), 화폐 기호, 화폐명, 관세계산가격(USD)) ex) ("20000","$","USD",100.0)

        """
        fee = 0
        for p in [price, intl_shipment]:
            *_, usd = self.change_currency_to_custom_usd(p)
            fee += usd

        if country == "US" and fee > 200:
            custom_fee = round(fee * self.custom_curr["USD"] * custom_rate, 2)
            return (custom_fee, "$", "USD", fee)

        if country != "US" and fee > 150:
            custom_fee = round(fee * self.custom_curr["USD"] * custom_rate, 2)
            return (custom_fee, "$", "USD", fee)

        return (0.0, "$", "USD", fee)

    def change_currency_to_custom_usd(self, price: str) -> Tuple[str, str, float]:
        """
        관세 계산을 위한 USD로 통화 변경

        Args:
            price(str) : USD로 변경할 통화

        Returns:
            Tuple[float, str, float]: (화폐 기호, 화폐명, 관세계산가격(USD)) ex) ("$","USD",100.0)
        """

        curr_char, curr_name, curr_float = self.get_price_info(price)
        # USD 인 경우
        if curr_char == "$":
            return ("$", "USD", curr_float)

        # KRW 인 경우(KRW => USD)
        if curr_char == "₩":
            usd = round(curr_float / self.custom_curr["USD"], 2)
            return ("$", "USD", usd)

        # 그 외(외국 통화 => KRW => USD)
        won = self.custom_curr[curr_name] * curr_float
        usd = round(won / self.custom_curr["USD"], 2)
        return ("$", "USD", usd)

    def change_currency_to_buying_won(self, currency: str) -> Tuple[str, str, float]:
        """
        한국 통화로 변경

        Args:
            currency(str) : KRW로 변경할 통화

        Returns:
            Tuple[float, str, float]: (화폐 기호, 화폐명, 관세계산가격(USD)) ex) ("$","USD",100.0)
        """
        curr_char, curr_name, curr_float = self.get_price_info(currency)
        if curr_char == "₩":
            return ("₩", "KRW", curr_float)
        else:
            # 외국통화 => KRW
            curr_float = self.buying_curr[curr_name] * curr_float
            return ("₩", "KRW", round(curr_float, 2))

    def _get_expense_info(
        self,
        price: str,
        country: str = "US",
        intl_shipment: str = "₩25,000",
        dome_shipment: str = "₩3,000",
        platform_fee: str = "₩7,000",
        card_fee_rate: float = 1.01,
        **_kwargs,
    ) -> Dict[str, Any]:
        """
        총 지출 계산

        Args:
            price(str): 물품가격  ex) $100, ₩100,000,000, €100,00
            intl_shipment(str): 배송비 ex) $100, ₩100,000,000, €100,00
            dome_shipment(str): "₩3,000"
            platform_fee(str): "₩7,000"
            card_fee_rate(float): 1.01

        Returns:
            Dict[str,Any]:

        """

        custom_fee, *_ = self._calc_custom_fee(price, intl_shipment, country)

        # create_dict
        key = [
            "price_kor",
            "intl_shipment",
            "dome_shipment",
            "platform_fee",
            "custom_fee",
        ]
        value = []
        for p in [price, intl_shipment, dome_shipment, platform_fee]:
            *_, curr_float = self.change_currency_to_buying_won(p)
            value.append(curr_float)

        value.append(custom_fee)
        d = dict(zip(key, value))

        # calculate_expense
        d["expense"] = (
            d["price_kor"] * card_fee_rate
            + d["intl_shipment"]
            + d["dome_shipment"]
            + d["platform_fee"]
            + custom_fee
        )

        # convert float to KRW
        expense_dict = {k: f"₩ {v:,.0f}" for k, v in d.items()}

        # add card_fee_rate
        expense_dict["card_fee_rate"] = str(card_fee_rate)

        return expense_dict

    def easy_change_to_krw(self, price: str) -> float:
        return self.change_currency_to_buying_won(price)[-1] * 1.02
