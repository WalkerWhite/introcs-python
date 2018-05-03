"""
Color constants.

These are some predefined color constants so that we do not have to construct the 
objects. The constants in this module are all defined in the RGB color space. 

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
from .models import RGB

# COLOR CONSTANTS
#: The color white in the default sRGB space.
WHITE = RGB(255, 255, 255)

#: The color light gray in the default sRGB space.
LIGHT_GRAY = RGB(192, 192, 192)

#: The color gray in the default sRGB space.
GRAY = RGB(128, 128, 128)

#: The color dark gray in the default sRGB space.
DARK_GRAY = RGB(64, 64, 64)

#: The color black in the default sRGB space.
BLACK = RGB(0, 0, 0)

#: The color red, in the default sRGB space.
RED = RGB(255, 0, 0)

#: The color pink in the default sRGB space.
PINK = RGB(255, 175, 175)

#: The color orange in the default sRGB space.
ORANGE = RGB(255, 200, 0)

#: The color yellow in the default sRGB space.
YELLOW = RGB(255, 255, 0)

#: The color green in the default sRGB space.
GREEN = RGB(0, 255, 0);

#: The color magenta in the default sRGB space.
MAGENTA = RGB(255, 0, 255)

#: The color cyan in the default sRGB space.
CYAN = RGB(0, 255, 255)

#: The color blue in the default sRGB space.
BLUE = RGB(0, 0, 255)