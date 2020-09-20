"""
Hansen method for square fondation
"""
from ..dmath import tan, cot
from math import exp, pi
from .meyerhof import Meyerhof

class Hansen:
    """
    Provide methods to calculate hansen's calculations
    """
    def __init__(self, mat):
        """
        mat is Layer material
        """
        self._mat = mat

    @staticmethod
    def Nc(phi):
        return Meyerhof.Nc(phi)

    @staticmethod
    def Nq(phi):
        return Meyerhof.Nq(phi)

    @staticmethod
    def Ny(phi):
        return 1.8*(Hansen.Nq(phi)-1)*tan(phi)
    
    def calculate(self, depth):
        """
        Calcutate for provided depth
        """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
