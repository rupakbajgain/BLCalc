"""
Teng method
"""

class Teng:
    """
    Teng method
    """
    @staticmethod
    def capacity(N60, depth_footing, width_footing, depth_water=0):
        rw = 0.5*(1+depth_water/width_footing)
        rd = 1+depth_footing/width_footing
        if rd>2:
            rd=2
        return 53*(N60-3)*((width_footing+0.3)/(2*width_footing))**2 * rw*rd
