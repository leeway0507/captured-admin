import pytest
import os

import pandas as pd
from backend.components.dev.platform.platform_data_loader import PlatformDataLoader

path = "/Users/yangwoolee/repo/captured/admin/backend/test/dev/platform/platform_data/product_card_page"
report_path = os.path.join(path, "_report")

test_platform = "kream"
test_brand = "barbour"
test_scrap_date = "231217-115135"
test_template_key = ["len", "kream_id_list", "data"]


@pytest.fixture(scope="module")
def platform_data():
    instance = PlatformDataLoader(
        path=path,
        platform=test_platform,
        brand=test_brand,
        scrap_date=test_scrap_date,
    )
    yield instance


def test_get_last_scrap_date_name():
    # When
    last_file_name = PlatformDataLoader.get_last_scrap_date_name(report_path)

    # Then
    assert last_file_name == test_scrap_date


def test_load_file(platform_data: PlatformDataLoader):
    # Given
    platform_data.file_type = "buy_and_sell"

    # When
    data = platform_data.load_file()

    # Then
    assert len(data) == 44


def test_get_unique_kream_id(platform_data: PlatformDataLoader):
    # Given
    platform_data.file_type = "buy_and_sell"
    data = platform_data.load_file()

    # When
    kream_list = platform_data.get_unique_kream_id(data)

    # Then
    assert len(kream_list) == 8
    assert type(kream_list[0]) == int


def test_set_template(platform_data: PlatformDataLoader):
    # Given
    platform_data.file_type = "buy_and_sell"
    data = platform_data.load_file()

    # When
    template = platform_data.set_template(data)

    # Then
    assert list(template) == test_template_key


def test_load_buy_and_sell(platform_data: PlatformDataLoader):
    # When
    template = platform_data.load("buy_and_sell")

    # Then
    assert list(template) == test_template_key


def test_product_bridge(platform_data: PlatformDataLoader):
    # When
    template = platform_data.load("product_bridge")

    # Then
    assert list(template) == test_template_key


def test_product_detail(platform_data: PlatformDataLoader):
    # When
    template = platform_data.load("product_detail")

    # Then
    assert list(template) == test_template_key


def test_trading_volume(platform_data: PlatformDataLoader):
    # When
    template = platform_data.load("trading_volume")

    # Then
    assert list(template) == test_template_key
