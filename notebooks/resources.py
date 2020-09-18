"""
Some initial setups
"""
#Here setup is done automatically
#Provide resources too later

import os
import sys
from pathlib import Path

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

def test_data_dir():
    """
    Returns path of test datas like excel
    Used for test or notebook
    """
    path = Path(__file__).parent.parent / 'testdata'
    return path
