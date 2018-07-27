.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs.turtle

Pen
===

``import introcs.turtle``

A graphics pen is like a :class:`Turtle` except that it does not have a heading, and 
there is no ``drawmode`` attribute. Instead, the pen relies on explicit drawing commands 
such as :meth:`~Pen.drawLine` or :meth:`~Pen.drawOval`.

Another difference with the pen is that it can draw solid shapes.  The pen has an 
attribute called :attr:`~Pen.solid`.  When this attribute is set to ``True``, it will fill the 
insides of any polygon traced by its :meth:`~Pen.drawLine` method. However, the fill will not 
be completed until `solid` is set to False, or the :meth:`~Pen.move` method is invoked.

Each pen is attached to a :class:`Window` upon creation, and this window cannot
be change. If the window is closed or deleted, the pen can no longer be used. 

Because of the overhead, this class is not included in the top level of the ``introcs`` 
module.  It must be imported separately as part of the ``introcs.turtle`` module.

Constructor
-----------
.. autoclass:: Pen

Mutable Attributes
------------------
.. autoattribute:: Pen.speed
.. autoattribute:: Pen.solid
.. autoattribute:: Pen.edgecolor
.. autoattribute:: Pen.fillcolor
.. autoattribute:: Pen.stroke
.. autoattribute:: Pen.dash
.. autoattribute:: Pen.visible

Immutable Attributes
--------------------
These attributes may be read (e.g. used in an expression), but not altered.

.. autoattribute:: Pen.x
.. autoattribute:: Pen.y
.. autoattribute:: Pen.color

Drawing Methods
---------------
All of these methods modify the underlying turtle object.

.. automethod:: Pen.move
.. automethod:: Pen.drawLine
.. automethod:: Pen.drawTo
.. automethod:: Pen.drawOval
.. automethod:: Pen.drawRectangle

Update Methods
--------------
All of these methods are used to update the status of the associated :class:`Window`

.. automethod:: Pen.flush
.. automethod:: Pen.clear
.. automethod:: Pen.reset

.. toctree::
   :maxdepth: 2