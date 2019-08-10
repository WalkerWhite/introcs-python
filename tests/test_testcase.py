"""
Unit test for the test case package

This tests the custom unittest package that we provide in introcs to make everything
easier.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
import unittest
import numpy


# This is necessary for command interception 
display = print
thequit = quit

class UnitTestTest(unittest.TestCase):
    """
    Unit test for the url tools package
    """
    
    def setUp(self):
        """
        Initializes a unit test
        """
        locs = locals()
        globs = globals()
        globs['__builtins__']['quit']  = self.doquit
        globs['__builtins__']['print'] = self.doprint
        
        self._test = __import__('introcs.testcase',globs,locs)
        self.clear()
    
    def tearDown(self):
        """
        Completes a unit test
        """
        globs = globals()
        globs['__builtins__']['quit']  = display
        globs['__builtins__']['print'] = thequit
        self._test = None
    
    def doquit(self):
        """
        Performs a faux application quit
        """
        self._quit = True
    
    def isquit(self):
        """
        Returns true if the assert quit the program.
        """
        return self._quit
    
    def doprint(self, *objects, sep=' ', end='\n', file=None, flush=False):
        """
        Captures a print statement to an internal attribute for recording.
        """
        from io import StringIO
        outs = StringIO()
        display(*objects,sep=sep,end=end,file=outs,flush=flush)
        self._outp.append(outs.getvalue())
        outs.close()
    
    def getprint(self):
        """
        Returns the attributes recorded form print statements.
        """
        return self._outp
    
    def clear(self):
        """
        Resets the recording of any assert messages.
        """
        self._quit = False
        self._outp = []
    
    def test03_quit(self):
        """
        Tests the quit command and interception.
        """
        def invoke(): # Since this function unwraps
            self._test.quit_with_error('Hello world!')
        invoke()
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'Hello world!')
        self.assertEqual(self._outp[1][:7],'Line 85')
        self.clear()
    
    def test04_asserts_basic(self):
        """
        Tests the basic unit test asserts.
        """
        self._test.assert_equals(1,1)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_equals(1,2) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_equals: expected 1 but instead got 2')
        self.assertEqual(self._outp[1][:7],'Line 99')
        self.clear()
        
        self._test.assert_not_equals(1,2)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_not_equals(1,1) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_not_equals: expected something different from 1')
        self.assertEqual(self._outp[1][:8],'Line 109')
        self.clear()
        
        self._test.assert_true(1==1)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_true(0) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_true: 0 evaluates to False')
        self.assertEqual(self._outp[1][:8],'Line 119')
        self.clear()
        
        self._test.assert_false(1==2)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_false(1) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_false: 1 evaluates to True')
        self.assertEqual(self._outp[1][:8],'Line 129')
        self.clear()
    
    def test05_asserts_floats(self):
        """
        Tests the float unit test asserts.
        """        
        self._test.assert_floats_equal(1.0000001,1.0000002)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_floats_equal('a',1) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_floats_equal: first argument 'a' is not a number")
        self.assertEqual(self._outp[1][:8],'Line 143')
        self.clear()
        
        self._test.assert_floats_equal(1,'a') # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_floats_equal: second argument 'a' is not a number")
        self.assertEqual(self._outp[1][:8],'Line 149')
        self.clear()
        
        self._test.assert_floats_equal(1.1,1.2) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_floats_equal: expected 1.1 but instead got 1.2')
        self.assertEqual(self._outp[1][:8],'Line 155')
        self.clear()
        
        self._test.assert_floats_not_equal(1.1,1.2)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_floats_not_equal('a',1) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_floats_not_equal: first argument 'a' is not a number")
        self.assertEqual(self._outp[1][:8],'Line 165')
        self.clear()
        
        self._test.assert_floats_not_equal(1,'a') # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_floats_not_equal: second argument 'a' is not a number")
        self.assertEqual(self._outp[1][:8],'Line 171')
        self.clear()
        
        self._test.assert_floats_not_equal(1.0000001,1.0000002) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_floats_not_equal: expected something different from 1.0000001')
        self.assertEqual(self._outp[1][:8],'Line 177')
        self.clear()
        
        self._test.assert_float_lists_equal([2,1.0000001],(2,1.0000002))
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_float_lists_equal('a',[1]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: first argument 'a' is not a sequence")
        self.assertEqual(self._outp[1][:8],'Line 187')
        self.clear()
        
        self._test.assert_float_lists_equal((1,),'a') # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: second argument 'a' is not a sequence")
        self.assertEqual(self._outp[1][:8],'Line 193')
        self.clear()
        
        self._test.assert_float_lists_equal((1,'a'),[2,1]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: first argument (1, 'a') has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 199')
        self.clear()
        
        self._test.assert_float_lists_equal([2,1],(1,'a')) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: second argument (1, 'a') has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 205')
        self.clear()
        
        self._test.assert_float_lists_equal([2],(2,1)) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: sequences [2] and (2, 1) have different sizes")
        self.assertEqual(self._outp[1][:8],'Line 211')
        self.clear()
        
        self._test.assert_float_lists_equal((2,1),[2]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: sequences (2, 1) and [2] have different sizes")
        self.assertEqual(self._outp[1][:8],'Line 217')
        self.clear()
        
        self._test.assert_float_lists_equal([1.1,2.1],[1.1,2.2]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_float_lists_equal: expected [1.1, 2.1] but instead got [1.1, 2.2]')
        self.assertEqual(self._outp[1][:8],'Line 223')
        self.clear()
        
        self._test.assert_float_lists_equal([[1,2],[3,4]],[[1,2],[3,4]])
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_float_lists_equal([[1,2],[3,4]],[[1,2],[3,5]]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: expected [[1, 2], [3, 4]] but instead got [[1, 2], [3, 5]]")
        self.assertEqual(self._outp[1][:8],'Line 233')
        self.clear()
        
        self._test.assert_float_lists_equal([[1,2],[3,4]],[[1,2]]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: sequences [[1, 2], [3, 4]] and [[1, 2]] have different sizes")
        self.assertEqual(self._outp[1][:8],'Line 239')
        self.clear()
        
        self._test.assert_float_lists_equal([[1,2],[3,4]],[[1,2],[3,'a']]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: second argument [[1, 2], [3, 'a']] has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 245')
        self.clear()
    
        self._test.assert_float_lists_equal([[1,2],[3,'a']],[[1,2],[3,4]]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_equal: first argument [[1, 2], [3, 'a']] has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 251')
        self.clear()
        
        self._test.assert_float_lists_not_equal([1.1,2.1],(1.1,2.2))
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_float_lists_not_equal('a',[1]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_not_equal: first argument 'a' is not a sequence")
        self.assertEqual(self._outp[1][:8],'Line 261')
        self.clear()
        
        self._test.assert_float_lists_not_equal((1,),'a') # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_not_equal: second argument 'a' is not a sequence")
        self.assertEqual(self._outp[1][:8],'Line 267')
        self.clear()
        
        self._test.assert_float_lists_not_equal((1,'a'),[2,1]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_not_equal: first argument (1, 'a') has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 273')
        self.clear()
        
        self._test.assert_float_lists_not_equal([2,1],(1,'a')) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_not_equal: second argument (1, 'a') has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 279')
        self.clear()
        
        self._test.assert_float_lists_not_equal([2],(2,1)) # Pay attention to the line number
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_float_lists_not_equal((2,1),[2]) # Pay attention to the line number
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_float_lists_not_equal([2,1.0000001],(2,1.0000002)) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),'assert_float_lists_not_equal: expected something different from [2, 1.0000001]')
        self.assertEqual(self._outp[1][:8],'Line 293')
        self.clear()
        
        self._test.assert_float_lists_not_equal([[1,2],[3,4]],[[1,2],[3,5]])
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_float_lists_not_equal([[1,2],[3,4]],[[1,2],[3,4]]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_not_equal: expected something different from [[1, 2], [3, 4]]")
        self.assertEqual(self._outp[1][:8],'Line 303')
        self.clear()
        
        self._test.assert_float_lists_not_equal([[1,2],[3,4]],[[1,2],[3,'a']]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_not_equal: second argument [[1, 2], [3, 'a']] has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 309')
        self.clear()
    
        self._test.assert_float_lists_not_equal([[1,2],[3,'a']],[[1,2],[3,4]]) # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_float_lists_not_equal: first argument [[1, 2], [3, 'a']] has non-numeric values")
        self.assertEqual(self._outp[1][:8],'Line 315')
        self.clear()
    
    def test06_asserts_error(self):
        """
        Tests the enforcement assertion
        """
        
        # Basic enforcement
        def func1(s):
            assert type(s) == str
            assert s != ''
            return s[0]
        
        # Enforced with other errors
        def func2(s):
            if type(s) != str:
                raise TypeError()
            if s == '':
                raise ValueError()
            return s[0]
        
        # Multiple arguments
        def func3(x,y):
            assert type(x) == int
            assert type(y) == int
            return x/y
        
        
        self._test.assert_error(1,2)  # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: argument 1 is not callable")
        self.assertEqual(self._outp[1][:8],'Line 347')
        self.clear()
        
        self._test.assert_error(func1,'a')  # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: call func1('a') did not crash but instead returned 'a'")
        self.assertEqual(self._outp[1][:8],'Line 353')
        self.clear()
        
        self._test.assert_error(func1,2)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_error(func1,'')
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_error(func2,'a')
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: call func2('a') did not crash but instead returned 'a'")
        self.assertEqual(self._outp[1][:8],'Line 367')
        self.clear()
        
        self._test.assert_error(func2,2)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: call func2(2) crashed with TypeError, not AssertionError")
        self.assertEqual(self._outp[1][:8],'Line 373')
        self.clear()
        
        self._test.assert_error(func2,2,error=TypeError)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_error(func2,'',error=TypeError)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: call func2('') crashed with ValueError, not TypeError")
        self.assertEqual(self._outp[1][:8],'Line 383')
        self.clear()
        
        self._test.assert_error(func2,'',error=ValueError)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_error(func3,3,2)  # Pay attention to the line number
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: call func3(3, 2) did not crash but instead returned 1.5")
        self.assertEqual(self._outp[1][:8],'Line 393')
        self.clear()
        
        self._test.assert_error(func3,3.0,2)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_error(func3,3.0,2,error=TypeError)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: call func3(3.0, 2) crashed with AssertionError, not TypeError")
        self.assertEqual(self._outp[1][:8],'Line 403')
        self.clear()
        
        self._test.assert_error(func3,3,2.0)
        self.assertFalse(self.isquit())
        self.clear()
        
        self._test.assert_error(func3,3,0)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),"assert_error: call func3(3, 0) crashed with ZeroDivisionError, not AssertionError")
        self.assertEqual(self._outp[1][:8],'Line 413')
        self.clear()
        
        self._test.assert_error(func3,3,0,error=ZeroDivisionError)
        self.assertFalse(self.isquit())
        self.clear()
    
    def test07_messages(self):
        """
        Tests the custom assert messages
        """
        message = 'Test1'
        self._test.assert_equals(1, 2, message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test2'
        self._test.assert_not_equals(1, 1, message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test3'
        self._test.assert_true(False, message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test4'
        self._test.assert_false(True, message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test5'
        self._test.assert_floats_equal(1,1.001, message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test6'
        self._test.assert_floats_not_equal(1,1.000001, message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test7'
        self._test.assert_floats_not_equal(1,1.000001, message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test8'
        self._test.assert_float_lists_equal([1,2],[1.001,2], message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test9'
        self._test.assert_float_lists_not_equal([1,2],[1.000001,2], message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        def func3(x,y):
            assert type(x) == int
            assert type(y) == int
            return x/y
        
        message = 'Test9'
        self._test.assert_error(1,2,message=message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test10'
        self._test.assert_error(func3,3,2,message=message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
        
        message = 'Test11'
        self._test.assert_error(func3,3,0,message=message)
        self.assertTrue(self.isquit())
        self.assertEqual(self._outp[0].strip(),message)
        self.clear()
    
    def test01_checks(self):
        """
        Tests the type checks.
        """
        self.assertTrue(self._test.isint(1.0))
        self.assertTrue(self._test.isint(1))
        self.assertTrue(self._test.isint('1'))
        self.assertFalse(self._test.isint('1.0'))
        self.assertFalse(self._test.isint('1e1'))
        self.assertFalse(self._test.isint('e1'))
        
        self.assertTrue(self._test.isfloat(1.0))
        self.assertTrue(self._test.isfloat(1))
        self.assertTrue(self._test.isfloat('1.0'))
        self.assertTrue(self._test.isfloat('1e1'))
        self.assertFalse(self._test.isfloat('e1'))
        
        self.assertTrue(self._test.isbool(True))
        self.assertTrue(self._test.isbool(1.0))
        self.assertTrue(self._test.isbool(1))
        self.assertTrue(self._test.isbool('True'))
        self.assertTrue(self._test.isbool('False'))
        self.assertFalse(self._test.isbool('true'))
        self.assertFalse(self._test.isbool('1'))
        self.assertFalse(self._test.isbool('1.0'))
        self.assertFalse(self._test.isbool('1e1'))
        self.assertFalse(self._test.isbool('e1'))
    
    def test02_compares(self):
        """
        Tests the float comparisons.
        """
        self.assertTrue(self._test.isclose(1,1.000001))
        self.assertFalse(self._test.isclose(1,1.001))
        self.assertEqual(self._test.isclose( (1,2),(1.000001,2.001) ), [True,False])
        self.assertEqual(self._test.isclose( (1,2),(1.001,2.000001) ), [False,True])
        self.assertEqual(self._test.isclose( ((1,2),(3,4)), ((1,2.0000001),(5,4)) ),   
                                             [[True,True],[False,True]])

        self.assertEqual(self._test.allclose( (1,2),(1.000001,2.001) ),False)
        self.assertEqual(self._test.allclose( (1,2),(1.001,2.000001) ),False)
        self.assertEqual(self._test.allclose( (1,2),(1.000001,2.000001) ),True)
        self.assertEqual(self._test.allclose( ((1,2),(3,4)), ((1,2.0000001),(5,4)) ),  False) 
        self.assertEqual(self._test.allclose( ((1,2),(3,4)), ((1,2.0000001),(3,4)) ),  True) 

if __name__=='__main__':
  unittest.main( )

