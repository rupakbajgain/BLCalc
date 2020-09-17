"""
Default exported functions
"""

from pathlib import Path

def root_dir():
    """
    Returns parent directory location
    """
    return Path(__file__).parent.parent
