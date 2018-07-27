.. introcs documentation master file, created by
   sphinx-quickstart on Thu Jul 26 09:50:44 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: introcs.filetools

File Functions
==============

``import introcs.filetools``

This functions are useful handling simple data science assignments. They read and write
popular (text-based) file formats.  The most value functions are :func:`read_csv` and
:func:`write_csv`, as these are non-trivial to implement.

These functions are relatively new and untested.  Because of that reason, they are not 
included in the top level of the ``introcs`` module.  They must be imported separately.

Reading
-------
read_txt
^^^^^^^^
.. autofunction:: read_txt

read_json
^^^^^^^^^
.. autofunction:: read_json

read_csv
^^^^^^^^
.. autofunction:: read_csv

read_package
^^^^^^^^^^^^
.. autofunction:: read_package

Writing
-------
There is no write-version of :func:`read_package`.  Any data value that could be written
to a package can be written to a single JSON file more efficiently.

write_txt
^^^^^^^^^
.. autofunction:: write_txt

write_json
^^^^^^^^^^
.. autofunction:: write_json

write_csv
^^^^^^^^^
.. autofunction:: write_csv

Errors
------
.. autoclass:: FileToolError

.. toctree::
   :maxdepth: 2
   