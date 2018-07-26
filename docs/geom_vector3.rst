.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

Vector3
=======

``import introcs``

Vectors have magnitude and direction, but they do not have position.  Use the class
:class:`Point3` if you want position.  Vectors support basic point arithmetic via the
operators.  However, pay close attention to how we handle typing.  For example, the 
adding a point to a vector produces another point (as it should).  But vectors may freely 
convert to points and vice versa.

The name ``Vector`` is an alias for ``Vector3``.

Constructor
-----------
.. autoclass:: Vector3

Attributes
----------
.. autoattribute:: Vector3.x
.. autoattribute:: Vector3.y

Immutable Methods
-----------------
Immutable methods return a new object and do not modify the original.

.. automethod:: Vector3.toPoint
.. automethod:: Vector3.length
.. automethod:: Vector3.length2
.. automethod:: Vector3.angle
.. automethod:: Vector3.isUnit
.. automethod:: Vector3.normal
.. automethod:: Vector3.interpolant
.. automethod:: Vector3.dot
.. automethod:: Vector3.cross
.. automethod:: Vector3.projection

.. automethod:: Vector3.interpolant
.. automethod:: Vector3.copy
.. automethod:: Vector3.list

Mutable Methods
---------------
Mutable methods modify the underlying object.

.. automethod:: Vector3.normalize
.. automethod:: Vector3.crossify
.. automethod:: Vector3.project
.. automethod:: Vector3.interpolate

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

.. automethod:: Vector3.__eq__
.. automethod:: Vector3.__lt__
.. automethod:: Vector3.__add__
.. automethod:: Vector3.__sub__
.. automethod:: Vector3.__mul__
.. automethod:: Vector3.__rmul__
.. automethod:: Vector3.__truediv__
.. automethod:: Vector3.__rtruediv__
.. toctree::
   :maxdepth: 2
   