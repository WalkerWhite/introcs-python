.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Graphics Turtle
===============

``import introcs.turtle``

A quick perusal of the Python documentation shows that Python already has
a `graphics turtle <https://docs.python.org/3/library/turtle.html>`_.  But that turtle
has several problems.  First of all, it requires that the turtle be a *singleton*; you
can only have one turtle at a time.  There is no reason for this.  Why cannot you 
have multiple windows open, each with its own turtle?

In addition, we really do not like that the official turtle uses the module as a 
class-style object. This is an design decision from the old days of Python that does 
not make sense in a Python 3 world.  Module garbage collection is very murky, 
so it is much better to use classes when you want to implement something mutable.

In implementing this class, we were inspired by the Java version of the turtle from the
`ACM graphics package <https://cs.stanford.edu/people/eroberts/jtf/javadoc/student/acm/graphics/package-summary.html>`_.  
This is a much better design of the turtle, and was used at Cornell for several years 
before the switch to Python. Indeed, the 
`Tkinter canvas <http://effbot.org/tkinterbook/canvas.htm>`_ used to implement the turtle
works very much like the ACM package.

We have taken advantage of this reimplementation to add new features -- like dashes and
stroke width -- that did not exist in the original turtle.  We also have proper support 
for speed 0 (which is not correctly implemented in the Python turtle). The lack of an 
instantaneous turtle has been a large source of student complaints.

Because of the overhead, these classes are not included in the top level of the
``introcs`` module.  They must be imported separately.

Classes
-------

.. toctree::
   :maxdepth: 1
   
   graph_window
   graph_turtle
   graph_pentool
