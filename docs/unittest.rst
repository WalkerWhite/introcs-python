.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs

Unit Test Functions
===================

``import introcs``

These functions provides simple unit testing tools.  They is a replacement for the 
built-in Python package ``unittest``, which is much less user friendly and requires an 
understanding of object-oriented programming. If students are writing test cases from
the beginning, you are doing it wrong.

Type Checking
-------------
isfloat
^^^^^^^
.. autofunction:: isfloat

isint
^^^^^
.. autofunction:: isint

isbool
^^^^^^
.. autofunction:: isbool

Comparing Floats
----------------
isclose
^^^^^^^
.. autofunction:: isclose

allclose
^^^^^^^^
.. autofunction:: allclose


Asserting Tests
---------------
assert_equals
^^^^^^^^^^^^^
.. autofunction:: assert_equals

assert_not_equals
^^^^^^^^^^^^^^^^^
.. autofunction:: assert_not_equals

assert_true
^^^^^^^^^^^
.. autofunction:: assert_true

assert_false
^^^^^^^^^^^^
.. autofunction:: assert_false

assert_floats_equal
^^^^^^^^^^^^^^^^^^^
.. autofunction:: assert_floats_equal

assert_floats_not_equal
^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: assert_floats_not_equal

assert_float_lists_equal
^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: assert_float_lists_equal

assert_float_lists_not_equal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: assert_float_lists_not_equal

.. toctree::
   :maxdepth: 2
   