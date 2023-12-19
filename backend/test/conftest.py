#
# conftest.py
import sys
from os.path import dirname as d
from os.path import abspath, join
import os

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

# default Root
os.chdir(root_dir)
