"""
Properties of footing
"""

from enum import Enum

from .base import Base

class FootingType(Enum):
    """
    Supported footing types
    """
    Circular = 'Circular'
    Square = 'Square'
    Strip = 'Strip'

class Footing(Base):
    """
    Footing base class
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
