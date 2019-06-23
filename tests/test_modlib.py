"""
Unit test for experimental modlib package

:author:  Walker M. White (wmw2)
:version: June 9, 2019
"""
import unittest
import os.path
from introcs.modlib import *

class ModuleTest(unittest.TestCase):
    """
    Unit test for the experimental modlib package
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

    def test01_load_from_path(self):
        path = [os.path.split(__file__)[0],'files']
        module = load_from_path('module1',path)

        self.assertEqual(module.x, 5)
        self.assertEqual(module.y, 'Hello')

    def test02_Environment(self):
        path = [os.path.split(__file__)[0],'files']
        envr = Environment('module2',path,*('A',2,[1]))

        envr.execute()
        self.assertEqual(len(envr.inputed),4)
        self.assertEqual(len(envr.printed),4)

        values = ('A','2','[1]','')
        for x in range(4):
            self.assertEqual(envr.inputed[x],'Item %s: ' % str(x))
            self.assertEqual(envr.printed[x],'Result is %s' % values[x])


if __name__=='__main__':
  unittest.main( )
