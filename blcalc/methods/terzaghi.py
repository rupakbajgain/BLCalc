"""
Terzaghi method for square fondation
"""
#Use interpolation based method since using formula is not giving result
#Need fix

# (Note: from Boweles, Foundation analysis and design, "Terzaghi never
# explained..how he obtained Kpr used to compute Nγ")

#Terzaghi Table
t_tables={}
t_tables['phi']=[0,5,10,15,20,25,30,35,40,45,50]
t_tables['nc']=[5.7,7.3,9.6,12.9,17.7,25.1,37.2,57.8,95.7,172.3,347.5]
t_tables['nq']=[1,1.6,2.7,4.4,7.4,12.7,22.5,41.4,81.3,173.3,415.1]
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
    def __init__(self, mat):
        """
        mat is Layer material
        """
        self._mat = mat

    @staticmethod
    def Nc(phi):
        return get_table(t_tables, 'nc', phi)

    @staticmethod
    def Nq(phi):
        return get_table(t_tables, 'nq', phi)

    @staticmethod
    def Ny(phi):
        return get_table(t_tables, 'ny', phi)
    
    def calculate(self, depth):
        """
        Calcutate for provided depth
        """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
