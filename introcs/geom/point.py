"""
Classes for representing points.

Points have position, but they do not have magnitude or direction.  Use the vector classes
if you want direction.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
from .tuple import Tuple2, Tuple3
import math

class Point2(Tuple2):
    """
    An instance is a point in 2D space.
    
    This class is a subclass of :class:``Tuple2`` and inherits all of its attributes and 
    methods.
    
    :ivar x: The x-coordinate
    :vartype x: ``float``
    
    :ivar y: The y-coordinate
    :vartype y: ``float``
    """
    
    # BUILT_IN METHODS
    def __init__(self, x=0, y=0):
        """
        Creates a new Point2 value (x,y).
        
        All values are 0.0 by default.
        
        :return: a new Point2 value (x,y).
        
        :param x: initial x value
        :type x:  ``int`` or ``float``
            
        :param y: initial y value
        :type y:  ``int`` or ``float``
        """
        super().__init__(x,y)
    
    def __add__(self, other):
        """
        Performs a context dependent addition of this point and ``other``.
        
        If ``other`` is a point, the result is the vector from this position to ``other``
        (so ``other`` is the head).  If it is a vector, it is the point at the head of
        the vector when it is anchored at this point.
        
        :param other: object to add
        :type other:  ``Point2`` or ``Vector2``
        
        :return: the sum of this object and ``other``.
        :rtype:  ``Point2`` or ``Vector2``
        """
        from .vector import Vector2
        if isinstance(other,Point2):
            result = self.toVector()
        elif isinstance(other,Vector2):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x += other.x
        result.y += other.y
        return result
    
    def __sub__(self, tail):
        """
        Performs a context dependent subtraction of this point and ``other``.
        
        If ``other`` is a point, the result is the vector from ``other`` to this position
        (so ``other`` is the tail).  If it is a vector, it is the point at the tail of
        the vector whose head is at this point.
        
        :param other: object to subtract
        :type other:  ``Point2`` or ``Vector2``
        
        :return: the difference of this object and ``other``.
        :rtype:  ``Point2`` or ``Vector2``
        """
        from .vector import Vector2
        if isinstance(other,Point2):
            result = self.toVector()
        elif isinstance(other,Vector2):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x += other.x
        result.y -= other.y
        return result
    
    # PUBLIC METHODS
    def toVector(self):
        """
        :return: The ``Vector2`` object equivalent to this point
        :rtype:  ``Vector2``
        """
        from .vector import Vector2
        return Vector2(self.x,self.y)
    
    def midpoint(self,other):
        """
        Computes the midpoint between self and ``other``.
        
        This method treats ``self`` and ``other`` as a line segment, so they must both
        be points.
        
        :param other: the other end of the line segment
        :type other:  ``type(self)``
        
        :return: the midpoint between this point and ``other``
        :rtype:  ``type(self)``
        """
        return self.interpolant(other,0.5)
    
    def distance(self, other):
        """
        Computes the Euclidean between two points
        
        :param other: value to compare against
        :type other:  ``Point2``
        
        :return: the Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point2)), "%s is not a point" % repr(tail)
        return math.sqrt((self.x-other.x)*(self.x-other.x)+
                         (self.y-other.y)*(self.y-other.y))
    
    def distance2(self, other):
        """
        Computes the squared Euclidean between two points
        
        This method is slightly faster than :meth:`distance`.
        
        :param other: value to compare against
        :type other:  ``Point2``
        
        :return: the squared Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point2)), "%s is not a point" % repr(tail)
        return (self.x-other.x)*(self.x-other.x)+(self.y-other.y)*(self.y-other.y)


# #mark -
class Point3(Tuple3):
    """
    An instance is a point in 3D space.
    
    This class is a subclass of :class:``Tuple2`` and inherits all of its attributes and 
    methods.
    
    :ivar x: The x-coordinate
    :vartype x: ``float``
    
    :ivar y: The y-coordinate
    :vartype y: ``float``
    
    :ivar z: The z-coordinate
    :vartype z: ``float``
    """
    
    # BUILT_IN METHODS
    def __init__(self, x=0, y=0, z=0):
        """
        Creates a new Point3 value (x,y,z).
        
        All values are 0.0 by default.
        
        :return: a new Point3 value (x,y,z).
        
        :param x: initial x value
        :type x:  ``int`` or ``float``
        
        :param y: initial y value
        :type y:  ``int`` or ``float``
        
        :param z: initial z value
        :type z:  ``int`` or ``float``
        """
        super().__init__(x,y,z)
    
    def __add__(self, other):
        """
        Performs a context dependent addition of this point and other.
        
        If ``other`` is a point, the result is the vector from this position to ``other``
        (so ``other`` is the head).  If it is a vector, it is the point at the head of
        the vector when it is anchored at this point.
        
        :param other: object to add
        :type other:  ``Point2`` or ``Vector2``
        
        :return: the sum of this object and ``other``.
        :rtype:  ``Point2`` or ``Vector2``
        """
        from .vector import Vector3
        if isinstance(other,Point3):
            result = self.toVector()
        elif isinstance(other,Vector2):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x += other.x
        result.y += other.y
        result.z += other.z
        return result
    
    def __sub__(self, tail):
        """
        Performs a context dependent subtraction of this point and other.
        
        If ``other`` is a point, the result is the vector from ``other`` to this position
        (so ``other`` is the tail).  If it is a vector, it is the point at the tail of
        the vector whose head is at this point.
        
        :param other: object to subtract
        :type other:  ``Point3`` or ``Vector3``
        
        :return: the difference of this object and ``other``.
        :rtype:  ``Point3`` or ``Vector3``
        """
        from .vector import Vector3
        if isinstance(other,Point2):
            result = self.toVector()
        elif isinstance(other,Vector3):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x -= other.x
        result.y -= other.y
        result.z -= other.z
        return result
    
    # PUBLIC METHODS
    def toVector(self):
        """
        :return: The ``Vector3`` object equivalent to this point
        :rtype:  ``Vector3``
        """
        from .vector import Vector3
        return Vector3(self.x,self.y,self.z)
    
    def midpoint(self,other):
        """
        Computes the midpoint between self and ``other``.
        
        This method treats ``self`` and ``other`` as a line segment, so they must both
        be points.
        
        :param other: the other end of the line segment
        :type other:  ``type(self)``
        
        :return: the midpoint between this point and ``other``
        :rtype:  ``type(self)``
        """
        return self.interpolant(other,0.5)
    
    def distance(self, other):
        """
        Computes the Euclidean between two points
        
        :param other: value to compare against
        :type other:  ``Point3``
        
        :return: the Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point3)), "%s is not a point" % repr(other)
        return math.sqrt((self.x-other.x)*(self.x-other.x)+
                         (self.y-other.y)*(self.y-other.y)+
                         (self.z-other.z)*(self.z-other.z))
    
    def distance2(self, other):
        """
        Computes the squared Euclidean between two points
        
        This method is slightly faster than :meth:`distance`.
        
        :param other: value to compare against
        :type other:  ``Point3``
        
        :return: the squared Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point3)), "%s is not a point" % repr(other)
        return (self.x-other.x)*(self.x-other.x)+(self.y-other.y)*(self.y-other.y)+(self.z-other.z)*(self.z-other.z)


# Make 3-dimensions the default
Point = Point3
