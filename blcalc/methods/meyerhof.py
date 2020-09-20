"""
Meyerhof method for square fondation
"""
from ..dmath import tan, cot
from math import exp, pi

class Meyerhof:
    """
    Provide methods to calculate meyerhof's calculations
    """
    def __init__(self, mat):
        """
        mat is Layer material
        """
        self._mat = mat

    @staticmethod
    def Nc(phi):
        if phi<1e-7:#checked for near value to 2+pi
            phi=1e-7
        return cot(phi)*(Meyerhof.Nq(phi)-1)

    @staticmethod
    def Nq(phi):
        return exp(pi*tan(phi))*(tan(45+phi/2))**2

    @staticmethod
    def Ny(phi):
        return (Meyerhof.Nq(phi)-1)*tan(1.4*phi)
    
    def calculate(self, depth):
        """
        Calcutate for provided depth
        """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
