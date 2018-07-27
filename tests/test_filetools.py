"""
Unit test for file tools package

This is a tricky package to test as we need to read and write files. Those are all 
done in this directory.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
import unittest
import os.path
from introcs import filetools


class UrlToolsTest(unittest.TestCase):
    """
    Unit test for the file tools package
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
    
    def test_read_basic(self):
        """
        Tests the basic (non-package) read functions.
        """
        folder = os.path.split(__file__)[0]
        text = filetools.read_txt(os.path.join(folder,'files','colors.txt'))
        self.assertEqual(text[:2],'..')
        self.assertEqual(text[-3:],'hsv')
        json = filetools.read_json(os.path.join(folder,'files','weather.json'))
        self.assertEqual(json['2017-12-31T23:00:00-05:00']['temperature']['value'],-15)
        self.assertEqual(json['2017-12-31T23:00:00-05:00']['sky'][0]['type'],'broken')
        data = filetools.read_csv(os.path.join(folder,'files','fleet.csv'))
        self.assertEqual(data[0][0],'TAIL NO')
        self.assertEqual(data[5][5],'9/1/17')
        self.assertEqual(len(data),15)
        self.assertEqual(len(data[0]),7)
        
    def test_read_package(self):
        """
        Tests the package read function.
        """
        folder = os.path.split(__file__)[0]
        pckg = filetools.read_package(os.path.join(folder,'files'))
        self.assertEqual(pckg['COLORS'][:2],'..')
        self.assertEqual(pckg['COLORS'][-3:],'hsv')
        self.assertEqual(pckg['WEATHER']['2017-12-31T23:00:00-05:00']['temperature']['value'],-15)
        self.assertEqual(pckg['WEATHER']['2017-12-31T23:00:00-05:00']['sky'][0]['type'],'broken')
        self.assertEqual(pckg['FLEET'][0][0],'TAIL NO')
        self.assertEqual(pckg['FLEET'][5][5],'9/1/17')
        self.assertEqual(len(pckg['FLEET']),15)
        self.assertEqual(len(pckg['FLEET'][0]),7)
        self.assertEqual(pckg['RULES']['TEACHERS'][3][2],'Alan')
        
    def test_write(self):
        """
        Tests the write functions.
        """
        folder = os.path.split(__file__)[0]
        text = filetools.read_txt(os.path.join(folder,'files','colors.txt'))
        filetools.write_txt(text,os.path.join(folder,'files','colors-1.txt'))
        comp = filetools.read_txt(os.path.join(folder,'files','colors-1.txt'))
        self.assertEqual(text,comp)
        json = filetools.read_json(os.path.join(folder,'files','weather.json'))
        filetools.write_json(json,os.path.join(folder,'files','weather-1.json'))
        comp = filetools.read_json(os.path.join(folder,'files','weather-1.json'))
        self.assertEqual(json,comp)
        data = filetools.read_csv(os.path.join(folder,'files','fleet.csv'))
        filetools.write_csv(data,os.path.join(folder,'files','fleet-1.csv'))
        comp = filetools.read_csv(os.path.join(folder,'files','fleet-1.csv'))
        self.assertEqual(data,comp)


if __name__=='__main__':
  unittest.main( )

