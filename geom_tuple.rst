.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs.tuple

Tuples (Class)
==============

``import introcs``

The ``Tuple`` classes are not the same thing as the built-in ``tuple`` type of Python.  
They are the base class of various point and vector classes and are used to properly
type arithmetic operations.  The two classes are :class:`Tuple2` and :class:`Tuple3`,
so there should be no confusion with the built-in type.

You will almost never use these classes directly.  You should use one of the point or
vector classes instead.

Tuple2
------

.. autoclass:: Tuple2

	
	
Attributes
^^^^^^^^^^
.. autoattribute:: Tuple2.x
.. autoattribute:: Tuple2.y

Methods
^^^^^^^

Operators
^^^^^^^^^
.. automethod:: Tuple2.__add__
.. automethod:: Tuple2.__sub__

Point3
------
.. autoclass:: Tuple3
	
Attributes
^^^^^^^^^^

.. autoattribute:: Tuple3.x
.. autoattribute:: Tuple3.y
.. autoattribute:: Tuple3.z

Methods
^^^^^^^


.. toctree::
   :maxdepth: 2
   