import asyncio
import pytest
import pytest_asyncio
from components.dev.utils.browser_controller import PwBrowserController
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_start_browser():
    await PwBrowserController.start()
