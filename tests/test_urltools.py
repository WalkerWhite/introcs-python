"""
Unit test for url tools package

This is a tricky package to have stable test cases for since websites change all the
time (and we do not really want all that much more traffic to the course web pages).
We picked Gutenberg as that is pretty stable.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
import unittest
import numpy
from introcs import urltools


class UrlToolsTest(unittest.TestCase):
    """
    Unit test for the url tools package
    """
    
    def setUp(self):
        """
        Initializes a unit test (UNUSED)
        """
        pass
    
    def tearDown(self):
        """
        Completes a unit test (UNUSED)
        """
        pass
    
    def test_urlread(self):
        """
        Tests the urlread function.
        """
        import re
        pattern = re.compile(r'<title.*?>(?P<title>(.+?))</title>')
        result = urltools.urlread('http://www.gutenberg.org')
        match  = pattern.search(result)
        self.assertTrue(match)
        self.assertEqual(match['title'],'Gutenberg')
        
        result = urltools.urlread('http://www.google.com')
        match  = pattern.search(result)
        self.assertEqual(match['title'],'Google')
    
    def test_urlread(self):
        """
        Tests the urlinfo function.
        """
        result = urltools.urlinfo('http://www.gutenberg.org')
        self.assertEqual(result['Content-Type'],'text/html; charset=UTF-8')
        
        # Why Google, Why?
        result = urltools.urlinfo('http://www.google.com')
        self.assertEqual(result['Content-Type'],'text/html; charset=ISO-8859-1')


if __name__=='__main__':
  unittest.main( )

