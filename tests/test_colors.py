"""
Unit test for color package

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
import unittest
import numpy
from introcs import colors


class ColorTest(unittest.TestCase):
    """
    Unit test for the color package
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
    
    def test_rgb_basics(self):
        """
        Tests the initialization and methods of the RGB type.
        """
        #print('Testing rgb basics')
        color = colors.RGB(255,128,64)
        self.assertEqual(color.red,   255)
        self.assertEqual(color.green, 128)
        self.assertEqual(color.blue,  64)
        self.assertEqual(color.alpha, 255)
        self.assertEqual(str(color),'(255,128,64,255)')
        self.assertEqual(repr(color),'(red=255,green=128,blue=64,alpha=255)')
        self.assertClose(color.glColor(),[1.0, 0.501961, 0.250980, 1.0])
        self.assertEqual(color.rgba(),(255, 128, 64, 255))
        self.assertEqual(color.webColor(),'#ff8040')
        other = colors.RGB(255,128,64)
        self.assertEqual(color,other)
        self.assertIsNot(color,other)
        
        color = colors.RGB(64,255,128,32)
        self.assertEqual(color.red,   64)
        self.assertEqual(color.green, 255)
        self.assertEqual(color.blue,  128)
        self.assertEqual(color.alpha, 32)
        self.assertEqual(str(color),'(64,255,128,32)')
        self.assertEqual(repr(color),'(red=64,green=255,blue=128,alpha=32)')
        self.assertClose(color.glColor(),[0.250980, 1.0, 0.501961, 0.125490])
        self.assertEqual(color.rgba(),(64, 255, 128, 32))
        self.assertEqual(color.webColor(),'#40ff80')
        
        color.red = 32
        self.assertEqual(color.red,   32)
        color.green = 64
        self.assertEqual(color.green, 64)
        color.blue = 96
        self.assertEqual(color.blue,  96)
        color.alpha = 128
        self.assertEqual(color.alpha, 128)
    
    def test_rgb_asserts(self):
        """
        Tests the precondition enforcement of the RGB type.
        """
        self.assertRaises(AssertionError,colors.RGB,302,  128,  64)
        self.assertRaises(AssertionError,colors.RGB,-1,   128,  64)
        self.assertRaises(AssertionError,colors.RGB,128.5,128,  64)
        self.assertRaises(AssertionError,colors.RGB,'255',128,  64)
        self.assertRaises(AssertionError,colors.RGB,255,  302,  64)
        self.assertRaises(AssertionError,colors.RGB,255,   -1,  64)
        self.assertRaises(AssertionError,colors.RGB,255,  128.5,64)
        self.assertRaises(AssertionError,colors.RGB,255,  '128',64)
        self.assertRaises(AssertionError,colors.RGB,255,  128,  302)
        self.assertRaises(AssertionError,colors.RGB,255,  128,   -1)
        self.assertRaises(AssertionError,colors.RGB,255,  128,  '64')
        self.assertRaises(AssertionError,colors.RGB,255,  128,  64.5)
        self.assertRaises(AssertionError,colors.RGB,255,  128,  64, 302)
        self.assertRaises(AssertionError,colors.RGB,255,  128,  64, -1)
        self.assertRaises(AssertionError,colors.RGB,255,  128,  64, 128.5)
        self.assertRaises(AssertionError,colors.RGB,255,  128,  64, '255')
        
        color = colors.RGB(255,255,255)
        self.assertRaises(AssertionError,colors.RGB.red.__set__,color,302)
        self.assertRaises(AssertionError,colors.RGB.red.__set__,color,-1)
        self.assertRaises(AssertionError,colors.RGB.red.__set__,color,128.5)
        self.assertRaises(AssertionError,colors.RGB.red.__set__,color,'128')
        self.assertRaises(AssertionError,colors.RGB.green.__set__,color,302)
        self.assertRaises(AssertionError,colors.RGB.green.__set__,color,-1)
        self.assertRaises(AssertionError,colors.RGB.green.__set__,color,128.5)
        self.assertRaises(AssertionError,colors.RGB.green.__set__,color,'128')
        self.assertRaises(AssertionError,colors.RGB.blue.__set__,color,302)
        self.assertRaises(AssertionError,colors.RGB.blue.__set__,color,-1)
        self.assertRaises(AssertionError,colors.RGB.blue.__set__,color,128.5)
        self.assertRaises(AssertionError,colors.RGB.blue.__set__,color,'128')
        self.assertRaises(AssertionError,colors.RGB.alpha.__set__,color,302)
        self.assertRaises(AssertionError,colors.RGB.alpha.__set__,color,-1)
        self.assertRaises(AssertionError,colors.RGB.alpha.__set__,color,128.5)
        self.assertRaises(AssertionError,colors.RGB.alpha.__set__,color,'128')
    
    def test_rgb_statics(self):
        """
        Tests the static constructors of the RGB type.
        """
        color = colors.RGB.CreateName('cornflower blue')
        self.assertEqual(color.red,   100)
        self.assertEqual(color.green, 149)
        self.assertEqual(color.blue,  237)
        self.assertEqual(color.alpha, 255)
        
        color = colors.RGB.CreateName('white smoke')
        self.assertEqual(color.red,   245)
        self.assertEqual(color.green, 245)
        self.assertEqual(color.blue,  245)
        self.assertEqual(color.alpha, 255)
        
        color = colors.RGB.CreateName('firebrick')
        self.assertEqual(color.red,   178)
        self.assertEqual(color.green, 34)
        self.assertEqual(color.blue,  34)
        self.assertEqual(color.alpha, 255)
        
        self.assertRaises(AssertionError,colors.RGB.CreateName, 253)
        self.assertRaises(ValueError,colors.RGB.CreateName, 'fire truck')
        
        color = colors.RGB.CreateWebColor('#CC00CC')
        self.assertEqual(color.red,   204)
        self.assertEqual(color.green, 0)
        self.assertEqual(color.blue,  204)
        self.assertEqual(color.alpha, 255)
        
        color = colors.RGB.CreateWebColor('#FFFFFF')
        self.assertEqual(color.red,   255)
        self.assertEqual(color.green, 255)
        self.assertEqual(color.blue,  255)
        self.assertEqual(color.alpha, 255)
        
        color = colors.RGB.CreateWebColor('#000000')
        self.assertEqual(color.red,   0)
        self.assertEqual(color.green, 0)
        self.assertEqual(color.blue,  0)
        self.assertEqual(color.alpha, 255)
        
        self.assertRaises(AssertionError,colors.RGB.CreateWebColor, 253)
        self.assertRaises(AssertionError,colors.RGB.CreateWebColor, 'bob')
        self.assertRaises(AssertionError,colors.RGB.CreateWebColor, '#ff')
        self.assertRaises(AssertionError,colors.RGB.CreateWebColor, '#ffffffff')
        self.assertRaises(AssertionError,colors.RGB.CreateWebColor, '#ffxyzw')
    
    def test_cmyk_basics(self):
        """
        Tests the initialization and methods of the CMYK type.
        """
        color = colors.CMYK(99,50,25,75.3)
        self.assertEqual(color.cyan,    99)
        self.assertEqual(color.magenta, 50)
        self.assertEqual(color.yellow,  25)
        self.assertEqual(color.black,   75.3)
        self.assertEqual(str(color),'(99.0,50.0,25.0,75.3)')
        self.assertEqual(repr(color),'(cyan=99.0,magenta=50.0,yellow=25.0,black=75.3)')
        other = colors.CMYK(99,50,25,75.3)
        self.assertEqual(color,other)
        self.assertIsNot(color,other)
        
        color = colors.CMYK(0.125,1.25,12.5,1)
        self.assertEqual(color.cyan,    0.125)
        self.assertEqual(color.magenta, 1.25)
        self.assertEqual(color.yellow,  12.5)
        self.assertEqual(color.black,   1.0)
        self.assertEqual(str(color),'(0.125,1.25,12.5,1.0)')
        self.assertEqual(repr(color),'(cyan=0.125,magenta=1.25,yellow=12.5,black=1.0)')
        
        color.cyan = 15.5
        self.assertEqual(color.cyan,    15.5)
        color.magenta = 25.5
        self.assertEqual(color.magenta, 25.5)
        color.yellow = 35.5
        self.assertEqual(color.yellow,  35.5)
        color.black = 45.5
        self.assertEqual(color.black,   45.5)

    def test_cmyk_asserts(self):
        """
        Tests the precondition enforcement of the CMYK type.
        """
        self.assertRaises(AssertionError,colors.CMYK,   -1, 50, 50, 50)
        self.assertRaises(AssertionError,colors.CMYK,  101, 50, 50, 50)
        self.assertRaises(AssertionError,colors.CMYK, '50', 50, 50, 50)
        self.assertRaises(AssertionError,colors.CMYK,   -1, 50, 50, 50)
        self.assertRaises(AssertionError,colors.CMYK, 50,   -1, 50, 50)
        self.assertRaises(AssertionError,colors.CMYK, 50,  101, 50, 50)
        self.assertRaises(AssertionError,colors.CMYK, 50, '50', 50, 50)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50,   -1, 50)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50,   -1, 50)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50,  101, 50)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50, '50', 50)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50, 50,   -1)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50, 50,   -1)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50, 50,  101)
        self.assertRaises(AssertionError,colors.CMYK, 50, 50, 50, '50')
        
        color = colors.CMYK(50,50,50,50)
        self.assertRaises(AssertionError,colors.CMYK.cyan.__set__,color, 101)
        self.assertRaises(AssertionError,colors.CMYK.cyan.__set__,color,  -1)
        self.assertRaises(AssertionError,colors.CMYK.cyan.__set__,color,'50')
        self.assertRaises(AssertionError,colors.CMYK.magenta.__set__,color, 101)
        self.assertRaises(AssertionError,colors.CMYK.magenta.__set__,color,  -1)
        self.assertRaises(AssertionError,colors.CMYK.magenta.__set__,color,'50')
        self.assertRaises(AssertionError,colors.CMYK.yellow.__set__,color, 101)
        self.assertRaises(AssertionError,colors.CMYK.yellow.__set__,color,  -1)
        self.assertRaises(AssertionError,colors.CMYK.yellow.__set__,color,'50')
        self.assertRaises(AssertionError,colors.CMYK.black.__set__,color, 101)
        self.assertRaises(AssertionError,colors.CMYK.black.__set__,color,  -1)
        self.assertRaises(AssertionError,colors.CMYK.black.__set__,color,'50')
    
    def test_hsv_basics(self):
        """
        Tests the initialization and methods of the HSV type.
        """
        color = colors.HSV(180,0.5,0.5)
        self.assertEqual(color.hue,        180)
        self.assertEqual(color.saturation, 0.5)
        self.assertEqual(color.value,      0.5)
        self.assertEqual(str(color),'(180.0,0.5,0.5)')
        self.assertEqual(repr(color),'(hue=180.0,saturation=0.5,value=0.5)')
        self.assertClose(color.glColor(),[0.25, 0.5, 0.5, 1.0])
        self.assertEqual(color.rgba(),(64, 128, 128, 255))
        self.assertEqual(color.webColor(),'#408080')
        other = colors.HSV(180,0.5,0.5)
        self.assertEqual(color,other)
        self.assertIsNot(color,other)
        
        color = colors.HSV(275,0.0,1.0)
        self.assertEqual(color.hue,        275)
        self.assertEqual(color.saturation, 0.0)
        self.assertEqual(color.value,      1.0)
        self.assertEqual(str(color),'(275.0,0.0,1.0)')
        self.assertEqual(repr(color),'(hue=275.0,saturation=0.0,value=1.0)')
        self.assertClose(color.glColor(),[1.0, 1.0, 1.0, 1.0])
        self.assertEqual(color.rgba(),(255, 255, 255, 255))
        self.assertEqual(color.webColor(),'#ffffff')
        
        color = colors.HSV(35.5,1.0,0.0)
        self.assertEqual(color.hue,         35.5)
        self.assertEqual(color.saturation, 1.0)
        self.assertEqual(color.value,      0.0)
        self.assertEqual(str(color),'(35.5,1.0,0.0)')
        self.assertEqual(repr(color),'(hue=35.5,saturation=1.0,value=0.0)')
        self.assertClose(color.glColor(),[0.0, 0.0, 0.0, 1.0])
        self.assertEqual(color.rgba(),(0, 0, 0, 255))
        self.assertEqual(color.webColor(),'#000000')
        
        color = colors.HSV(135,1.0,1.0)
        self.assertEqual(color.hue,        135)
        self.assertEqual(color.saturation, 1.0)
        self.assertEqual(color.value,      1.0)
        self.assertEqual(str(color),'(135.0,1.0,1.0)')
        self.assertEqual(repr(color),'(hue=135.0,saturation=1.0,value=1.0)')
        self.assertClose(color.glColor(),[0.0, 1.0, 0.25, 1.0])
        self.assertEqual(color.rgba(),(0, 255, 64, 255))
        self.assertEqual(color.webColor(),'#00ff40')
        
        color.hue = 32
        self.assertEqual(color.hue,   32)
        color.saturation = 0.5
        self.assertEqual(color.saturation, 0.5)
        color.value = 0.2
        self.assertEqual(color.value,  0.2)
    
    def test_hsv_asserts(self):
        """
        Tests the precondition enforcement of the HSV type.
        """
        self.assertRaises(AssertionError,colors.HSV, 400, 0.5, 0.5)
        self.assertRaises(AssertionError,colors.HSV, 360, 0.5, 0.5)
        self.assertRaises(AssertionError,colors.HSV,  -1, 0.5, 0.5)
        self.assertRaises(AssertionError,colors.HSV,'35', 0.5, 0.5)
        self.assertRaises(AssertionError,colors.HSV, 350,  -1, 0.5)
        self.assertRaises(AssertionError,colors.HSV, 350, 1.5, 0.5)
        self.assertRaises(AssertionError,colors.HSV, 350, 0.5, '1')
        self.assertRaises(AssertionError,colors.HSV, 350, 0.5,  -1)
        self.assertRaises(AssertionError,colors.HSV, 350, 0.5, 1.5)
        
        color = colors.HSV(180,0.5,0.5)
        self.assertRaises(AssertionError,colors.HSV.hue.__set__,color,  400)
        self.assertRaises(AssertionError,colors.HSV.hue.__set__,color,   -1)
        self.assertRaises(AssertionError,colors.HSV.hue.__set__,color,  360)
        self.assertRaises(AssertionError,colors.HSV.hue.__set__,color, '35')
        self.assertRaises(AssertionError,colors.HSV.saturation.__set__,color,  -1)
        self.assertRaises(AssertionError,colors.HSV.saturation.__set__,color, 1.5)
        self.assertRaises(AssertionError,colors.HSV.saturation.__set__,color, '1')
        self.assertRaises(AssertionError,colors.HSV.value.__set__,color,  -1)
        self.assertRaises(AssertionError,colors.HSV.value.__set__,color, 1.5)
        self.assertRaises(AssertionError,colors.HSV.value.__set__,color, '1')


if __name__=='__main__':
  unittest.main( )

