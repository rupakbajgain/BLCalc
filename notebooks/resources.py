"""
Some initial setups
"""
#Here setup is done automatically
#Provide resources too later

import os
import sys

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from blcalc import root_dir

def test_data_dir():
    path = root_dir() / 'testdata'
    return path