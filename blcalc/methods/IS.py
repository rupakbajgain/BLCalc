"""
IS method

max settlement as per Skempton and Mc Donald
Clay: 45mm
Sand: 32mm
"""

class IS:
    """
    IS method for 40mm settlement
    """
    @staticmethod
    def capacity(N60, W, width_footing):
        return (N60-3)*((width_footing+0.3)/(2*width_footing))**2 * W
