"""
Material, represents a single soil material,
assume every soil is saturated for now
"""
from enum import Enum
import copy

from .base import Base
from .soilproperty import SoilProperty

class MaterialData(Enum):
    """
    Soil material info
    """
    WaterDepth = 'WaterDepth'

def _group_index_correction(group_index):
    """
    The input group_index may not contain proper group_index as required by problem
    Fix it,
    Like L was found in various logs as I
    """
    if len(group_index)==1:
        #just to make sure 2 letter group_index is available
        group_index=group_index+group_index
    if group_index[1]=='I':
        #Is I for intermediate[not standard] or is it actually L
        group_index=group_index[0]+'L'
    if not group_index[0] in ['S','M','G','C','P','O']:
        group_index=group_index[1]+group_index[1]
    if not group_index[0] in ['S','M','G','C','P','O']:
        #cannot determine make it clay
        #@TODO add fail here
        group_index='C'+group_index[1]
    return group_index

# _clamp result between min and max values
def _clamp(value, amin, amax):
    if value<amin:
        return amin
    if value>amax:
        return amax
    return value

class Material(Base):
    """
    It is a single soil material for a layer,
    it takes SPT and other previously known material properties,
    and group_indexves the unknown by analytical formulas,
    this contains datas like surchage too
    """
    def is_clayey(self):
        """
        Check first letter and determine if soil is clayey
        """
        group_index = self._data[SoilProperty.GI]
        return group_index[0] not in ['S','G']

    def _get_n(self):
        """
        Get n_60 value
        No overburden is applied since we have shallow depth(more errors)
        - Dilitarcy correction is applied for sand
        """#@Needs to fix it for general case
        n_60 = 0.55 * 1 * 1 * 0.75 * self._data[SoilProperty.SPT_N] /0.6
        if not self.is_clayey() and n_60>15: #apply dilitracy correction
            n_60 = 15 + 0.5 * (n_60 - 15)
        return n_60

    def _get_gamma(self):
        """
        Get value of gamma based on soil type
        """
        gamma = None
        if self.is_clayey():
            gamma = 16.8 + 0.15*self._data[SoilProperty.N60]
        else:
            gamma = 16 + 0.1 * self._data[SoilProperty.N60]
        gamma=_clamp(gamma,10,2.8*9.81)#do we need this
        return gamma

    # Note: The unconfined compressive strength value is two times undrained shear strength. The
    # ultimate bearing capacity is approximately six times the undrained shear strength where C in
    # CNc is the undrained shear strength. The value of Nc is 5.14 and 5.7 respectively by
    # Meyerhof and Terzaghi.
    # BC Mapping Bhadra 4

    @staticmethod
    def qu(N60):
        """
        Determine Qu from N60
        """
        return 0.29 * N60**0.72 * 100

    # correction from: https://civilengroup_indexneeringbible.com/subtopics.php?i=91
    def _get_cu(self):
        """
        Get cohesion of soil
        """
        c_undrained=0
        #group_index = self._data['GI']
        if self.is_clayey():
            c_undrained = self.qu(self._data[SoilProperty.N60])/2
            #c_undrained=_clamp(c_undrained, 10, 103)
        # Plasix calculation needs very small c_undrained
        #if c_undrained<0.21:
        #    c_undrained = 0.21
        #use 0.2 as per plasix recommendation
        return c_undrained#the cu is always 103 check with small value of n_60, some mistake maybe

    def _get_packing_state(self):
        """
        Get packing state table column
        """
        # Ok, first determining packing condition as per Table 2.4,
        s_phelp = [0,4,10,30,50]
        if self.is_clayey():
            s_phelp = [0,2,4,8,15,30]
        packing_case = 0 # Packing cases as per table
        for i,value in enumerate(s_phelp):
            if self._data[SoilProperty.N60]>value:
                packing_case=i
        return packing_case

    @staticmethod
    def phi(N60):
        """
        Determine phi from N60
        """
        return 27.1 + 0.3*N60 - 0.00054* N60**2

    def _get_phi(self):
        """
        Get phi of soil
        #Many tables are used need to be refactred
        """
        phi = self.phi(self._data[SoilProperty.N60])
        ### Ok let's remove for clay
        if self.is_clayey():
            phi=0 #very small value for plasix:::@TODO 0.01
        return phi

    def _get_e(self):
        """
        Elasticity
        """
        group_index = self._data[SoilProperty.GI]
        n_60 = self._data[SoilProperty.N60]
        packing_case = self._data[SoilProperty.packing_case]
        elasticity=None
        if self.is_clayey():
            if packing_case==0:#15-40
                elasticity= (15+40)/2 * n_60 * 100
            elif packing_case==1:#40-80
                elasticity= (40+80)/2 * n_60 * 100
            else:#80-200
                elasticity= (80+200)/2 * n_60 * 100
        else:
            if group_index[1] in ['M','C','P','O']:#with fines
                elasticity= 5 * n_60 * 100
            else: #The OCR condition of cohesionless test cannot be determined, assume NC sand
                elasticity= 10 * n_60 * 100
        return elasticity

    def __init__(self, input_data):
        """
        Save only use later when required
        """
        Base.__init__(self)
        self._data = input_data
        self._data[SoilProperty.GI] = _group_index_correction(self._data[SoilProperty.GI])
        if SoilProperty.N60 not in self._data:
            self._data[SoilProperty.N60] = self._get_n()
        if SoilProperty.packing_case not in self._data:
            self._data[SoilProperty.packing_case] = self._get_packing_state()
        if SoilProperty.gamma not in self._data:
            self._data[SoilProperty.gamma] = self._get_gamma()
        if SoilProperty.cohesion not in self._data:
            self._data[SoilProperty.cohesion] = self._get_cu()
        if SoilProperty.phi not in self._data:
            self._data[SoilProperty.phi] = self._get_phi()
        if SoilProperty.elasticity not in self._data:
            self._data[SoilProperty.elasticity] = self._get_e()
        if SoilProperty.nu not in self._data:
            if self.is_clayey():
                self._data[SoilProperty.nu] = 0.5
            else:
                self._data[SoilProperty.nu] = 0.3
        #update data to this dict
        self.set(self._data)

