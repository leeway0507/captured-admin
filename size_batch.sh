#!/bin/zsh

source ~/.zshrc

cd /Users/yangwoolee/repo/captured/admin/backend

pyenv activate py310-admin

python shop_scrap/size_batch/batch_cli.py --batch_size 300

# python shop_scrap/size_batch/batch_cli.py --sync_only True --scrap_time 20240206-090219




