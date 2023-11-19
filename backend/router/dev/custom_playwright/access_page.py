from .page import KreamPage, customPage

page_dict = {}

init_page_error = "init_page가 None입니다. init 메서드를 먼저 실행해주세요."
browser_error = "browser가 None입니다. init 메서드를 먼저 실행해주세요."
login_password_error = "KREAM_PASSWORD가 설정되지 않았습니다. 재확인 바랍니다."


async def get_custom_page():
    """kream page 로드"""
    print("""kream page 로드""")
    if page_dict.get("custom_page") is None:
        custom_page = customPage()
        await custom_page.init()
        page_dict.update({"custom_page": custom_page})

    return page_dict.get("custom_page")


async def close_custom_page():
    if page_dict.get("custom_page"):
        b = page_dict.get("custom_page")
        assert isinstance(b, customPage), "custom_page is not KreamPage"
        assert b.browser, "browser does not exist"
        await b.close_browser()  # type: ignore
        page_dict.pop("custom_page")

    return {"result": "success"}


async def get_kream_page():
    """kream page 로드"""
    print("""kream page 로드""")
    if page_dict.get("kream_page") is None:
        kream_page = KreamPage()
        await kream_page.init()
        page_dict.update({"kream_page": kream_page})

    return page_dict.get("kream_page")


async def close_kream_page():
    """kream page 리로드"""

    if page_dict.get("kream_page"):
        b = page_dict.get("kream_page")
        assert isinstance(b, KreamPage), "kream_page is not KreamPage"
        assert b.browser, "browser does not exist"
        await b.close_browser()  # type: ignore
        page_dict.pop("kream_page")

    return {"result": "success"}
