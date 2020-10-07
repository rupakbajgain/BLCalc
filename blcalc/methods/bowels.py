"""
Bowels method for 25mm settlement
"""

class Bowels:
    """
    Bowels method
    """
    @staticmethod
    def capacity(N60, depth_footing, width_footing):
        kd = 1 + 0.33*depth_footing/width_footing
        if kd>1.33:
            kd=1.33
        S0 = 25 #seviceability settlement mm
        if width_footing<1.22:
            return 19.16*N60*kd*(S0/25.4)
        return 11.98*N60* ((3.28*width_footing+1)/3.28*width_footing)**2 *  kd * (S0*25.4)
"""
        #change N60 to N55
        # N55 * 55 = N60 * 60
        N55 = N60 * 60/55
        F1 = 0.05
        F2 = 0.08
        F3 = 0.3
        F4 = 1.2
        if footing_width<F4:
            return N55 / F1 * kd
        return N55 / F2 * ((width_footing + F3)/width_footing)**2 * kd
"""
