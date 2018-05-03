"""
Classes for three different color models, with some constants.

The classes are RGB, CMYK, HSV.  The constants in this module are all defined in the RGB 
color space.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
from .models import RGB, HSV, CMYK
from .constants import *
from .tkcolor import is_tkcolor