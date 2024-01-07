import os
import shutil


def remove_test_folder(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
