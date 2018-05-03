"""
Type checking functions for strings

These functions examine strings and test if they are convertable to primitives.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


def isfloat(s):
    """
    Checks whether the string ``s`` represents a float.
    
    :param s: the candidate string to test
    :type s:  ``str``
    
    :return: True if s is the string representation of a number
    :rtype:  ``bool``
    """
    try:
        x = float(s)
        return True
    except:
        return False


def isint(s):
    """
    Checks whether the string ``s`` represents an integer.
    
    :param s: the candidate string to test
    :type s:  ``str``
    
    :return: True if s is the string representation of an integer
    :rtype:  ``bool``
    """
    try:
        x = int(s)
        return True
    except:
        return False


def isbool(s):
    """
    Checks whether the string ``s`` represents a boolean.
    
    The string requires Python capitalization (e.g. 'True', not 'true').
    
    :param s: the candidate string to test
    :type s:  ``str``
    
    :return: True if s is the string representation of a boolean
    :rtype:  ``bool``
    """
    if (type(s) != str):
        return False
    return (s == 'True' or s == 'False')