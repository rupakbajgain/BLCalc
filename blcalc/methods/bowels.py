"""
Bowels method for 25mm settlement
"""

class Bowels:
    """
    Bowels method
    """
    @staticmethod
    def capacity(n60, depth_footing, width_footing):
        """
        Bearing capacity using bowels method
        """
        kd_factor = 1 + 0.33*depth_footing/width_footing
        if kd_factor>1.33:
            kd_factor=1.33
        settlement_mm = 25 #seviceability settlement mm
        if width_footing<1.22:
            return 19.16*n60*kd_factor*(settlement_mm/25.4)
        return 11.98 * n60 \
                * ((3.28*width_footing+1)/3.28*width_footing)**2 \
                *  kd_factor * (settlement_mm*25.4)

#From book guessed
#        change N60 to N55
#         N55 * 55 = N60 * 60
#        N55 = N60 * 60/55
#        F1 = 0.05
#        F2 = 0.08
#        F3 = 0.3
#        F4 = 1.2
#        if footing_width<F4:
#            return N55 / F1 * kd
#        return N55 / F2 * ((width_footing + F3)/width_footing)**2 * kd
