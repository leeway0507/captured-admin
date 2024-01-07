#
# conftest.py
import sys
from os.path import dirname, abspath

import os

root_dir = dirname(dirname(abspath(__file__)))

sys.path.append(root_dir)

# default Root
os.chdir(root_dir)
