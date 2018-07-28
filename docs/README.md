# Sphinx Documentation

This director contains the Makefile and ``.rst`` files for generating HTML documentation.  To compile the documentation, you will need the module ``sphinx`` installed in Python:
	
	pip install sphinx

The documentation was built with Sphinx 1.7.4.

To make the documentation, type
	
	make html

This will create a folder called ``_build`` with the html
inside of it.

While this documentation is fine by itself, we do not like this documentation for students.  Sphinx makes all methods look like classmethods (it prepends the method by the class name). To make some minor changes to this documentation, we have a "fix" script:
	
	./fixhtml.py
