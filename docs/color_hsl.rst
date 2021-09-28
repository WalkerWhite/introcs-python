.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

HSL
===

``import introcs``

This class represents an HSL color value.  As an additive color, it has conversion 
methods for ``tkinter``, ``kivy`` and ``PIL``.  However, most of these methods require
conversion to RGB color space before use.

HSL colors are represented by a double cone.  Pure color values such as red or green
are positioned at the vertical center of the cone, with a ``lightness`` value of 0.5.

Constructor
-----------

.. autoclass:: HSL

Attributes
----------

.. autoattribute:: HSL.hue
.. autoattribute:: HSL.saturation
.. autoattribute:: HSL.lightness

Methods
-------

.. automethod:: HSL.glColor
.. automethod:: HSL.webColor
.. automethod:: HSL.rgba

.. toctree::
   :maxdepth: 2
   