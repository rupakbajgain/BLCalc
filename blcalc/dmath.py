"""
Math module for degree,
and adding additional functions like cot
"""

import math

def sin(x):
    return math.sin(x*math.pi/180)

def cos(x):
    return math.cos(x*math.pi/180)

def tan(x):
    return math.tan(x*math.pi/180)

def cot(x):
    return 1/tan(x)#tan alreday defined
