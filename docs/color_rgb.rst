.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

RGB
===
``import introcs``

This class represents a RGB (with optional alpha) color value.  It is the core color 
value, and the one most supported by graphics packages.  In particular, it has conversion 
methods for ``tkinter``, ``kivy`` and ``PIL``.

Constructor
-----------
.. autoclass:: RGB
	
Attributes
----------

.. autoattribute:: RGB.red
.. autoattribute:: RGB.green
.. autoattribute:: RGB.blue
.. autoattribute:: RGB.alpha

Methods
-------

.. automethod:: RGB.glColor
.. automethod:: RGB.webColor
.. automethod:: RGB.rgba

Class Methods
-------------
Class methods are methods that are called with the class name before the period, instead
of an object.  They provide alternate constructors.

.. automethod:: RGB.CreateName
.. automethod:: RGB.CreateWebColor

.. toctree::
   :maxdepth: 2
   