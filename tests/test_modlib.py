"""
Unit test for experimental modlib package

:author:  Walker M. White (wmw2)
:version: June 9, 2019
"""
import unittest
import os.path
from introcs.modlib import *
__guard__ = 0


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
        """
        Tests loading from a path.
        """
        path = [os.path.split(__file__)[0],'files']
        module = load_from_path('module1',path)
        
        self.assertEqual(module.x, 5)
        self.assertEqual(module.y, 'Hello')
    
    def test02_guard(self):
        """
        Test code rewriting against while loops
        """
        path = [os.path.split(__file__)[0],'files']
        with open(os.path.join(*path,'module2.py')) as file:
            module = file.read()
        
        copy = guard_loops(module,10,'__guard__').split('\n')
        self.assertEqual(copy[0], '__guard__ = 0')
        self.assertEqual(copy[8], 'global __guard__')
        self.assertEqual(copy[9], '__guard__ = 0')
        self.assertEqual(copy[10], 'while True and __guard__ < 10:')
        self.assertEqual(copy[11], '    __guard__ += 1')
        
        copy = guard_loops(module,10,'__guard__',False).split('\n')
        self.assertEqual(copy[7], 'global __guard__')
        self.assertEqual(copy[8], '__guard__ = 0')
        self.assertEqual(copy[9], 'while True and __guard__ < 10:')
        self.assertEqual(copy[10], '    __guard__ += 1')
        
        varbs = {}
        exec('\n'.join(copy),varbs)
        self.assertEqual(varbs['__guard__'], 10)
        self.assertEqual(varbs['x'], 5)
    
    def test03_Environment(self):
        """
        Test an environment with while-loops
        """
        path = [os.path.split(__file__)[0],'files']
        envr = Environment('module3',path)
        envr.enter('A',2,[1])
        
        self.assertTrue(envr.execute())
        self.assertEqual(len(envr.inputed),4)
        self.assertEqual(len(envr.printed),4)
        
        values = ('A','2','[1]','')
        for x in range(4):
            self.assertEqual(envr.inputed[x],'Item %s: ' % str(x))
            self.assertEqual(envr.printed[x],'Result is %s' % values[x])
        
        code = ''
        with open(os.path.join(*path,'module3.py')) as file:
            code = file.read()
        
        envr = Environment('other',code=code)
        envr.enter('A',2,[1])
        
        self.assertTrue(envr.execute())
        self.assertEqual(len(envr.inputed),4)
        self.assertEqual(len(envr.printed),4)
        
        values = ('A','2','[1]','')
        for x in range(4):
            self.assertEqual(envr.inputed[x],'Item %s: ' % str(x))
            self.assertEqual(envr.printed[x],'Result is %s' % values[x])
    
    def test04_errors(self):
        """
        Test environment error handling
        """
        path = [os.path.split(__file__)[0],'files']
        envr = Environment('module4',path)
        
        self.assertTrue(envr.execute())
        self.assertEqual(len(envr.printed),1)
        envr.module.foo()
        self.assertEqual(len(envr.printed),envr.LIMIT+2)
        self.assertEqual(envr.module.__guard__,envr.LIMIT)
        
        envr.reset()
        message = ''
        try:
            envr.module.hey()
        except Exception as a:
            message = envr.format_error(a)
        
        correct = 'Traceback (most recent call last):\n  File "tests/test_modlib.py", line 115, in test04_errors\n    envr.module.hey()\n  File "tests/files/module4.py", line 20, in hey\n    print(varb)\nNameError: name \'varb\' is not defined\n'
        self.assertEqual(message,correct)
        
        message = ''
        try:
            envr.module.bar(0)
        except Exception as a:
            message = envr.format_error(a)
        
        correct = 'Traceback (most recent call last):\n  File "tests/test_modlib.py", line 124, in test04_errors\n    envr.module.bar(0)\n  File "tests/files/module4.py", line 24, in bar\n    return 1/x\nZeroDivisionError: division by zero\n'
        self.assertEqual(message,correct)
        
        envr.reset(True)
        self.assertFalse(envr.execute())
        correct ='Bye\nTraceback (most recent call last):\n  File "/Users/wmwhite/Developer/introcs-python/introcs/modlib.py", line 306, in execute\n    exec(compiled, self._mods.__dict__)\n  File "tests/files/module4.py", line 31, in <module>\n    hey()\n  File "tests/files/module4.py", line 20, in hey\n    print(varb)\nNameError: name \'varb\' is not defined'
        message = '\n'.join(envr.printed)
        self.assertEqual(message,correct)


if __name__=='__main__':
  unittest.main( )
