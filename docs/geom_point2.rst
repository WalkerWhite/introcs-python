.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

Point2
======

``import introcs``

Points have position, but they do not have magnitude or direction.  Use the class 
:class:`Vector2` if you want direction.  Points support basic point arithmetic via the
operators.  However, pay close attention to how we handle typing.  For example, the 
difference between two points is a vector (as it should be).  But points may freely 
convert to vectors and vice versa.

Constructor
-----------
.. autoclass:: Point2

Attributes
----------
.. autoattribute:: Point2.x
.. autoattribute:: Point2.y

Immutable Methods
-----------------
Immutable methods return a new object and do not modify the original.

.. automethod:: Point2.toVector
.. automethod:: Point2.midpoint
.. automethod:: Point2.distance
.. automethod:: Point2.distance2
.. automethod:: Point2.under
.. automethod:: Point2.over
.. automethod:: Point2.isZero
.. automethod:: Point2.interpolant
.. automethod:: Point2.copy
.. automethod:: Point2.list

Mutable Methods
---------------
Mutable methods modify the underlying object.

.. automethod:: Point2.interpolate
.. automethod:: Point2.clamp

Operators
---------
Operators redefine the meaning of the basic operations.  For example:: ``p + q`` is
the same as ``p.__add__(q)``.  This allows us to treat points like regular numbers.
For the sake of brevity, we have not listed all operators -- only the most important
ones.  The equivalences are as follows::
	
	p == q     -->    p.__eq__(q)
	p < q      -->    p.__lt__(q)
	p + q      -->    p.__add__(q)
	p - q      -->    p.__sub__(q)
	p * q      -->    p.__mul__(q)
	q * p      -->    p.__rmul__(q)
	p / q      -->    p.__truediv__(q)
	q / p      -->    p.__rtruediv__(q)

.. automethod:: Point2.__eq__
.. automethod:: Point2.__lt__
.. automethod:: Point2.__add__
.. automethod:: Point2.__sub__
.. automethod:: Point2.__mul__
.. automethod:: Point2.__rmul__
.. automethod:: Point2.__truediv__
.. automethod:: Point2.__rtruediv__


.. toctree::
   :maxdepth: 2
   