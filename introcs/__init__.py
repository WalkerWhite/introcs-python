"""
IntroCS modules

The purpose of this package is to provide proper masking, giving instructors more 
flexibility in how they arrange their Python course.  Masking takes a complex feature and 
hides it behind a simpler interface.  When the students have mastered that interface, the 
instructor can remove it and allow students direct access to the complex feature.

For example, this package provides non-method string functions for basic functionality 
such as searching, replacing, and testing.  This allows the students to write interesting 
text-manipulation functions when they are just starting out, without having to understand
the extra subtleties of method calls.  When they are ready to move on to method calls, the
students are free (and encouraged) to stop using these functions.

Key features include, but are not limited to

* Method-free string functions
* Simplified unit test utilities
* Simplified web connections (similar to the classic `urllib2`)
* Simplified color model interfaces

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
name = 'introcs'
from .geom import *
from .colors import *
from .strings import *
from .tuples import *
from .testcase import *
from .urltools import *