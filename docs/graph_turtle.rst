.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs.turtle

Turtle
======

``import introcs.turtle``

A graphics turtle is a pen that is controlled by direction and movement. The ``Turtle`` 
is a cursor that that you control by moving it left, right, forward, or backward.  
As it moves, it draws a line of the same color as the ``Turtle``.

Each turtle is attached to a :class:`Window` upon creation, and this window cannot
be change. If the window is closed or deleted, the turtle can no longer be used. 

Because of the overhead, this class is not included in the top level of the ``introcs`` 
module.  It must be imported separately as part of the ``introcs.turtle`` module.

Constructor
-----------
.. autoclass:: Turtle

Mutable Attributes
------------------
.. autoattribute:: Turtle.heading
.. autoattribute:: Turtle.speed
.. autoattribute:: Turtle.color
.. autoattribute:: Turtle.stroke
.. autoattribute:: Turtle.dash
.. autoattribute:: Turtle.visible
.. autoattribute:: Turtle.drawmode

Immutable Attributes
--------------------
These attributes may be read (e.g. used in an expression), but not altered.

.. autoattribute:: Turtle.x
.. autoattribute:: Turtle.y


Drawing Methods
---------------
All of these methods modify the underlying turtle object.

.. automethod:: Turtle.forward
.. automethod:: Turtle.backward
.. automethod:: Turtle.right
.. automethod:: Turtle.left
.. automethod:: Turtle.move

Update Methods
--------------
All of these methods are used to update the status of the associated :class:`Window`

.. automethod:: Turtle.flush
.. automethod:: Turtle.clear
.. automethod:: Turtle.reset

.. toctree::
   :maxdepth: 2