# Student Tools for Beginning Python

Python is an extremely popular language for introduction to computing courses at various 
universities. However, many Python features require knowledge of advance language elements
before they can be used.  For example, the Unit Testing framework is extremely comple and 
is typically inaccessible to a beginning student.  Similarly, Python has moved all string 
functionality to method calls, which are confusing for a student just starting out with 
functions.

The purpose of this package is to provide proper masking, giving instructors more 
flexibility in how they arrange their Python course.  Masking takes a complex feature and 
hides it behind a simpler interface.  When the students have mastered that interface, the 
instructor can remove it and allow students direct access to the complex feature.

For example, this package provides non-method string functions for basic functionality 
such as searching, replacing, and testing.  This allows the students to write interesting 
text-manipulation functions when they are just starting out, without having to understand
the extra subtleties of method calls.  When they are ready to move on to method calls, the
students are free (and encouraged) to stop using these functions.

For a complete list of modules provided by this package, see the associated documentation. 
Key features include, but are not limited to

* Method-free string functions
* Simplified unit test utilities
* Simplified web connections (similar to the classic `urllib2`)
* Simplified color model interfaces

These packages were developed as part of the introduction to computing sequence at 
Cornell University. However, they are free to all educators that might find them useful.
