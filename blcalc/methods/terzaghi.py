"""
Terzaghi method for square fondation
"""
#TODO: consider local shear correction of soil
#Use interpolation based method since using formula is not giving result
#Need fix
from math import exp, pi

from ..dmath import tan, cos, sin

# (Note: from Boweles, Foundation analysis and design, "Terzaghi never
# explained..how he obtained Kpr used to compute Nγ")
# lets interpolate for Nγ
#Terzaghi Table
t_tables={}
t_tables['phi']=[0,5,10,15,20,25,30,35,40,45,50]
t_tables['ny']=[0,0.5,1.2,2.5,5,9.7,19.7,42.4,100.4,297.5,1153.0]

def get_table(tables, var, phi):
    """
    Table Searching function
    """
    if phi>=50:
        phi = 50
    #First find phi index
    idx=0
    while(True):
        if tables['phi'][idx]>=phi:
            break
        idx+=1
    if(tables['phi'][idx-1]==phi):
        return tables[var][idx-1]
    else:
        #Let's interpolate
        return (tables[var][idx]-tables[var][idx-1])/(tables['phi'][idx]-tables['phi'][idx-1])*(phi-tables['phi'][idx-1])+tables[var][idx-1]

class Terzaghi:
    """
    Provide methods to calculate terzaghi's calculations
    """
    def __init__(self, width_footing, depth_footing, water_depth=0):
        """
        Provide values that are common to all methods
        """
        dw1 = water_depth
        dw2 = water_depth - depth_footing
        #save some values
        self.rw1 = 1.
        self.rw2 = 1.
        self.width_footing = width_footing
        self.depth_footing = depth_footing
        #self.water_depth = water_depth
        if water_depth > width_footing + depth_footing: #water is too far down
            break
        top_dist_ratio = dw1/depth_footing
        bottom_dist_ratio = dw2/width_footing
        if top_dist_ratio <= 1: #water level above base level of foundation
            self.rw1 = 0.5 * (1 + top_dist_ratio)
        if 0<dw2/width_footing<=1:#water level below base level of foundation
            self.rw2 = 0.5 * (1 + bottom_dist_ratio)
    
    @staticmethod
    def Nc(phi):
        if phi<1e-7:
            phi=1e-7
        return (Terzaghi.Nq(phi)-1)/tan(phi)

    @staticmethod
    def Nq(phi):
        return (exp(2*pi*(0.75-phi/360)*tan(phi))) /(2 * cos(45+phi/2)**2)

    @staticmethod
    def Ny(phi):
        # return 2 * (Terzaghi.Nq(phi) + 1)* tan(phi) / (1+ 0.4*sin(4*pi))
        # this formula has error of 10%
        # better save table at 1deg interval
        return get_table(t_tables, 'ny', phi)

    def strip_capacity(self, cohesion, phi, gamma ,surchage=0):
        return cohesion*self.Nc(phi) + surchage*self.Nq(phi)*self.rw1 + 0.5*gamma*self.width_footing*Ny(phi)*self.rw2

    def square_capacity(self, cohesion, phi, gamma ,surchage=0):
        return 1.3*cohesion*self.Nc(phi) + surchage*self.Nq(phi)*self.rw1 + 0.4*gamma*self.width_footing*Ny(phi)*self.rw2

    def circular_capacity(self, cohesion, phi, gamma ,surchage=0):
        return 1.3*cohesion*self.Nc(phi) + surchage*self.Nq(phi)*self.rw1 + 0.3*gamma*self.width_footing*Ny(phi)*self.rw2

if __name__ == "__main__":
    import doctest
    doctest.testmod()

