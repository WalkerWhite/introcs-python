"""
Unit test for geometry package

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
import unittest
import numpy
from introcs import geom


class GeomTest(unittest.TestCase):
    """
    Unit test for the geometry package
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
    
    def test_tuple2_basics(self):
        """
        Tests the initialization and basic methods of the Tuple2 type.
        """
        first = geom.tuple.Tuple2(1.5,-2.5)
        self.assertEqual(first.x,  1.5)
        self.assertEqual(first.y, -2.5)
        self.assertEqual(str(first),'(1.5,-2.5)')
        self.assertEqual(repr(first),'%s%s' % (str(first.__class__),str(first)))
        self.assertTrue(first)
        self.assertEqual(first,first.copy())
        self.assertIsNot(first,first.copy())
        self.assertEqual(first.list(),[1.5,-2.5])
        
        copyd = first.copy()
        copyd.clamp(-5,5)
        self.assertEqual(first,copyd)
        copyd.clamp(-1,5)
        self.assertNotEqual(first,copyd)
        self.assertEqual(copyd,geom.tuple.Tuple2(1.5,-1))
        copyd.clamp(-1,1)
        self.assertEqual(copyd,geom.tuple.Tuple2(1,-1))
        
        secnd = geom.tuple.Tuple2(-1.5,2.5)
        self.assertEqual(secnd.x, -1.5)
        self.assertEqual(secnd.y,  2.5)
        self.assertEqual(str(secnd),'(-1.5,2.5)')
        self.assertEqual(repr(secnd),'%s%s' % (str(secnd.__class__),str(secnd)))
        self.assertTrue(secnd)
        self.assertNotEqual(first,secnd)
        self.assertGreater(first,secnd)
        self.assertFalse(first.under(secnd))
        self.assertFalse(first.over(secnd))
        
        third = geom.tuple.Tuple2(1.5,2.5)
        self.assertEqual(third.x,  1.5)
        self.assertEqual(third.y,  2.5)
        self.assertEqual(str(third),'(1.5,2.5)')
        self.assertEqual(repr(third),'%s%s' % (str(third.__class__),str(third)))
        self.assertTrue(third)
        self.assertNotEqual(first,third)
        self.assertLess(first,third)
        self.assertTrue(first.under(third))
        self.assertTrue(third.over(first))
        
        forth = geom.tuple.Tuple2(0.0,0.0)
        self.assertFalse(forth)
        
        forth.x = 1.5
        self.assertEqual(forth.x, 1.5)
        forth.y = -2.5
        self.assertEqual(forth.y, -2.5)
        self.assertEqual(first,forth)
        self.assertIsNot(first,forth)
    
    def test_tuple2_asserts(self):
        """
        Tests the precondition enforcement of the Tuple2 type.
        """
        self.assertRaises(AssertionError,geom.tuple.Tuple2, '1',   1)
        self.assertRaises(AssertionError,geom.tuple.Tuple2,   1, "1")
        
        item = geom.tuple.Tuple2(0.0,0.0)
        self.assertRaises(AssertionError,geom.tuple.Tuple2.x.__set__,item,'1')
        self.assertRaises(AssertionError,geom.tuple.Tuple2.y.__set__,item,'1')
    
    def test_tuple2_arithmetic(self):
        """
        Tests the arithmetic methods of the Tuple2 type.
        """
        first = geom.tuple.Tuple2(1.5,-2.5)
        secnd = geom.tuple.Tuple2(-1.5,1.0)
        self.assertEqual(first+secnd,geom.tuple.Tuple2(0.0,-1.5))
        self.assertEqual(first-secnd,geom.tuple.Tuple2(3.0,-3.5))
        self.assertEqual(2*first,geom.tuple.Tuple2(3.0,-5.0))
        self.assertEqual(first*2,geom.tuple.Tuple2(3.0,-5.0))
        self.assertEqual(first*secnd,geom.tuple.Tuple2(-2.25,-2.5))
        self.assertEqual(2*(first/2),first)
        self.assertEqual(first/first,geom.tuple.Tuple2(1.0,1.0))
        self.assertEqual(1/geom.tuple.Tuple2(4.0,2.0),geom.tuple.Tuple2(0.25,0.5))
        
        third = first
        third += secnd
        self.assertEqual(third,geom.tuple.Tuple2(0.0,-1.5))
        third -= secnd
        self.assertEqual(third,first)
        third *= 2
        self.assertEqual(third,geom.tuple.Tuple2(3.0,-5.0))
        third /= 2
        self.assertEqual(third,first)
        third *= secnd
        self.assertEqual(third,geom.tuple.Tuple2(-2.25,-2.5))
        third /= secnd
        self.assertEqual(third,first)
        
        first = geom.tuple.Tuple2(1.0,3.0)
        secnd = geom.tuple.Tuple2(2.0,1.0)
        self.assertEqual(first.interpolant(secnd,0.5),geom.tuple.Tuple2(1.5,2.0))
        first.interpolate(secnd,0.5)
        self.assertEqual(first,geom.tuple.Tuple2(1.5,2.0))
    
    def test_tuple3_basics(self):
        """
        Tests the initialization and basic methods of the Tuple3 type.
        """
        first = geom.tuple.Tuple3(1.5,-2.5,3.5)
        self.assertEqual(first.x,  1.5)
        self.assertEqual(first.y, -2.5)
        self.assertEqual(first.z,  3.5)
        self.assertEqual(str(first),'(1.5,-2.5,3.5)')
        self.assertEqual(repr(first),'%s%s' % (str(first.__class__),str(first)))
        self.assertTrue(first)
        self.assertEqual(first,first.copy())
        self.assertIsNot(first,first.copy())
        self.assertEqual(first.list(),[1.5,-2.5,3.5])
        
        copyd = first.copy()
        copyd.clamp(-5,5)
        self.assertEqual(first,copyd)
        copyd.clamp(-1,5)
        self.assertNotEqual(first,copyd)
        self.assertEqual(copyd,geom.tuple.Tuple3(1.5,-1,3.5))
        copyd.clamp(-1,2)
        self.assertEqual(copyd,geom.tuple.Tuple3(1.5,-1,2))
        copyd.clamp(-1,1)
        self.assertEqual(copyd,geom.tuple.Tuple3(1,-1,1))
        
        secnd = geom.tuple.Tuple3(-1.5,2.5,-3)
        self.assertEqual(secnd.x, -1.5)
        self.assertEqual(secnd.y,  2.5)
        self.assertEqual(secnd.z,   -3)
        self.assertEqual(str(secnd),'(-1.5,2.5,-3.0)')
        self.assertEqual(repr(secnd),'%s%s' % (str(secnd.__class__),str(secnd)))
        self.assertTrue(secnd)
        self.assertNotEqual(first,secnd)
        self.assertGreater(first,secnd)
        self.assertFalse(first.under(secnd))
        self.assertFalse(first.over(secnd))
        
        third = geom.tuple.Tuple3(1.5,2.5,4.0)
        self.assertEqual(third.x,  1.5)
        self.assertEqual(third.y,  2.5)
        self.assertEqual(third.z,  4.0)
        self.assertEqual(str(third),'(1.5,2.5,4.0)')
        self.assertEqual(repr(third),'%s%s' % (str(third.__class__),str(third)))
        self.assertTrue(third)
        self.assertNotEqual(first,third)
        self.assertLess(first,third)
        self.assertTrue(first.under(third))
        self.assertTrue(third.over(first))
        
        forth = geom.tuple.Tuple3(0,0,0)
        self.assertFalse(forth)
        
        forth.x = 1.5
        self.assertEqual(forth.x, 1.5)
        self.assertLess(first,forth)
        forth.y = -2.5
        self.assertEqual(forth.y, -2.5)
        self.assertGreater(first,forth)
        forth.z = 3.5
        self.assertEqual(forth.z,  3.5)
        self.assertEqual(first,forth)
        self.assertIsNot(first,forth)
    
    def test_tuple3_asserts(self):
        """
        Tests the precondition enforcement of the Tuple3 type.
        """
        self.assertRaises(AssertionError,geom.tuple.Tuple3, '1',   1,   1)
        self.assertRaises(AssertionError,geom.tuple.Tuple3,   1, '1',   1)
        self.assertRaises(AssertionError,geom.tuple.Tuple3,   1,   1, '1')
        
        item = geom.tuple.Tuple3(0.0,0.0)
        self.assertRaises(AssertionError,geom.tuple.Tuple3.x.__set__,item,'1')
        self.assertRaises(AssertionError,geom.tuple.Tuple3.y.__set__,item,'1')
        self.assertRaises(AssertionError,geom.tuple.Tuple3.z.__set__,item,'1')
    
    def test_tuple3_arithmetic(self):
        """
        Tests the arithmetic methods of the Tuple3 type.
        """
        first = geom.tuple.Tuple3(1.5,-2.5,3.0)
        secnd = geom.tuple.Tuple3(-1.5,1.0,2.0)
        self.assertEqual(first+secnd,geom.tuple.Tuple3(0.0,-1.5,5.0))
        self.assertEqual(first-secnd,geom.tuple.Tuple3(3.0,-3.5,1.0))
        self.assertEqual(2*first,geom.tuple.Tuple3(3.0,-5.0,6.0))
        self.assertEqual(first*2,geom.tuple.Tuple3(3.0,-5.0,6.0))
        self.assertEqual(first*secnd,geom.tuple.Tuple3(-2.25,-2.5,6.0))
        self.assertEqual(2*(first/2),first)
        self.assertEqual(first/first,geom.tuple.Tuple3(1.0,1.0,1.0))
        self.assertEqual(1/geom.tuple.Tuple3(4.0,2.0,8.0),geom.tuple.Tuple3(0.25,0.5,0.125))
        
        third = first
        third += secnd
        self.assertEqual(third,geom.tuple.Tuple3(0.0,-1.5,5.0))
        third -= secnd
        self.assertEqual(third,first)
        third *= 2
        self.assertEqual(third,geom.tuple.Tuple3(3.0,-5.0,6.0))
        third /= 2
        self.assertEqual(third,first)
        third *= secnd
        self.assertEqual(third,geom.tuple.Tuple3(-2.25,-2.5,6.0))
        third /= secnd
        self.assertEqual(third,first)
        
        first = geom.tuple.Tuple3(1.0,3.0,2.0)
        secnd = geom.tuple.Tuple3(2.0,1.0,-2.0)
        self.assertEqual(first.interpolant(secnd,0.5),geom.tuple.Tuple3(1.5,2.0,0.0))
        first.interpolate(secnd,0.5)
        self.assertEqual(first,geom.tuple.Tuple3(1.5,2.0,0.0))
    
    def test_point2(self):
        """
        Tests the initialization and basic methods of the Point2 type.
        """
        first = geom.Point2(1.5,-2.5)
        secnd = geom.Point2(-1.5,1.0)
        third = geom.Vector2(-1.5,1.0)
        forth = geom.tuple.Tuple2(-1.5,1.0)
        self.assertEqual(first.x,  1.5)
        self.assertEqual(first.y, -2.5)
        self.assertEqual(type(first+secnd), geom.Vector2)
        self.assertEqual(type(first-secnd), geom.Vector2)
        self.assertEqual(type(first+third), geom.Point2)
        self.assertEqual(type(first-third), geom.Point2)
        self.assertRaises(AssertionError,first.__add__,forth)
        self.assertRaises(AssertionError,first.__sub__,forth)
        
        third = first.toVector()
        self.assertEqual(type(third), geom.Vector2)
        self.assertEqual(third, geom.Vector2(1.5,-2.5))
        self.assertEqual(first.midpoint(secnd),((first+secnd)/2).toPoint())
       
        self.assertAlmostEqual(first.distance2(secnd),21.25)
        self.assertAlmostEqual(first.distance(secnd),4.6097722)
    
    def test_point3(self):
        """
        Tests the initialization and basic methods of the Point3 type.
        """
        first = geom.Point3(1.5,-2.5,3.0)
        secnd = geom.Point3(-1.5,1.0,2.0)
        third = geom.Vector3(-1.5,1.0,2.0)
        forth = geom.tuple.Tuple3(-1.5,1.0,2.0)
        self.assertEqual(first.x,  1.5)
        self.assertEqual(first.y, -2.5)
        self.assertEqual(first.z,  3.0)
        self.assertEqual(type(first+secnd), geom.Vector3)
        self.assertEqual(type(first-secnd), geom.Vector3)
        self.assertEqual(type(first+third), geom.Point3)
        self.assertEqual(type(first-third), geom.Point3)
        self.assertRaises(AssertionError,first.__add__,forth)
        self.assertRaises(AssertionError,first.__sub__,forth)
        
        third = first.toVector()
        self.assertEqual(type(third), geom.Vector3)
        self.assertEqual(third, geom.Vector3(1.5,-2.5,3.0))
        self.assertEqual(first.midpoint(secnd),((first+secnd)/2).toPoint())
       
        self.assertAlmostEqual(first.distance2(secnd),22.25)
        self.assertAlmostEqual(first.distance(secnd),4.7169906)
        
        fifth = geom.Point(0,0,0)
        self.assertEqual(first.__class__,fifth.__class__)
    
    def test_vector2_basics(self):
        """
        Tests the initialization and basic methods of the Vector2 type.
        """
        first = geom.Vector2(1.5,-2.5)
        secnd = geom.Vector2(-1.5,1.0)
        third = geom.Point2(-1.5,1.0)
        forth = geom.tuple.Tuple2(-1.5,1.0)
        self.assertEqual(first.x,  1.5)
        self.assertEqual(first.y, -2.5)
        self.assertEqual(type(first+secnd), geom.Vector2)
        self.assertEqual(type(first-secnd), geom.Vector2)
        self.assertEqual(type(first+third), geom.Point2)
        self.assertEqual(type(first-third), geom.Point2)
        self.assertRaises(AssertionError,first.__add__,forth)
        self.assertRaises(AssertionError,first.__sub__,forth)
        
        third = first.toPoint()
        self.assertEqual(type(third), geom.Point2)
        self.assertEqual(third, geom.Point2(1.5,-2.5))
       
        self.assertAlmostEqual(first.length2(),8.5)
        self.assertAlmostEqual(first.length(),2.9154759)
        self.assertFalse(first.isUnit())
        
        fifth = geom.Vector2(-0.7071068,0.7071068)
        self.assertTrue(fifth.isUnit())
    
    def test_vector2_linear(self):
        """
        Tests the linear algebra methods of the Vector2 type.
        """
        import math
        first = geom.Vector2(1.5,-2.5)
        secnd = geom.Vector2(0.5144958, -0.8574929)
        xaxis = geom.Vector2(1.0,0.0)
        yaxis = geom.Vector2(0.0,1.0)
        lines = xaxis+yaxis
        
        self.assertClose(first.normal().list(), secnd.list())
        third = first.copy()
        third.normalize()
        self.assertClose(third.list(), secnd.list())
        self.assertAlmostEqual(first.angle(secnd), 0)
        self.assertAlmostEqual(xaxis.angle(yaxis), math.pi/2)
        self.assertAlmostEqual(xaxis.angle(lines), math.pi/4)
        
        self.assertEqual(first.dot(first),first.length2())
        self.assertEqual(xaxis.rperp(),yaxis)
        self.assertEqual(xaxis.perp(),-yaxis)
        self.assertEqual(xaxis.cross(yaxis),1.0)
        self.assertEqual(xaxis.cross(xaxis),0.0)
        self.assertEqual(xaxis.cross(2*lines),2.0)
        
        self.assertEqual(xaxis.rotation(math.pi/4),lines.normal())
        self.assertEqual(xaxis.rotation(0),xaxis)
        self.assertEqual(xaxis.rotation(math.pi/2),yaxis)
        third = xaxis.copy()
        third.rotate(0)
        self.assertEqual(third,xaxis)
        third.rotate(math.pi/4)
        self.assertEqual(third,lines.normal())
        third.rotate(math.pi/4)
        self.assertEqual(third,yaxis)
        
        self.assertEqual(first.projection(xaxis),xaxis*first.x)
        self.assertEqual(first.projection(yaxis),yaxis*first.y)
        self.assertEqual(first.projection(first),first)
        third = first.copy(); third.project(xaxis)
        self.assertEqual(third,xaxis*first.x)
        third = first.copy(); third.project(yaxis)
        self.assertEqual(third,yaxis*first.y)
        third = first.copy(); third.project(first)
        self.assertEqual(third,first)
    
    def test_vector3_basics(self):
        """
        Tests the initialization and basic methods of the Vector3 type.
        """
        first = geom.Vector3(1.5,-2.5,3.0)
        secnd = geom.Vector3(-1.5,1.0,2.0)
        third = geom.Point3(-1.5,1.0,2.0)
        forth = geom.tuple.Tuple3(-1.5,1.0,2.0)
        self.assertEqual(first.x,  1.5)
        self.assertEqual(first.y, -2.5)
        self.assertEqual(first.z,  3.0)
        self.assertEqual(type(first+secnd), geom.Vector3)
        self.assertEqual(type(first-secnd), geom.Vector3)
        self.assertEqual(type(first+third), geom.Point3)
        self.assertEqual(type(first-third), geom.Point3)
        self.assertRaises(AssertionError,first.__add__,forth)
        self.assertRaises(AssertionError,first.__sub__,forth)
        
        third = first.toPoint()
        self.assertEqual(type(third), geom.Point3)
        self.assertEqual(third, geom.Point3(1.5,-2.5,3.0))
       
        self.assertAlmostEqual(first.length2(),17.5)
        self.assertAlmostEqual(first.length(),4.1833001)
        
        fifth = geom.Vector(0.5773503,-0.5773503,0.5773503)
        self.assertEqual(first.__class__,fifth.__class__)
        self.assertTrue(fifth.isUnit())
    
    def test_vector3_linear(self):
        """
        Tests the linear algebra methods of the Vector3 type.
        """
        import math
        first = geom.Vector3(1.5,-2.5,3.0)
        secnd = geom.Vector3(0.3585686, -0.5976143, 0.7171372)
        xaxis = geom.Vector3(1.0,0.0,0.0)
        yaxis = geom.Vector3(0.0,1.0,0.0)
        zaxis = geom.Vector3(0.0,0.0,1.0)
        lines = xaxis+yaxis
        
        self.assertClose(first.normal().list(), secnd.list())
        third = first.copy()
        third.normalize()
        self.assertClose(third.list(), secnd.list())
        self.assertAlmostEqual(first.angle(secnd), 0)
        self.assertAlmostEqual(xaxis.angle(zaxis), math.pi/2)
        self.assertAlmostEqual(xaxis.angle(lines), math.pi/4)
        
        self.assertEqual(first.dot(first),first.length2())
        self.assertEqual(xaxis.cross(yaxis),zaxis)
        self.assertEqual(lines.cross(yaxis-xaxis).normal(),zaxis)
        third = lines.copy()
        third.crossify(yaxis-xaxis)
        third.normalize()
        self.assertEqual(third,zaxis)
        
        self.assertEqual(first.projection(xaxis),xaxis*first.x)
        self.assertEqual(first.projection(yaxis),yaxis*first.y)
        self.assertEqual(first.projection(zaxis),zaxis*first.z)
        self.assertEqual(first.projection(first),first)
        third = first.copy(); third.project(xaxis)
        self.assertEqual(third,xaxis*first.x)
        third = first.copy(); third.project(yaxis)
        self.assertEqual(third,yaxis*first.y)
        third = first.copy(); third.project(zaxis)
        self.assertEqual(third,zaxis*first.z)
        third = first.copy(); third.project(first)
        self.assertEqual(third,first)
    
    def test_matrix_basics(self):
        """
        Tests the initialization and basic methods of the Matrix type.
        """
        import math
        first = geom.Matrix()
        self.assertEqual(str(first),'[[1.0, 0.0, 0.0, 0.0],\n [0.0, 1.0, 0.0, 0.0],\n [0.0, 0.0, 1.0, 0.0],\n [0.0, 0.0, 0.0, 1.0]]')
        self.assertEqual(repr(first),'%s%s' % (str(first.__class__),str(first)))
        secnd = first.copy()
        self.assertEqual(first,secnd)
        self.assertIsNot(first,secnd)
        
        secnd = geom.Matrix.CreateTranslation(2,3,4.5)
        self.assertClose(eval(str(secnd)),[[1, 0, 0, 2], [0, 1, 0, 3], [0, 0, 1, 4.5], [0, 0, 0, 1]])
        third = geom.Matrix.CreateRotation(math.pi/4)
        self.assertClose(eval(str(third)),[[0.9999061, -0.0137074, 0, 0], [0.0137074, 0.9999061, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        third = geom.Matrix.CreateRotation(math.pi/4,x=1,y=0,z=0)
        self.assertClose(eval(str(third)),[[1, 0, 0, 0], [0.0, 0.99990606, -0.013707355, 0.0], [0.0, 0.013707355, 0.99990606, 0.0], [0, 0, 0, 1]])
        third = geom.Matrix.CreateRotation(math.pi/4,x=0,y=1,z=0)
        self.assertClose(eval(str(third)),[[0.99990606, 0.0, 0.013707355, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.013707355, 0.0, 0.99990606, 0.0], [0, 0, 0, 1]])
        forth = geom.Matrix.CreateScale(2,3,4)
        self.assertClose(eval(str(forth)),[[2, 0, 0, 0], [0, 3, 0, 0], [0, 0, 4, 0], [0, 0, 0, 1]])
        
        self.assertClose(eval(str(secnd.transpose())),[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [2, 3, 4.5, 1]])
        self.assertClose(eval(str(forth.transpose())),[[2, 0, 0, 0], [0, 3, 0, 0], [0, 0, 4, 0], [0, 0, 0, 1]])
        
        fifth = first.copy(); fifth.translate(2,3,4.5)
        self.assertEqual(fifth,secnd)
        fifth = first.copy(); fifth.rotate(math.pi/4,x=0,y=1,z=0)
        self.assertEqual(fifth,third)
        fifth = first.copy(); fifth.scale(2,3,4)
        self.assertEqual(fifth,forth)
        
        self.assertEqual(secnd.inverse(),geom.Matrix.CreateTranslation(-2,-3,-4.5))
        self.assertEqual(third.inverse(),geom.Matrix.CreateRotation(-math.pi/4,x=0,y=1,z=0))
        self.assertEqual(forth.inverse(),geom.Matrix.CreateScale(1/2,1/3,1/4))
        
        fifth = secnd.copy(); fifth.invert()
        self.assertEqual(fifth,geom.Matrix.CreateTranslation(-2,-3,-4.5))
        fifth = third.copy(); fifth.invert()
        self.assertEqual(fifth,geom.Matrix.CreateRotation(-math.pi/4,x=0,y=1,z=0))
        fifth = forth.copy(); fifth.invert()
        self.assertEqual(fifth,geom.Matrix.CreateScale(1/2,1/3,1/4))
        
        fifth = secnd.copy(); fifth.rotate(math.pi/4,x=0,y=1,z=0)
        self.assertEqual(secnd*third,fifth)
        fifth.scale(2,3,4)
        self.assertEqual(secnd*third*forth,fifth)
    
    def test_matrix_inversion(self):
        """
        Tests the inversion methods of the Matrix type.
        """
        first = geom.Matrix()
        secnd = first.copy()
        self.assertEqual(first,secnd.transpose())
        secnd.transpost()
        self.assertEqual(first,secnd)
        self.assertEqual(first,secnd.inverse())
        secnd.invert()
        self.assertEqual(first,secnd)
        self.assertEqual(first,secnd.inverse())
        
        first = geom.Matrix.CreateScale(10,9,1/2)
        secnd = geom.Matrix.CreateScale(1/10,1/9,2)
        third = secnd.copy()
        self.assertEqual(secnd,third.transpose())
        third.transpost()
        self.assertEqual(secnd,third)
        secnd.invert()
        self.assertEqual(first,secnd)
        self.assertEqual(first,third.inverse())
        
        first = geom.Matrix.CreateRotation(35)
        secnd = geom.Matrix.CreateRotation(-35)
        third = secnd.copy()
        self.assertNotEqual(secnd,third.transpose())
        third.transpost()
        self.assertEqual(secnd,third.transpose())
        third.transpost()
        self.assertEqual(secnd,third)
        secnd.invert()
        self.assertEqual(first,secnd)
        self.assertEqual(first,third.inverse())
        
        first = geom.Matrix.CreateTranslation(14,16,2)
        secnd = geom.Matrix.CreateTranslation(-14,-16,-2)
        third = secnd.copy()
        self.assertNotEqual(secnd,third.transpose())
        third.transpost()
        self.assertEqual(secnd,third.transpose())
        third.transpost()
        self.assertEqual(secnd,third)
        secnd.invert()
        self.assertEqual(first,secnd)
        self.assertEqual(first,third.inverse())
        
        first = geom.Matrix.CreateScale(10,9,1/2)
        first.translate(14,16,-2)
        secnd = geom.Matrix.CreateTranslation(-14,-16,2)
        secnd.scale(1/10,1/9,2)
        third = secnd.copy()
        self.assertNotEqual(secnd,third.transpose())
        third.transpost()
        self.assertEqual(secnd,third.transpose())
        third.transpost()
        self.assertEqual(secnd,third)
        secnd.invert()
        self.assertEqual(first,secnd)
        self.assertEqual(first,third.inverse())
    
    def test_matrix_transforms(self):
        """
        Tests the transformation methods of the Matrix type.
        """
        import math
        first = geom.Matrix()
        secnd = geom.Matrix.CreateTranslation(2,3,4.5)
        third = geom.Matrix.CreateRotation(math.pi/4)
        forth = geom.Matrix.CreateScale(2,3,4)
        
        value = geom.Vector3(0,0,0)
        self.assertEqual(first.transform(value),value)
        self.assertEqual(value*first,value)
        self.assertEqual(secnd.transform(value),geom.Vector3(2,3,4.5))
        self.assertEqual(value*secnd,geom.Vector3(2,3,4.5))
        self.assertEqual(third.transform(value),value)
        self.assertEqual(value*third,value)
        self.assertEqual(forth.transform(value),value)
        self.assertEqual(value*forth,value)
        self.assertEqual(first.transform(value.toPoint()),value.toPoint())
        self.assertEqual(value.toPoint()*first,value.toPoint())
       
        value = geom.Vector3(1,2,3)
        self.assertEqual(first.transform(value),value)
        self.assertEqual(value*first,value)
        self.assertEqual(secnd.transform(value),geom.Vector3(3,5,7.5))
        self.assertEqual(value*secnd,secnd.transform(value))
        self.assertEqual(third.transform(value),geom.Vector3(0.9724914,2.0135195,3.0))
        self.assertEqual(value*third,third.transform(value))
        self.assertEqual(forth.transform(value),geom.Vector3(2,6,12))
        self.assertEqual(value*forth,forth.transform(value))
        
        fifth = secnd.copy(); fifth.scale(2,3,4)
        self.assertEqual(value*(secnd*forth),fifth.transform(value))
        self.assertEqual((value*secnd)*forth,fifth.transform(value))
        fifth = secnd.copy(); fifth.rotate(math.pi/4)
        self.assertEqual(value*(secnd*third),fifth.transform(value))
        self.assertEqual((value*secnd)*third,fifth.transform(value))
        fifth = forth.copy(); fifth.rotate(math.pi/4)
        self.assertEqual((value*forth)*third,fifth.transform(value))
        self.assertEqual(value*(forth*third),fifth.transform(value))
        fifth = third.copy(); fifth.translate(2,3,4.5)
        self.assertEqual((value*third)*secnd,fifth.transform(value))
        self.assertEqual(value*(third*secnd),fifth.transform(value))
        
        value = geom.Vector2(0,0)
        self.assertEqual(first.transform(value),value)
        self.assertEqual(value*first,value)
        self.assertEqual(secnd.transform(value),geom.Vector2(2,3))
        self.assertEqual(value*secnd,geom.Vector2(2,3))
        self.assertEqual(third.transform(value),value)
        self.assertEqual(value*third,value)
        self.assertEqual(forth.transform(value),value)
        self.assertEqual(value*forth,value)
        self.assertEqual(first.transform(value.toPoint()),value.toPoint())
        self.assertEqual(value.toPoint()*first,value.toPoint())
       
        value = geom.Vector2(1,2)
        self.assertEqual(first.transform(value),value)
        self.assertEqual(value*first,value)
        self.assertEqual(secnd.transform(value),geom.Vector2(3,5))
        self.assertEqual(value*secnd,secnd.transform(value))
        self.assertEqual(third.transform(value),geom.Vector2(0.9724914,2.0135195))
        self.assertEqual(value*third,third.transform(value))
        self.assertEqual(forth.transform(value),geom.Vector2(2,6))
        self.assertEqual(value*forth,forth.transform(value))
        
        fifth = secnd.copy(); fifth.scale(2,3,4)
        self.assertEqual(value*(secnd*forth),fifth.transform(value))
        self.assertEqual((value*secnd)*forth,fifth.transform(value))
        fifth = secnd.copy(); fifth.rotate(math.pi/4)
        self.assertEqual(value*(secnd*third),fifth.transform(value))
        self.assertEqual((value*secnd)*third,fifth.transform(value))
        fifth = forth.copy(); fifth.rotate(math.pi/4)
        self.assertEqual((value*forth)*third,fifth.transform(value))
        self.assertEqual(value*(forth*third),fifth.transform(value))
        fifth = third.copy(); fifth.translate(2,3,4.5)
        self.assertEqual((value*third)*secnd,fifth.transform(value))
        self.assertEqual(value*(third*secnd),fifth.transform(value))

if __name__=='__main__':
  unittest.main( )

