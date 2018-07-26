"""
Unit test for the tuples package

:author:  Walker M. White (wmw2)
:version: July 20, 2018
"""
import unittest
import numpy
from introcs import tuples


class GeomTest(unittest.TestCase):
    """
    Unit test for the tuples package
    """
    
    def assertClose(self,given,correct):
        """
        Replacement to assertAlmostEquals that works on list.
        
        This method uses numpy.allclose to compare given and expected.  If they are not
        equal, it results in an error.
        
        :param given: The value produced by the test
        :type given:  any
        
        :param correct: The expected value
        :type correct:  any
        """
        message = '%s != %s' % (repr(given),repr(correct))
        self.assertTrue(numpy.allclose(given,correct),message)
    
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
    
    def test_tuples_search(self):
        """
        Tests the tuple search functions.
        """
        for w in [(1,2,3),(1,2,1),(1,2,2,1,1,3),(3.5,'a',True),('a',True,True,'a'),((1,2),(3,4),(1,2))]:
            for i in [1,2,'a',True,3.5,(1,2)]:
                self.assertEqual(tuples.count_tup(w,i),w.count(i))
                self.assertEqual(tuples.find_tup(w,i),w.index(i) if i in w else -1)
                for p in [(0,3),(1,-1),(0,-3),(1,2),(2,-3)]:
                    self.assertEqual(tuples.count_tup(w,i,*p),w[p[0]:p[1]].count(i))
                    self.assertEqual(tuples.find_tup(w,i,*p),w.index(i,*p) if i in w[p[0]:p[1]] else -1)
                    if i in w[p[0]:p[1]]:
                        self.assertEqual(tuples.index_tup(w,i,*p),tuples.find_tup(w,i,*p))
                        self.assertEqual(tuples.rindex_tup(w,i,*p),tuples.rfind_tup(w,i,*p))
                    else:
                        self.assertRaises(ValueError,tuples.index_tup,w,i,*p)
                        self.assertRaises(ValueError,tuples.rindex_tup,w,i,*p)
        self.assertEqual(tuples.rfind_tup((1,2,2,1,1,3),1),4)
        self.assertEqual(tuples.rfind_tup((1,2,2,1,1,3),2),2)
        self.assertEqual(tuples.rfind_tup((1,2,2,1,1,3),4),-1)
        self.assertEqual(tuples.rfind_tup((1,2,2,1,1,3),1,None,-2),3)
        self.assertEqual(tuples.rfind_tup((1,2,2,1,1,3),2,0,2),1)
        self.assertEqual(tuples.rfind_tup((1,2,2,1,1,3),2,0,1),-1)
    
    def test_tuples_replace(self):
        """
        Tests the tuple replace function.
        """
        self.assertEqual(tuples.replace_tup((1,2,2,1,1,3),3,4),(1,2,2,1,1,4))
        self.assertEqual(tuples.replace_tup((1,2,2,1,1,3),2,4),(1,4,4,1,1,3))
        self.assertEqual(tuples.replace_tup((1,2,2,1,1,3),1,4),(4,2,2,4,4,3))
        self.assertEqual(tuples.replace_tup((1,2,2,1,1,3),5,4),(1,2,2,1,1,3))
        self.assertEqual(tuples.replace_tup((1,2,2,1,1,3),1,4,0),(1,2,2,1,1,3))
        self.assertEqual(tuples.replace_tup((1,2,2,1,1,3),1,4,1),(4,2,2,1,1,3))
        self.assertEqual(tuples.replace_tup((1,2,2,1,1,3),1,4,2),(4,2,2,4,1,3))
        
        

if __name__=='__main__':
  unittest.main( )

