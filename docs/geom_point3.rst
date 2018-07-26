.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

Point3
======

``import introcs``

Points have position, but they do not have magnitude or direction.  Use the class 
:class:`Vector3` if you want direction.  Points support basic point arithmetic via the
operators.  However, pay close attention to how we handle typing.  For example, the 
difference between two points is a vector (as it should be).  But points may freely 
convert to vectors and vice versa.

The name ``Point`` is an alias for ``Point3``.

Constructor
-----------
.. autoclass:: Point3

Attributes
----------
.. autoattribute:: Point3.x
.. autoattribute:: Point3.y

Immutable Methods
-----------------
Immutable methods return a new object and do not modify the original.

.. automethod:: Point3.toVector
.. automethod:: Point3.midpoint
.. automethod:: Point3.distance
.. automethod:: Point3.distance2
.. automethod:: Point3.under
.. automethod:: Point3.over
.. automethod:: Point3.isZero
.. automethod:: Point3.interpolant
.. automethod:: Point3.copy
.. automethod:: Point3.list

Mutable Methods
---------------
Mutable methods modify the underlying object.

.. automethod:: Point3.interpolate
.. automethod:: Point3.clamp

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

.. automethod:: Point3.__eq__
.. automethod:: Point3.__lt__
.. automethod:: Point3.__add__
.. automethod:: Point3.__sub__
.. automethod:: Point3.__mul__
.. automethod:: Point3.__rmul__
.. automethod:: Point3.__truediv__
.. automethod:: Point3.__rtruediv__

.. toctree::
   :maxdepth: 2
   