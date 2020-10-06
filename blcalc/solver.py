"""
Apply appropriate method based on data provided
"""

from enum import Enum

class Methods(Enum):
    """
    Supported solution methods
    """
    Terzaghi = 'Terzaghi'
    Meyerhof = 'Meyerhof'

class Solver:
    """
    Apply appropriate method based on data provided
    """
    def __init__(self, assembly):
        """
        init solver
        """
        self._assembly = assembly

    def run(self, method):
        """
        Run selected method based on method
        """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
