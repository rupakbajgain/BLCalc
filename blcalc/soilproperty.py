"""
Diffrent properties of soil
"""
from enum import Enum

class SoilProperty(Enum):
    """
    Diffrent soil properties
    """
    cohesion = 'cohesion'
    SPT_N = 'SPT_N'
    N60 = 'N60'
    depth = 'depth'
    gamma = 'gamma'
    surcharge = 'surcharge'
    phi = 'phi'
    GI = 'GI'
    elasticity = 'elasticity'
    packing_case = 'packing_case'
    nu = 'nu'
