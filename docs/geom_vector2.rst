.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

Vector2
=======

``import introcs``

Vectors have magnitude and direction, but they do not have position.  Use the class
:class:`Point2` if you want position.  Vectors support basic point arithmetic via the
operators.  However, pay close attention to how we handle typing.  For example, the 
adding a point to a vector produces another point (as it should).  But vectors may freely 
convert to points and vice versa.

Constructor
-----------
.. autoclass:: Vector2

Attributes
----------
.. autoattribute:: Vector2.x
.. autoattribute:: Vector2.y

Immutable Methods
-----------------
Immutable methods return a new object and do not modify the original.

.. automethod:: Vector2.toPoint
.. automethod:: Vector2.length
.. automethod:: Vector2.length2
.. automethod:: Vector2.angle
.. automethod:: Vector2.isUnit
.. automethod:: Vector2.normal
.. automethod:: Vector2.rotation
.. automethod:: Vector2.interpolant
.. automethod:: Vector2.dot
.. automethod:: Vector2.cross
.. automethod:: Vector2.perp
.. automethod:: Vector2.rperp
.. automethod:: Vector2.projection

.. automethod:: Vector2.interpolant
.. automethod:: Vector2.copy
.. automethod:: Vector2.list

Mutable Methods
---------------
Mutable methods modify the underlying object.

.. automethod:: Vector2.normalize
.. automethod:: Vector2.rotate
.. automethod:: Vector2.project
.. automethod:: Vector2.interpolate

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

.. automethod:: Vector2.__eq__
.. automethod:: Vector2.__lt__
.. automethod:: Vector2.__add__
.. automethod:: Vector2.__sub__
.. automethod:: Vector2.__mul__
.. automethod:: Vector2.__rmul__
.. automethod:: Vector2.__truediv__
.. automethod:: Vector2.__rtruediv__
.. toctree::
   :maxdepth: 2
   