from typing import List, Dict
from datetime import datetime, timedelta
from db.dev_db import AdminDB
from db.tables_kream import (
    KreamProductCardTable,
    KreamProductIdBridgeTable,
    KreamBuyAndSellTable,
    KreamTradingVolumeTable,
)
from sqlalchemy import select
from model.db_model_kream import KreamProductCardSchema
from model.response_kream_table import ResponseMarketPrice
import pandas as pd


class KreamProductCardWithProductIdSchema(KreamProductCardSchema):
    product_id: str


class KreamTable:
    def __init__(self, max_day: int = 20):
        self.admin_db = AdminDB()
        self.max_day = max_day

    async def get_kream_prod_card(self, type: str, content: str):
        stmt = getattr(LoadStrategy(), type)(content)
        result = await self.admin_db.execute(stmt)

        return [
            KreamProductCardWithProductIdSchema(
                **{**row[0].to_dict(), **row[1].to_dict()}
            )
            for row in result
        ]

    async def get_buy_and_sell(self, prod_id: str):
        kream_id = await self.get_kream_id(prod_id)
        stmt = select(KreamBuyAndSellTable).where(
            KreamBuyAndSellTable.kream_id == kream_id
        )
        result = await self.admin_db.execute(stmt)
        return [row[0].to_dict() for row in result]

    async def get_trading_volume(self, prod_id: str):
        kream_id = await self.get_kream_id(prod_id)
        stmt = select(KreamTradingVolumeTable).where(
            KreamTradingVolumeTable.kream_id == kream_id,
            KreamTradingVolumeTable.trading_at > self._base_date(),
        )
        result = await self.admin_db.execute(stmt)
        return [row[0].to_dict() for row in result]

    async def get_kream_id(self, prod_id: str):
        stmt = select(KreamProductIdBridgeTable.kream_id).filter(
            KreamProductIdBridgeTable.product_id == prod_id
        )
        prod_id_list = await self.admin_db.execute(stmt)
        return prod_id_list[0][0]

    async def preprocess_trading_volume(self, trading_volume: List[Dict]):
        raw_df = pd.DataFrame(trading_volume)
        df = raw_df.groupby(["kream_product_size"])["price"].describe().reset_index()
        df = df.rename(columns={"50%": "median"})

        # get lightening info
        lightening_df = (
            raw_df.groupby(["kream_product_size"])["lightening"]
            .value_counts()
            .reset_index()
        )
        lightening_df = lightening_df[lightening_df["lightening"] == True][
            ["kream_product_size", "count"]
        ]
        lightening_df = lightening_df.rename(columns={"count": "lightening"})
        df = pd.merge(df, lightening_df, on="kream_product_size", how="left").fillna(0)
        return df

    async def get_market_price_info(self, prod_id: str):
        buy_and_sell = await self.get_buy_and_sell(prod_id)
        trading_volume = await self.get_trading_volume(prod_id)

        if not trading_volume:
            return {"baseDate": self._base_date(), "data": []}

        buy_and_sell_df = pd.DataFrame(buy_and_sell)
        trading_volume_df = await self.preprocess_trading_volume(trading_volume)
        merged_df = self.merge_trading_volume_with_buy_and_sell(
            buy_and_sell_df, trading_volume_df
        )

        response_model = [
            ResponseMarketPrice(**{str(k): v for k, v in row.items()})
            for row in merged_df.to_dict("records")
        ]

        return {"baseDate": self._base_date(), "data": response_model}

    def merge_trading_volume_with_buy_and_sell(
        self, buy_and_sell_df: pd.DataFrame, trading_volume_df: pd.DataFrame
    ):
        df = pd.merge(
            buy_and_sell_df,
            trading_volume_df,
            on="kream_product_size",
            how="left",
        ).fillna(0)
        return df[
            [
                "kream_product_size",
                "buy",
                "sell",
                "count",
                "min",
                "median",
                "max",
                "lightening",
            ]
        ]

    def _base_date(self):
        max_day = timedelta(self.max_day)
        now = datetime.now()
        return now - max_day


class LoadStrategy:
    def productId(self, content: str):
        content_list = content.split(",")
        return (
            select(KreamProductCardTable, KreamProductIdBridgeTable)
            .join(KreamProductIdBridgeTable)
            .where(KreamProductIdBridgeTable.product_id.in_(content_list))
        )

    def brandName(self, content: str):
        return (
            select(KreamProductCardTable, KreamProductIdBridgeTable)
            .join(KreamProductIdBridgeTable)
            .where(KreamProductCardTable.brand_name == content)
            .order_by(KreamProductCardTable.updated_at.desc())
        )
