import asyncio

from playwright.async_api import Page


async def load_page(page: Page, url):
    """페이지 로드"""
    await asyncio.sleep(1)
    await page.goto(url)
    await page.wait_for_load_state(state="networkidle")
    await page.wait_for_timeout(1000)
    return page


async def save_cookies(page):
    # Get cookies from the current page
    cookies = await page.context.cookies()

    # Save cookies to a file or database
    # In this example, cookies are saved to a file named 'cookies.json'
    with open('router/dev/kream/cookie/cookies.json', 'w') as file:
        file.write(str(cookies))


async def load_cookies(page):
    # Load cookies from a file or database
    # In this example, cookies are loaded from a file named 'cookies.json'
    with open('router/dev/kream/cookie/cookies.json', 'r') as file:
        cookies = eval(file.read())

    # Set cookies in the current page
    await page.context.add_cookies(cookies)