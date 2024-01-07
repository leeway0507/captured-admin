from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import dotenv_values
from typing import Literal


class DevEnv(BaseSettings):
    DB_USER_NAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DEV_DB_NAME: str
    TEST_DB_NAME: str

    ###
    KREAM_EMAIL: str
    KREAM_PASSWORD: str

    ###
    SHOP_BUYING_CURRENCY_API_KEY: str
    SHOP_CUSTOM_CURRENCY_APY_KEY: str
    SHOP_CURRENCY_DIR: str
    SHOP_LIST_DIR: str

    ###
    PLATFORM_PRODUCT_LIST_DIR: str
    PLATFORM_PRODUCT_PAGE_DIR: str

    SHOP_PRODUCT_LIST_DIR: str
    SHOP_PRODUCT_PAGE_DIR: str

    model_config = SettingsConfigDict(env_file=".env.dev")


class ProdEnv(BaseSettings):
    DB_USER_NAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    PRODUCTION_SIZE_BATCH: str

    PRODUCT_IMAGE_DIR: str

    CLOUDFRONT_DISTRIBUTION_ID: str

    model_config = SettingsConfigDict(env_file=".env.production")


dev_env = DevEnv(**dotenv_values(".env.dev"))  # type: ignore
prod_env = ProdEnv(**dotenv_values(".env.production"))  # type: ignore


def get_path(
    report_type: Literal["shop_page", "shop_list", "platform_page", "platform_list"]
):
    match report_type:
        case "shop_page":
            return dev_env.SHOP_PRODUCT_PAGE_DIR

        case "shop_list":
            return dev_env.SHOP_PRODUCT_LIST_DIR

        case "platform_page":
            return dev_env.PLATFORM_PRODUCT_PAGE_DIR

        case "platform_list":
            return dev_env.PLATFORM_PRODUCT_LIST_DIR
