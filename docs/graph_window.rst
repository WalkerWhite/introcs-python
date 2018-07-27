.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs.turtle

Window
======

``import introcs.turtle``

A window is a GUI canvas that supports turtle (:class:`Turtle` or :class:`Pen`) graphics.
You construct a window before adding the turtle or pen.  A window can have as many 
turtles or pens as you want at the same time.  It can also have no turtles or pens.

While windows may be resized, your should take great care when resizing them while drawing.  
Since the origin is typically the center of the window, resizing a window will shift the 
drawing implements (:class:`Turtle` and :class:`Pen` objects) to a new position.  For 
the most part, this should preserve coordinates, but round-off error may be an issue.

Because of the overhead, this class is not included in the top level of the ``introcs`` 
module.  It must be imported separately as part of the ``introcs.turtle`` module.


Constructor
-----------
.. autoclass:: Window

Mutable Attributes
------------------
.. autoattribute:: Window.x
.. autoattribute:: Window.y
.. autoattribute:: Window.width
.. autoattribute:: Window.height
.. autoattribute:: Window.title
.. autoattribute:: Window.resizable

Immutable Attributes
--------------------
These attributes may be read (e.g. used in an expression), but not altered.

.. autoattribute:: Window.turtles
.. autoattribute:: Window.pens


Methods
-------
All of these methods modify the underlying window object.

.. automethod:: Window.setPosition
.. automethod:: Window.setSize
.. automethod:: Window.setMaxSize
.. automethod:: Window.setMinSize
.. automethod:: Window.iconify
.. automethod:: Window.deiconify
.. automethod:: Window.flush
.. automethod:: Window.clear
.. automethod:: Window.dispose
.. automethod:: Window.beep


Errors
------
.. currentmodule:: introcs.turtle.window

.. autoclass:: AttachmentError

.. toctree::
   :maxdepth: 2
