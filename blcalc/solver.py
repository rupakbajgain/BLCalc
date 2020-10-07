"""
Apply appropriate method based on data provided
"""

from enum import Enum
from .assembly import AssemblyType
from .footing import FootingType, FootingData
from .material import MaterialData
from .methods.terzaghi import Terzaghi
from .methods.meyerhof import Meyerhof
from .methods.hansen import Hansen
from .methods.vesic import Vesic
from .methods.bowels import Bowels
from .methods.IS import IS
from .methods.teng import Teng
from .soilproperty import SoilProperty

class Methods(Enum):
    """
    Supported solution methods
    """
    Terzaghi = 'Terzaghi'
    Meyerhof = 'Meyerhof'
    Hansen = 'Hansen'
    Bowels = 'Bowels'
    Vesic = 'Vesic'
    IS = 'IS'
    Teng = 'Teng'

FOS = 3

class Solver:
    """
    Apply appropriate method based on data provided
    """
    def __init__(self, assembly):
        """
        init solver
        """
        self._footing = assembly[AssemblyType.Footing]
        self._soilLayer = assembly[AssemblyType.SoilLayer]

    def calc_terzaghi(self):
        """
        Calculate based on terzaghi method
        """
        terzaghi = Terzaghi(
                    self._footing[FootingData.Width],
                    self._footing[FootingData.Depth],
                    self._soilLayer[MaterialData.WaterDepth]
                )
        footing_type = self._footing[FootingData.Type]
        mat = self._soilLayer.get(self._footing[FootingData.Depth])
        if footing_type==FootingType.Circular:
            return terzaghi.circular_capacity(
                        mat[SoilProperty.cohesion],
                        mat[SoilProperty.phi],
                        mat[SoilProperty.gamma],
                        mat[SoilProperty.surcharge]
                    ) / FOS
        elif footing_type==FootingType.Square:
            return terzaghi.square_capacity(
                        mat[SoilProperty.cohesion],
                        mat[SoilProperty.phi],
                        mat[SoilProperty.gamma],
                        mat[SoilProperty.surcharge]
                    ) / FOS
        return terzaghi.strip_capacity(
                        mat[SoilProperty.cohesion],
                        mat[SoilProperty.phi],
                        mat[SoilProperty.gamma],
                        mat[SoilProperty.surcharge]
                    ) / FOS

    def calc_meyerhoff(self):
        meyerhof = Meyerhof(
                    self._footing[FootingData.Width],
                    self._footing[FootingData.Depth],
                    self._soilLayer[MaterialData.WaterDepth]
                )
        mat = self._soilLayer.get(self._footing[FootingData.Depth])
        return meyerhof.capacity(
                    mat[SoilProperty.cohesion],
                    mat[SoilProperty.phi],
                    mat[SoilProperty.gamma],
                    self._footing[FootingData.Length],
                    mat[SoilProperty.surcharge]
                ) / FOS

    def calc_hansen(self):
        hansen = Hansen(
                    self._footing[FootingData.Width],
                    self._footing[FootingData.Depth],
                    self._soilLayer[MaterialData.WaterDepth]
                )
        mat = self._soilLayer.get(self._footing[FootingData.Depth])
        return hansen.capacity(
                    mat[SoilProperty.cohesion],
                    mat[SoilProperty.phi],
                    mat[SoilProperty.gamma],
                    self._footing[FootingData.Length],
                    mat[SoilProperty.surcharge]
                ) / FOS

    def calc_vesic(self):
        vesic = Vesic(
                    self._footing[FootingData.Width],
                    self._footing[FootingData.Depth],
                    self._soilLayer[MaterialData.WaterDepth]
                )
        mat = self._soilLayer.get(self._footing[FootingData.Depth])
        return vesic.capacity(
                    mat[SoilProperty.cohesion],
                    mat[SoilProperty.phi],
                    mat[SoilProperty.gamma],
                    self._footing[FootingData.Length],
                    mat[SoilProperty.surcharge]
                ) / FOS

    def calc_bowels(self):
        avg_N60 = self._soilLayer.get_avg_N(self._footing[FootingData.Depth])
        return Bowels.capacity(
            avg_N60,
            self._footing[FootingData.Depth],
            self._footing[FootingData.Width]
        )

    def calc_IS(self):
        avg_N60 = self._soilLayer.get_avg_N(self._footing[FootingData.Depth])
        return IS.capacity(
            avg_N60,
            self._footing[FootingData.Depth],
            self._footing[FootingData.Width]
        )

    def calc_teng(self):
        avg_N60 = self._soilLayer.get_avg_N(self._footing[FootingData.Depth])
        return Teng.capacity(
            avg_N60,
            self._footing[FootingData.Depth],
            self._footing[FootingData.Width],
            self._soilLayer[MaterialData.WaterDepth]
        )

    def run(self, methods=Methods): #all method if not selected
        """
        Run selected method based on method
        """
        results = {}
        for method in methods:
            if method == Methods.Terzaghi:
                results[method] = self.calc_terzaghi()
            elif method == Methods.Meyerhof:
                results[method] = self.calc_meyerhoff()
            elif method == Methods.Hansen:
                results[method] = self.calc_hansen()
            elif method == Methods.Bowels:
                results[method] = self.calc_bowels()
            elif method == Methods.Vesic:
                results[method] = self.calc_vesic()
            elif method == Methods.IS:
                results[method] = self.calc_IS()
            elif method == Methods.Teng:
                results[method] = self.calc_teng()
            else:
                pass
        return results

if __name__ == "__main__":
    import doctest
    doctest.testmod()
