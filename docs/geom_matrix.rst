.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

Matrix
======

``import introcs``

We assume that all matrices at 4x4 matrices, allowing us to represent affine transforms
on homogeneous coordinates.  This class is primarily used for the graphics applications
in class.  For more general matrices, you should use ``numpy``.

Note that ``Matrix`` has no attributes.  This is what we call an *opaque class*.  In 
fact you cannot even pass attributes to the standard constructor.  You are expected
to make an identity matrix and then modify it via methods. If you want a special type
of matrix quickly, use one of the class methods.

This is a very advanced class for an introductory course and is almost always delegated
to behind-the-scenes parts of assignments.

Constructor
-----------
.. autoclass:: Matrix

Class Methods
-------------
Class methods are methods that are called with the class name before the period, instead
of an object.  They provide alternate constructors.

.. automethod:: Matrix.CreateTranslation
.. automethod:: Matrix.CreateRotation
.. automethod:: Matrix.CreateScale

Immutable Methods
-----------------
Immutable methods return a new object and do not modify the original.

.. automethod:: Matrix.invert
.. automethod:: Matrix.transpose
.. automethod:: Matrix.transform
.. automethod:: Matrix.copy

Mutable Methods
---------------
Mutable methods modify the underlying object.

.. automethod:: Matrix.inverse
.. automethod:: Matrix.transpost
.. automethod:: Matrix.translate
.. automethod:: Matrix.rotate
.. automethod:: Matrix.scale

Operators
---------
Operators redefine the meaning of the basic operations.  For example:: ``p * q`` is
the same as ``p.__mul__(q)``. 

.. automethod:: Matrix.__mul__
.. automethod:: Matrix.__imul__

.. toctree::
   :maxdepth: 2
   