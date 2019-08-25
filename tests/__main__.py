"""
Unit tests for the introc module

:author:  Walker M. White (wmw2)
:version: June 9, 2019
"""
import unittest


def suite():
    """
    Creates the test suite for all packages except turtle (which is graphical)
    """
    modules  = ( 'test_testcase', 'test_strings','test_tuples','test_colors',
                 'test_geom','test_filetools','test_urltools','test_modlib',
                 'test_turtle') # Been burned too many times
    alltests = unittest.TestSuite()
    for module in map(__import__, modules):
        alltests.addTest(unittest.findTestCases(module))
    return alltests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
