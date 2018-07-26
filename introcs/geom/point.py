"""
Classes for representing points.

Points have position, but they do not have magnitude or direction.  Use the vector classes
if you want direction.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
# The docs at the bottom are to hide inheritance from the documentation
from .tuple import Tuple2, Tuple3
import math

class Point2(Tuple2):
    """
    An instance is a point in 2D space.
    """
    
    # BUILT_IN METHODS
    def __init__(self, x=0, y=0):
        """
        All attribute values are 0.0 by default.
        
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
    
    def __sub__(self, other):
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
        
        result.x -= other.x
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
        :type other:  ``Point2``
        
        :return: the midpoint between this point and ``other``
        :rtype:  ``Point2``
        """
        return self.interpolant(other,0.5).toPoint()
    
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
    """
    
    # BUILT_IN METHODS
    def __init__(self, x=0, y=0, z=0):
        """
        All attribute values are 0.0 by default.
        
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
        elif isinstance(other,Vector3):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x += other.x
        result.y += other.y
        result.z += other.z
        return result
    
    def __sub__(self, other):
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
        if isinstance(other,Point3):
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
        :type other:  ``Point3``
        
        :return: the midpoint between this point and ``other``
        :rtype:  ``Point3``
        """
        return self.interpolant(other,0.5).toPoint()
    
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


# #mark -
# #mark Point2 docs
Point2.__eq__.__doc__ = """
    Compares this point with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.  Equivalence also requires type
    equivalence.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: True if ``self`` and ``other`` are equivalent
    :rtype:  ``bool``
    """

Point2.__ne__.__doc__ = """
    Compares this object with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: False if ``self`` and ``other`` are equivalent objects. 
    :rtype:  ``bool``
    """

Point2.__lt__.__doc__ = """
    Compares the lexicographic ordering of ``self`` and ``other``.
    
    Lexicographic ordering checks the x-coordinate first, and then y.
    
    :param other: The object to check
    :type other:  ``Point2``
    
    :return: True if ``self`` is lexicographic kess than ``other``
    :rtype:  ``float``
    """

Point2.__neg__.__doc__ = """
    Negates this point, producing a new object.
    
    :return: the negation of this tuple
    :rtype:  ``Point2``
    """

Point2.__abs__.__doc__ = """
    Creates a copy where each component of this tuple is its absolute value.
    
    :return: the absolute value of this tuple
    :rtype:  ``Point2``
    """

Point2.__mul__.__doc__ = """
    Multiples this object by a scalar, ``Point2``, or a ``Matrix``, producing a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a point, then the
    result is pointwise multiplication. Finally, if is a matrix, then we use the
    matrix to transform the object.  We treat matrix transformation as multiplication
    on the right to make in-place multiplication easier.  See :class:`Matrix` doe more
    
    :param value: value to multiply by
    :type value:  ``int``, ``float``, ``Point2`` or ``Matrix``
    
    :return: the altered object
    :rtype:  ``Point2``
    """

Point2.__rmul__.__doc__ = """
    Multiplies this object by a scalar or ``Point2`` on the left.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a 2d tuple, then the
    result is pointwise multiplication. We do not allow matrix multiplication on 
    the left. 
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Point2``
    
    :return: the scalar multiple of ``self`` and ``scalar``
    :rtype:  ``Point2``
    """

Point2.__truediv__.__doc__ = """
    Divides this object by a scalar or a ``Point2`` on the right, producting a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar division.  If it is a ``Point2``, then the
    result is pointwise division.
    
    The value returned has the same type as ``self`` (so if ``self`` is an instance
    of a subclass, it uses that object instead of the original class. The contents of 
    this object are not altered.
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Point2``
    
    :return: the division of ``self`` by ``value``
    :rtype:  ``Point2``
    """

Point2.__rtruediv__.__doc__ = """
    Divides a scalar or ``Point2`` by this object.
    
    Dividing by a point means pointwise reciprocation, followed by multiplication.
    
    :param value: The value to divide
    :type value:  ``int``, ``float``, or ``Point2``
    
    :return: the division of ``value`` by ``self``
    :rtype: 
    """
    
Point2.under.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the first are greater 
    than or equal to the components of the second.  This is a partial order, not a total 
    one.
    
    :param other: The object to check
    :type other:  ``Point2``
    
    :return: True if ``other`` dominates ``self``; False otherwise
    :rtype:  ``bool``
    """

Point2.over.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the 
    first are greater than or equal to the components of the second.  This is a
    partial order, not a total one.
    
    :param other: The object to check
    :type other:  ``Point2``
    
    :return: True if ``self`` dominates ``other``; False otherwise
    :rtype:  ``bool``
    """

Point2.isZero.__doc__ = """
    Determines whether or not this object is 'close enough' to the origin.
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :return: True if this object is 'close enough' to the origin; False otherwise
    :rtype:  ``bool``
    """

Point2.interpolant.__doc__ = """
    Interpolates this object with another, producing a new object
    
    The resulting value is::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    :param other: object to interpolate with
    :type other:  ``Point2``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: the interpolation of this object and ``other`` via ``alpha``.
    :rtype:  ``Point2``
    """

Point2.interpolate.__doc__ = """
    Interpolates this object with another in place
    
    This method will modify the attributes of this oject.  The new attributes will
    be equivalent to::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    This method returns this object for chaining.
    
    :param other: object to interpolate with
    :type other:  ``Point2``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: This object, newly modified
    """

Point2.copy.__doc__ = """
    :return: A copy of this point
    :rtype:  ``Point2``
    """

