import sys

sys.path.append("/Users/yangwoolee/repo/captured/admin/backend")

import asyncio
import argparse
from datetime import datetime

from main import SizeBatchMain
from db.dev_db import (
    dev_session_local as dev_session,
    admin_session_local as admin_session,
)
from db.production_db import prod_session_local as prod_session
from components.env import get_path


def init_scrap_time():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple command-line interface.")

    # Define command-line arguments
    parser.add_argument("--batch_size", default=100, help="scrap size")
    parser.add_argument("--num_processor", default=6, help="processor size")
    parser.add_argument("--scrap_time", default=None, help="set_scrap_time")

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.scrap_time:
        scrap_time = args.scrap_time
    else:
        scrap_time = init_scrap_time()

    # Call the main function with the parsed arguments
    size_batch = SizeBatchMain(
        dev_session=dev_session,
        prod_session=prod_session,
        admin_session=admin_session,
        path=get_path("size_batch"),
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        size_batch.execute(
            batch_size=args.batch_size,
            num_processor=args.num_processor,
            scrap_time=scrap_time,
        )
    )
