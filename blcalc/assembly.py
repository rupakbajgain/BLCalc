"""
Combine the various info to single datas
> now footing and soil layers
"""
from enum import Enum

from .base import Base

class AssemblyType(Enum):
    """
    Supported footing types
    """
    Footing = 'Footing'
    SoilLayer = 'SoilLayer'

class Assembly(Base):
    """
    Combine both footing and layers to one
    """
    def __init__(self, footing=None, soil_layer=None):
        Base.__init__(self)
        self[AssemblyType.Footing] = footing
        self[AssemblyType.SoilLayer] = soil_layer

if __name__ == "__main__":
    import doctest
    doctest.testmod()
