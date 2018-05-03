"""
Cornell implementation of the Tk Turtle

This module is preferable to the default turtle module for several reasons.  First, it 
makes it easier to support simultaneous turtle windows.  Second, it provides support for 
custom color models.  Finally, the attributes and methods have been streamlined to make 
them easier to understand for beginners.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
from .window import Window
from .turtle import Turtle
from .pen import Pen