Point2.list.__doc__ = """
    :return: A python list with the contents of this point.
    :rtype:  ``list``
    """

Point2.clamp.__doc__ = """
    Clamps this point to the range [``low``, ``high``].
    
    Any value in this tuple less than ``low`` is set to ``low``.  Any value greater 
    than ``high`` is set to ``high``.
    
    This method returns this object for chaining.
    
    :param low: The low range of the clamp
    :type low:  ``int`` or ``float``
    
    :param high: The high range of the clamp
    :type high:  ``int`` or ``float``
    
    :return: This object, newly modified
    :rtype:  ``Point2``
    """


# #mark -
# #mark Point3 docs
Point3.__eq__.__doc__ = """
    Compares this point with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.  Equivalence also requires type
    equivalence.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: True if ``self`` and ``other`` are equivalent
    :rtype:  ``bool``
    """

Point3.__ne__.__doc__ = """
    Compares this object with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: False if ``self`` and ``other`` are equivalent objects. 
    :rtype:  ``bool``
    """

Point3.__lt__.__doc__ = """
    Compares the lexicographic ordering of ``self`` and ``other``.
    
    Lexicographic ordering checks the x-coordinate first, and then y.
    
    :param other: The object to check
    :type other:  ``Point3``
    
    :return: True if ``self`` is lexicographic kess than ``other``
    :rtype:  ``float``
    """

Point3.__neg__.__doc__ = """
    Negates this point, producing a new object.
    
    :return: the negation of this tuple
    :rtype:  ``Point3``
    """

Point3.__abs__.__doc__ = """
    Creates a copy where each component of this tuple is its absolute value.
    
    :return: the absolute value of this tuple
    :rtype:  ``Point3``
    """

Point3.__mul__.__doc__ = """
    Multiples this object by a scalar, ``Point3``, or a ``Matrix``, producing a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a point, then the
    result is pointwise multiplication. Finally, if is a matrix, then we use the
    matrix to transform the object.  We treat matrix transformation as multiplication
    on the right to make in-place multiplication easier.  See :class:`Matrix` doe more
    
    :param value: value to multiply by
    :type value:  ``int``, ``float``, ``Point3`` or ``Matrix``
    
    :return: the altered object
    :rtype:  ``Point3``
    """

Point3.__rmul__.__doc__ = """
    Multiplies this object by a scalar or ``Point3`` on the left.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a 2d tuple, then the
    result is pointwise multiplication. We do not allow matrix multiplication on 
    the left. 
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Point3``
    
    :return: the scalar multiple of ``self`` and ``scalar``
    :rtype:  ``Point3``
    """

Point3.__truediv__.__doc__ = """
    Divides this object by a scalar or a ``Point3`` on the right, producting a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar division.  If it is a ``Point3``, then the
    result is pointwise division.
    
    The value returned has the same type as ``self`` (so if ``self`` is an instance
    of a subclass, it uses that object instead of the original class. The contents of 
    this object are not altered.
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Point3``
    
    :return: the division of ``self`` by ``value``
    :rtype:  ``Point3``
    """

Point3.__rtruediv__.__doc__ = """
    Divides a scalar or ``Point3`` by this object.
    
    Dividing by a point means pointwise reciprocation, followed by multiplication.
    
    :param value: The value to divide
    :type value:  ``int``, ``float``, or ``Point3``
    
    :return: the division of ``value`` by ``self``
    :rtype: 
    """
    
Point3.under.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the first are greater 
    than or equal to the components of the second.  This is a partial order, not a total 
    one.
    
    :param other: The object to check
    :type other:  ``Point3``
    
    :return: True if ``other`` dominates ``self``; False otherwise
    :rtype:  ``bool``
    """

Point3.over.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the 
    first are greater than or equal to the components of the second.  This is a
    partial order, not a total one.
    
    :param other: The object to check
    :type other:  ``Point3``
    
    :return: True if ``self`` dominates ``other``; False otherwise
    :rtype:  ``bool``
    """

Point3.isZero.__doc__ = """
    Determines whether or not this object is 'close enough' to the origin.
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :return: True if this object is 'close enough' to the origin; False otherwise
    :rtype:  ``bool``
    """

Point3.interpolant.__doc__ = """
    Interpolates this object with another, producing a new object
    
    The resulting value is::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    :param other: object to interpolate with
    :type other:  ``Point3``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: the interpolation of this object and ``other`` via ``alpha``.
    :rtype:  ``Point3``
    """

Point3.interpolate.__doc__ = """
    Interpolates this object with another in place
    
    This method will modify the attributes of this oject.  The new attributes will
    be equivalent to::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    This method returns this object for chaining.
    
    :param other: object to interpolate with
    :type other:  ``Point3``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: This object, newly modified
    """

Point3.copy.__doc__ = """
    :return: A copy of this point
    :rtype:  ``Point3``
    """

Point3.list.__doc__ = """
    :return: A python list with the contents of this point.
    :rtype:  ``list``
    """

Point3.clamp.__doc__ = """
    Clamps this point to the range [``low``, ``high``].
    
    Any value in this tuple less than ``low`` is set to ``low``.  Any value greater 
    than ``high`` is set to ``high``.
    
    This method returns this object for chaining.
    
    :param low: The low range of the clamp
    :type low:  ``int`` or ``float``
    
    :param high: The high range of the clamp
    :type high:  ``int`` or ``float``
    
    :return: This object, newly modified
    :rtype:  ``Point3``
    """