"""
Unit test for strings package

:author:  Walker M. White (wmw2)
:version: July 20, 2018
"""
import unittest
import numpy
from introcs import strings


class GeomTest(unittest.TestCase):
    """
    Unit test for the strings package
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
    
    def test_strings_test(self):
        """
        Tests the boolean string functions..
        """
        for c in ['a','a1','A','A1','1','1.0','Ⅷ','  ','½',chr(0)]:
            self.assertEqual(strings.isalnum(c),c.isalnum())
            self.assertEqual(strings.isdecimal(c),c.isdecimal())
            self.assertEqual(strings.isdigit(c),c.isdigit())
            self.assertEqual(strings.islower(c),c.islower())
            self.assertEqual(strings.isnumeric(c),c.isnumeric())
            self.assertEqual(strings.isprintable(c),c.isprintable())
            self.assertEqual(strings.isspace(c),c.isspace())
            self.assertEqual(strings.isupper(c),c.isupper())
    
    def test_strings_case(self):
        """
        Tests the boolean string case functions.
        """
        for c in ['lower','UPPER','mIxEd cAsE']:
            self.assertEqual(strings.capitalize(c),c.capitalize())
            self.assertEqual(strings.swapcase(c),c.swapcase())
            self.assertEqual(strings.lower(c),c.lower())
            self.assertEqual(strings.upper(c),c.upper())
    
    def test_strings_format(self):
        """
        Tests the string formatting functions.
        """
        for c in ['lower','UPPER','mIxEd cAsE']:
            for w in [3,5,6,20,100]:
                for f in [' ',';','.']:
                    self.assertEqual(strings.center(c,w,f),c.center(w,f))
                    self.assertEqual(strings.ljust(c,w,f),c.ljust(w,f))
                    self.assertEqual(strings.rjust(c,w,f),c.rjust(w,f))
    
    def test_strings_replace(self):
        """
        Tests the string replacement functions.
        """
        for c in ['lower','UPPER','mIxEd cAsE']:
            for p in [('e','a'),('E','a'),('x','y'),('er','owy')]:
                self.assertEqual(strings.replace_str(c,*p),c.replace(*p))
                
        for c in ['   a','b     ','   a   b','b  a  ','   a   ','  a  b  ']:
            self.assertEqual(strings.strip(c),c.strip())
            self.assertEqual(strings.lstrip(c),c.lstrip())
            self.assertEqual(strings.rstrip(c),c.rstrip())
    
    def test_strings_search(self):
        """
        Tests the string search functions.
        """
        for w in ['dog','cat','apple','Log cabin','log cabin']:
            for i in ['d','a','p','x','Lo','lo','in']:
                for p in [(None,None),(1,-1),(None,-3),(1,2),(2,None)]:
                    self.assertEqual(strings.count_str(w,i,*p),w.count(i,*p))
                    self.assertEqual(strings.endswith_str(w,i,*p),w.endswith(i,*p))
                    self.assertEqual(strings.startswith_str(w,i,*p),w.startswith(i,*p))
                    self.assertEqual(strings.find_str(w,i,*p),w.find(i,*p))
                    self.assertEqual(strings.rfind_str(w,i,*p),w.rfind(i,*p))
        self.assertEqual(strings.index_str('pool','p'),'pool'.index('p'))
        self.assertEqual(strings.index_str('pool','o'),'pool'.index('o'))
        self.assertEqual(strings.index_str('pool','l'),'pool'.index('l'))
        self.assertEqual(strings.rindex_str('pool','p'),'pool'.rindex('p'))
        self.assertEqual(strings.rindex_str('pool','o'),'pool'.rindex('o'))
        self.assertEqual(strings.rindex_str('pool','l'),'pool'.rindex('l'))
        self.assertRaises(ValueError,strings.rindex_str,'pool','x')
        self.assertRaises(ValueError,strings.index_str,'pool','x')
    
    
    def test_strings_split(self):
        """
        Tests the split and join string functions.
        """
        text = 'This is some text, with punctation -- other others -- to make a really, long list.  Enjoy!'
        seps = [' ',',','--','.','!','a']
        for s in seps:
            self.assertEqual(strings.split(text,s),tuple(text.split(s)))
            self.assertEqual(strings.rsplit(text,s),tuple(text.rsplit(s)))
            self.assertEqual(strings.split(text,s,2),tuple(text.split(s,2)))
            self.assertEqual(strings.rsplit(text,s,2),tuple(text.rsplit(s,2)))
            self.assertEqual(strings.partition(text,s),tuple(text.partition(s)))
            self.assertEqual(strings.rpartition(text,s),tuple(text.rpartition(s)))
            splits = strings.split(text,s)
            self.assertEqual(strings.join(splits,s),text)
            self.assertEqual(strings.join(splits),text.replace(s,''))


if __name__=='__main__':
  unittest.main( )

