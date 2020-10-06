"""
Math module for degree,
and adding additional functions like cot
"""

import math

def sin(ang_rad):
    """
    sin in degree
    """
    return math.sin(ang_rad*math.pi/180)

def cos(ang_rad):
    """
    cos in degree
    """
    return math.cos(ang_rad*math.pi/180)

def tan(ang_rad):
    """
    tan in degree
    """
    return math.tan(ang_rad*math.pi/180)

def cot(ang_rad):
    """
    cot in degree
    """
    return 1/tan(ang_rad)#tan alreday defined

def atan(ang_rad):
    """
    tan^-1 in degree
    """
    return math.atan(ang_rad)*180/math.pi
