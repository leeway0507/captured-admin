import os
import json
from typing import List, Dict
from shop_scrap.page.main import ShopPageMain
from shop_scrap.size_batch.batch_data_processor import SizeBatchProcessor
from db.scrap_data_sync_db import ShopPageDataSyncDB, SizeDataSyncProdDB
from sqlalchemy.orm import sessionmaker
from components.messanger.slack import send_slack_message


def logExcutionResult(method):
    async def wrapper(self, *args, **kwargs):
        result = await method(self, *args, **kwargs)
        status = {method.__name__: result}
        await self.TempFile.append_temp_file("batch_status", status)

        return result

    return wrapper


class SizeBatchMain(ShopPageMain):
    def __init__(
        self,
        path: str,
        prod_session: sessionmaker,
        dev_session: sessionmaker,
        admin_session: sessionmaker,
    ):
        super().__init__(path, admin_session)
        self.path = path
        self.admin_session = admin_session
        self.prod_session = prod_session
        self.dev_session = dev_session
        self.slack_chennel_id = "C06D5UGUL6R"

    async def execute(
        self, scrap_time: str, batch_size: int = 100, num_processor: int = 6
    ):
        await self.init(batch_size, num_processor, scrap_time)
        await self.scrap_candidate_page()
        await self.sync_scrap_data_to_shop_db()
        await self.create_prod_batch_data()
        await self.sync_prod_batch_data_to_prod_db()
        self.send_status_to_sns(f"{self.scrap_time} Done!!")

    async def init(self, batch_size: int, num_processor: int, scrap_time: str):
        self.batch_size = batch_size
        self.num_processor = num_processor
        self.scrap_time = scrap_time

        self.target_list = await self.extract_target_list()
        self.main_scraper = await self.main_scraper_factory.size_batch(
            self.target_list, self.num_processor, self.scrap_time
        )
        await self.main_scraper.init()
        self.TempFile = self.main_scraper.TempFile

        self.SizeBatchProcessor = SizeBatchProcessor(
            self.admin_session, self.prod_session, self.path, self.scrap_time
        )

        self.ShopPageSyncDB = ShopPageDataSyncDB(self.admin_session, self.path)
        self.ShopPageSyncDB.scrap_time = self.scrap_time

        self.ShopDataSyncProdDB = SizeDataSyncProdDB(
            self.dev_session, self.prod_session, self.path, self.scrap_time
        )

        return await self.save_meta_data()

    @logExcutionResult
    async def save_meta_data(self):
        scrap_meta_data = {
            "scrap_time": self.main_scraper.scrap_time,
            "batch_size": self.batch_size,
            "num_processor": self.num_processor,
            "job": self.target_list,
            "job_len": len(self.target_list),
        }
        self._send_start_batch_info_to_sns(scrap_meta_data)
        return scrap_meta_data

    def _send_start_batch_info_to_sns(self, data: Dict):
        scrap_meta_data = data.copy()

        scrap_meta_data.pop("job")

        scrap_info = f"Size Batch 스크랩 시작 : {data['scrap_time']} \n"
        text = json.dumps(scrap_meta_data, indent=2)
        self.send_status_to_sns(scrap_info + text)

    def send_status_to_sns(self, text: str):
        # send_slack_message(self.slack_chennel_id, text)
        ...

    @logExcutionResult
    async def scrap_candidate_page(self):
        await self.main_scraper.scrap()
        await self.Report.save_report()
        await self.DataSave.save_scrap_data()
        return {"status": "success"}

    async def extract_target_list(self):
        return await self.Target.extract_data(str(self.batch_size))

    async def sync_scrap_data_to_shop_db(self):
        await self.ShopPageSyncDB.sync_data()

    @logExcutionResult
    async def create_prod_batch_data(self):
        await self.SizeBatchProcessor.execute()
        return {"status": "success"}

    @logExcutionResult
    async def sync_prod_batch_data_to_prod_db(self):
        await self.ShopDataSyncProdDB.sync_data()
        return {"status": "success"}

    @logExcutionResult
    async def _test_logExcutionResult(self):
        return {"status": "success"}
