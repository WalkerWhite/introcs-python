"""
Unit tests for the introc module

:author:  Walker M. White (wmw2)
:version: July 24, 2018
"""
import unittest

def suite():
    """
    Creates the test suite for all packages except turtle (which is graphical)
    """
    modules  = ( "test_colors",'test_geom','test_strings','test_tuples','test_testcase','test_filetools','test_urltools')
    alltests = unittest.TestSuite()
    for module in map(__import__, modules[:-1]):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')