class LayerSoil(Base):
    """
    Use to determine multiple layer of soil
    so include surchage info also
    """
    def __init__(self, data, water_depth=0):
        super().__init__(self)
        self[MaterialData.WaterDepth] = water_depth
        #@TODO: fix other datas based on water depth
        self._data = data
        self._values = []
        prev_surchage = 0.
        prev_depth = 0.
        for layer in data:
            layer[SoilProperty.surcharge] = prev_surchage
            mat = Material(layer)
            res = mat.get()
            new_depth = res[SoilProperty.depth]
            prev_surchage += res[SoilProperty.gamma]*(new_depth-prev_depth)
            prev_depth=new_depth
            self._values.append(res)

    def get_avg_N(self, depth=0.):
        Ns = []# N values
        depths = []#depth total values
        row_start=0
        while self._values[row_start][SoilProperty.depth]<depth/2:
            row_start+=1
        row_end = row_start
        while self._values[row_end][SoilProperty.depth]<2*depth:
            row_end+=1
        if row_start==0:
            depths.append(0.)
        else:
            depth.append(self._values[row_start-1][SoilProperty.depth])
        for data in self._values[row_start:row_end]:
            Ns.append(data[SoilProperty.N60])
            depths.append(data[SoilProperty.depth])
        total_ns = 0.
        total_depth = 0.
        for (row, N_value) in enumerate(Ns):
            thickness = depths[row+1]-depths[row]
            total_ns += N_value*thickness
            total_depth += thickness
        return total_ns/total_depth

    def get(self, depth=None):
        """
        Return soil material at givel depth
        if no depth is given returns all saved materials
        """
        if depth is None:#Return all
            return self._values

        if depth<self._values[0][SoilProperty.depth]:
            mat = copy.copy(self._values[0])
            mat[SoilProperty.depth]=depth
            mat[SoilProperty.surcharge]=mat[SoilProperty.gamma]*depth
            return mat
        size = len(self._values)
        if depth>self._values[size-1][SoilProperty.depth]:
            mat = copy.copy(self._values[size-1])
            mat[SoilProperty.surcharge]=mat[SoilProperty.surcharge]+mat[SoilProperty.gamma]*(depth-mat[SoilProperty.depth])
            mat[SoilProperty.depth]=depth
            return mat
        row=0
        while self._values[row][SoilProperty.depth]<depth:
            row+=1
        mat = copy.copy(self._values[row])
        mat[SoilProperty.surcharge]= mat[SoilProperty.surcharge] - self._values[row-1][SoilProperty.gamma]*(mat[SoilProperty.depth]-depth)
        mat[SoilProperty.depth]=depth
        return mat

if __name__ == "__main__":
    import doctest
    doctest.testmod()
