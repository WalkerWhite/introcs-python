.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Color Classes
=============

``import introcs``

We provide classes for three different color models: RGB, CMYK, HSV. Each of these classes
have methods to allow them to be used in popular graphic packages like ``tkinter``, ``kivy``
and ``PIL``. We also support parsing string color representations such as TCL/Tk color
names, or web colors (e.g. ``'#ff00ff'``).

Classes
-------

.. toctree::
   :maxdepth: 1
   
   color_rgb
   color_cmyk
   color_hsl
   color_hsv
