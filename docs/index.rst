.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The ``introcs`` Package
=======================

The purpose of this package is to provide proper masking, giving instructors more 
flexibility in how they arrange their Python course.  Masking takes a complex feature and 
hides it behind a simpler interface.  When the students have mastered that interface, the 
instructor can remove it and allow students direct access to the complex feature.

For example, this package provides non-method string functions for basic functionality 
such as searching, replacing, and testing.  This allows the students to write interesting 
text-manipulation functions when they are just starting out, without having to understand
the extra subtleties of method calls.  When they are ready to move on to method calls, the
students are free (and encouraged) to stop using these functions.


Contents
--------
.. toctree::
    :maxdepth: 1
    :name: indextoc
    
    strings
    tuples
    colors
    geometry
    unittest
    urltools
    graphics
    filetools


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
