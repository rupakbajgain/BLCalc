"""
This is simple module which provides only one function

>>> add1(5)
6
"""

def add1(x):
    """
    Simple test function
    >>> add1(2)
    3
    """
    return x+1

if __name__ == "__main__":
    import doctest
    doctest.testmod()
