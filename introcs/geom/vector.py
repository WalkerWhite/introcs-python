"""
Classes for representing vectors.

Vectors have magnitude and direction, but they do not have position.  Use the point classes
if you want position.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
# The docs at the bottom are to hide inheritance from the documentation
from .tuple import Tuple2, Tuple3
import math

class Vector2(Tuple2):
    """
    An instance is a vector in 2D space.
    
    :ivar x: The x-coordinate
    :vartype x: ``float``
    
    :ivar y: The y-coordinate
    :vartype y: ``float``
    """
    
    # BUILT-IN METHODS
    def __init__(self, x=0, y=0):
        """
        All values are 0.0 by default.
        """
        Tuple2.__init__(self,x,y)
    
    def __str__(self):
        """
        :return: A readable string representation of this vector. 
        :rtype:  ``bool``
        """
        return "<"+str(self.x)+","+str(self.y)+">"
    
    def __add__(self, other):
        """
        Performs a context dependent addition of this vector and ``other``.
        
        If ``other`` is a vector, the result is vector addition.  If it is point,
        the result is the head of the vector when it is anchored at this point.
        
        :param other: object to add
        :type other:  ``Point2`` or ``Vector2``
        
        :return: the sum of this object and ``other``.
        :rtype:  ``Point2`` or ``Vector2``
        """
        from .point import Point2
        if isinstance(other,Point2):
            result = self.toPoint()
        elif isinstance(other,Vector2):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x += other.x
        result.y += other.y
        return result
    
    def __sub__(self, other):
        """
        Performs a context dependent subtraction of this vector and ``other``.
        
        If ``other`` is a vector, the result is vector subtraction.  If it is point,
        the result is the tail of the vector when it has its head at this point.
        
        :param other: object to subtract
        :type other:  ``Point2`` or ``Vector2``
        
        :return: the difference of this object and ``other``.
        :rtype:  ``Point2`` or ``Vector2``
        """
        from .point import Point2
        if isinstance(other,Point2):
            result = self.toPoint()
        elif isinstance(other,Vector2):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x -= other.x
        result.y -= other.y
        return result
    
    
    # PUBLIC METHODS
    def toPoint(self):
        """
        :return: The ``Point2`` object equivalent to this vector
        :rtype:  ``Point2``
        """
        from .point import Point2
        return Point2(self.x,self.y)
    
    def length(self):
        """
        Computes the magnitude of this vector.
        
        :return: the length of this vector.
        :rtype:  ``float``
        """
        import math
        return math.sqrt(self.x*self.x+self.y*self.y)
    
    def length2(self):
        """
        Computes the square of the magnitude of this vector
        
        This method is slightly faster than :meth:`length`.
        
        :return: the square of the length of this vector.
        :rtype:  ``float``
        """
        return self.x*self.x+self.y*self.y
    
    def isUnit(self):
        """
        Determines whether or not this object is 'close enough' to a unit vector.
        
        A unit vector is one that has length 1. This method uses ``numpy`` to test whether
        the lenght is  "close enough", and does not require exact equuivalence.
        
        :return: True if this object is 'close enough' to a unit vector; False otherwise
        :rtype:  ``bool``
        """
        import numpy
        return numpy.allclose([self.length2()],[1])
    
    def normal(self):
        """
        Normalizes this vector, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :return: the normalized version of this vector
        :rtype:  ``type(self)``
        """
        assert self, '%s is the zero vector' % repr(self)
        return self/self.length()
    
    def normalize(self):
        """
        Normalizes this vector in place.
        
        This method alters the vector so that it has the same direction,  but its length 
        is now 1.  The method returns this object for chaining.
        
        :return: This object, newly modified
        """
        assert self, '%s is the zero vector' % repr(self)
        self /= self.length()
        return self
    
    def angle(self,other):
        """
        Computes the angle between two vectors.
        
        The answer provided is in radians. Neither this vector nor ``other`` may be the 
        zero vector.
        
        :param other: value to compare against
        :type other:  nonzero ``Vector2``
        
        :return:: the angle between this vector and other.
        :rtype:  ``float``
        """
        assert (isinstance(other, Vector2)), "%s is not a valid vector" % repr(other)
        import math
        na = self.length()
        nb = other.length()
        
        if na*nb == 0:
            return 0
        return math.acos(self.dot(other)/(na*nb))
    
    def rotate(self,angle):
        """
        Rotates this vector by the angle (in radians) around the origin in place
        
        The rotation angle is given in degrees, not radians. Rotation is counterclockwise 
        around the z-axis.
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param angle: angle of rotation in degrees
        :type angle:  ``int`` or ``float``
        
        :return: This object, newly modified
        """
        assert type(angle) in [int,float], "%s is not a number" % repr(angle)
        ca = math.cos(angle)
        cb = math.sin(angle)
        x = self.x*ca - self.y*cb
        y = self.x*cb + self.y*ca
        self.x = x
        self.y = y
        return self
    
    def rotation(self,angle):
        """
        Rotates this vector by the angle (in radians) around the origin, producing a new object
        
        The rotation angle is given in degrees, not radians. Rotation is counterclockwise 
        around the z-axis.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param angle: angle of rotation in degrees
        :type angle:  ``int`` or ``float``
        
        :return: The rotation of this vector by ``angle``
        :rtype:  ``type(self)``
        """
        assert type(angle) in [int,float], "%s is not a number" % repr(angle)
        ca = math.cos(angle)
        cb = math.sin(angle)
        result = self.copy()
        result.x = self.x*ca - self.y*cb
        result.y = self.x*cb + self.y*ca
        return result
    
    def dot(self,other):
        """
        Computes the dot project of this vector with ``other``
        
        :param other: value to dot
        :type other:  ``Vector2``
        
        :return: the dot product between this vector and ``other``.
        :rtype:  ``float``
        """
        assert (isinstance(other, Vector2)), "%s is not a valid vector" % repr(other)
        return (self.x*other.x+self.y*other.y)
    
    def cross(self,other):
        """
        Computes the cross project of this vector with ``other``
        
        In two dimensions, the value is the magnitude of the z-axis.
        
        :param other: value to cross
        :type other:  ``Vector2``
        
        :return: the cross product between this vector and ``other``.
        :rtype:  ``float``
        """
        assert (isinstance(other, Vector2)), "%s is not a valid vector" % repr(other)
        return self.x*other.y - self.y*other.x
    
    def perp(self):
        """
        Computes a vector perpendicular to this one.
        
        The resulting vector is rotated 90 degrees counterclockwise.
        
        :return: a 2D vector perpendicular to this one
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = self.y
        result.y = -self.x
        return result
    
    def rperp(self):
        """
        Computes a vector perpendicular to this one.
        
        The resulting vector is rotated 90 degrees clockwise.
        
        :return: a 2D vector perpendicular to this one
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = -self.y
        result.y = self.x
        return result
    
    def project(self,other):
        """
        Computes the project of this vector on to ``other``
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param other: value to project on to
        :type other:  ``Vector2``
        
        :return: This object, newly modified
        """
        assert (isinstance(other, Vector2)), "%s is not a valid vector" % repr(other)
        dot   = self.dot(other)
        base  = other.length2()
        other = other*(dot/base)
        self.x = other.x
        self.y = other.y
        return self
    
    def projection(self,other):
        """
        Computes the project of this vector on to ``other``
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param other: value to project on to
        :type other:  ``Vector2``
        
        ::return: the projection of this vector on to ``other``.
        :rtype:  ``Vector2``
        """
        assert (isinstance(other, Vector2)), "%s is not a valid vector" % repr(other)
        dot  = self.dot(other)
        base = other.length2()
        return (dot/base)*other


# #mark -
class Vector3(Tuple3):
    """
    An instance is a vector in 3D space.
    """
    
    # BUILT-IN METHODS
    def __init__(self, x=0, y=0, z=0):
        """
        All values are 0.0 by default.
        
        :param x: initial x value
        :type x:  ``int`` or ``float``
        
        :param y: initial y value
        :type y:  ``int`` or ``float``
        
        :param z: initial z value
        :type z:  ``int`` or ``float``
        """
        Tuple3.__init__(self,x,y,z)
    
    def __str__(self):
        """
        :return: A readable string representation of this vector. 
        :rtype:  ``bool``
        """
        return "<"+str(self.x)+","+str(self.y)+","+str(self.z)+">"
    
    
    def __add__(self, other):
        """
        Performs a context dependent addition of this vector and ``other``.
        
        If ``other`` is a vector, the result is vector addition.  If it is point,
        the result is the head of the vector when it is anchored at this point.
        
        :param other: object to add
        :type other:  ``Point3`` or ``Vector3``
        
        :return: the sum of this object and ``other``.
        :rtype:  ``Point3`` or ``Vector3``
        """
        from .point import Point3
        if isinstance(other,Point3):
            result = self.toPoint()
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
        Performs a context dependent subtraction of this vector and ``other``.
        
        If ``other`` is a vector, the result is vector subtraction.  If it is point,
        the result is the tail of the vector when it has its head at this point.
        
        :param other: object to subtract
        :type other:  ``Point3`` or ``Vector3``
        
        :return: the difference of this object and ``other``.
        :rtype:  ``Point3`` or ``Vector3``
        """
        from .point import Point3
        if isinstance(other,Point3):
            result = self.toPoint()
        elif isinstance(other,Vector3):
            result = self.copy()
        else:
            assert False, "%s is not a valid value" % repr(other)
        
        result.x -= other.x
        result.y -= other.y
        result.z -= other.z
        return result
    
    
    # PUBLIC METHODS
    def toPoint(self):
        """
        :return: The ``Point3`` object equivalent to this vector
        :rtype:  ``Point3``
        """
        from .point import Point3
        return Point3(self.x,self.y,self.z)
    
    def length(self):
        """
        Computes the magnitude of this vector.
        
        :return: the length of this vector.
        :rtype:  ``float``
        """
        import math
        return math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    
    def length2(self):
        """
        Computes the square of the magnitude of this vector
        
        This method is slightly faster than :meth:`length`.
        
        :return: the square of the length of this vector.
        :rtype:  ``float``
        """
        return self.x*self.x+self.y*self.y+self.z*self.z
    
    def isUnit(self):
        """
        Determines whether or not this object is 'close enough' to a unit vector.
        
        A unit vector is one that has length 1. This method uses ``numpy`` to test whether
        the lenght is  "close enough", and does not require exact equuivalence.
        
        :return: True if this object is 'close enough' to a unit vector; False otherwise
        :rtype:  ``bool``
        """
        import numpy
        return numpy.allclose([self.length2()],[1])
    
    def normal(self):
        """
        Normalizes this vector, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :return: the normalized version of this vector
        :rtype:  ``type(self)``
        """
        assert self, '%s is the zero vector' % repr(self)
        return self/self.length()
    
    def normalize(self):
        """
        Normalizes this vector in place.
        
        This method alters the vector so that it has the same direction,  but its length 
        is now 1.  The method returns this object for chaining.
        
        :return: This object, newly modified
        """
        assert self, '%s is the zero vector' % repr(self)
        self /= self.length()
        return self
    
    def angle(self,other):
        """
        Computes the angle between two vectors.
        
        The answer provided is in radians. Neither this vector nor ``other`` may be the 
        zero vector.
        
        :param other: value to compare against
        :type other:  nonzero ``Vector2``
        
        :return:: the angle between this vector and other.
        :rtype:  ``float``
        """
        assert (isinstance(other, Vector3)), "%s is not a valid vector" % repr(other)
        import math
        import numpy
        
        dx = self.y * other.z - self.z * other.y;
        dy = self.z * other.x - self.x * other.z;
        dz = self.x * other.y - self.y * other.x;
        dc = math.sqrt(dx * dx + dy * dy + dz * dz);
        
        angle = 0.0 if numpy.allclose([dc],[0]) else math.atan2(dc, self.dot(other))
        return angle
    
    def dot(self,other):
        """
        Computes the dot project of this vector with ``other``
        
        :param other: value to dot
        :type other:  ``Vector3``
        
        :return: the dot product between this vector and ``other``.
        :rtype:  ``float``
        """
        assert (isinstance(other, Vector3)), "%s is not a valid vector" % repr(other)
        return (self.x*other.x+self.y*other.y+self.z*other.z)
    
    def cross(self,other):
        """
        Computes the cross project of this vector with ``other``, producing a new vector
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param other: value to cross
        :type other:  ``Vector3``
        
        :return: the cross product between this vector and ``other``.
        :rtype:  ``Vector3``
        """
        assert (isinstance(other, Vector3)), "%s is not a valid vector" % repr(other)
        result = self.copy()
        result.x = (self.y * other.z) - (self.z * other.y)
        result.y = (self.z * other.x) - (self.x * other.z)
        result.z = (self.x * other.y) - (self.y * other.x)
        return result
    
    def crossify(self,other):
        """
        Computes the cross project of this vector with ``other`` in place
        
        This method alters the vector so it is the result of the cross product,  but its length 
        is now 1.  The method returns this object for chaining.
        
        :param other: value to cross
        :type other:  ``Vector3``
        
        :return: This object, newly modified
        """
        assert (isinstance(other, Vector3)), "%s is not a valid vector" % repr(other)
        x = (self.y * other.z) - (self.z * other.y)
        y = (self.z * other.x) - (self.x * other.z)
        z = (self.x * other.y) - (self.y * other.x)
        self.x = x
        self.y = y
        self.z = z
        return self
    
    def project(self,other):
        """
        Computes the project of this vector on to ``other``
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param other: value to project on to
        :type other:  ``Vector3``
        
        :return: This object, newly modified
        """
        assert (isinstance(other, Vector3)), "%s is not a valid vector" % repr(other)
        dot   = self.dot(other)
        base  = other.length2()
        other = other*(dot/base)
        self.x = other.x
        self.y = other.y
        self.z = other.z
        return self
    
    def projection(self,other):
        """
        Computes the project of this vector on to ``other``
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param other: value to project on to
        :type other:  ``Vector3``
        
        ::return: the projection of this vector on to ``other``.
        :rtype:  ``Vector3``
        """
        assert (isinstance(other, Vector3)), "%s is not a valid vector" % repr(other)
        dot  = self.dot(other)
        base = other.length2()
        return (dot/base)*other


# Make 3-dimensions the default
Vector = Vector3

# #mark -
# #mark Vector2 docs
Vector2.__eq__.__doc__ = """
    Compares this point with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.  Equivalence also requires type
    equivalence.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: True if ``self`` and ``other`` are equivalent
    :rtype:  ``bool``
    """

Vector2.__ne__.__doc__ = """
    Compares this object with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: False if ``self`` and ``other`` are equivalent objects. 
    :rtype:  ``bool``
    """

Vector2.__lt__.__doc__ = """
    Compares the lexicographic ordering of ``self`` and ``other``.
    
    Lexicographic ordering checks the x-coordinate first, and then y.
    
    :param other: The object to check
    :type other:  ``Vector2``
    
    :return: True if ``self`` is lexicographic kess than ``other``
    :rtype:  ``float``
    """

Vector2.__neg__.__doc__ = """
    Negates this point, producing a new object.
    
    :return: the negation of this tuple
    :rtype:  ``Vector2``
    """

Vector2.__abs__.__doc__ = """
    Creates a copy where each component of this tuple is its absolute value.
    
    :return: the absolute value of this tuple
    :rtype:  ``Vector2``
    """

Vector2.__mul__.__doc__ = """
    Multiples this object by a scalar, ``Vector2``, or a ``Matrix``, producing a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a point, then the
    result is pointwise multiplication. Finally, if is a matrix, then we use the
    matrix to transform the object.  We treat matrix transformation as multiplication
    on the right to make in-place multiplication easier.  See :class:`Matrix` doe more
    
    :param value: value to multiply by
    :type value:  ``int``, ``float``, ``Vector2`` or ``Matrix``
    
    :return: the altered object
    :rtype:  ``Vector2``
    """

Vector2.__rmul__.__doc__ = """
    Multiplies this object by a scalar or ``Vector2`` on the left.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a 2d tuple, then the
    result is pointwise multiplication. We do not allow matrix multiplication on 
    the left. 
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Vector2``
    
    :return: the scalar multiple of ``self`` and ``scalar``
    :rtype:  ``Vector2``
    """

Vector2.__truediv__.__doc__ = """
    Divides this object by a scalar or a ``Vector2`` on the right, producting a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar division.  If it is a ``Vector2``, then the
    result is pointwise division.
    
    The value returned has the same type as ``self`` (so if ``self`` is an instance
    of a subclass, it uses that object instead of the original class. The contents of 
    this object are not altered.
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Vector2``
    
    :return: the division of ``self`` by ``value``
    :rtype:  ``Vector2``
    """

Vector2.__rtruediv__.__doc__ = """
    Divides a scalar or ``Vector2`` by this object.
    
    Dividing by a point means pointwise reciprocation, followed by multiplication.
    
    :param value: The value to divide
    :type value:  ``int``, ``float``, or ``Vector2``
    
    :return: the division of ``value`` by ``self``
    :rtype: 
    """
    
Vector2.under.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the first are greater 
    than or equal to the components of the second.  This is a partial order, not a total 
    one.
    
    :param other: The object to check
    :type other:  ``Vector2``
    
    :return: True if ``other`` dominates ``self``; False otherwise
    :rtype:  ``bool``
    """

Vector2.over.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the 
    first are greater than or equal to the components of the second.  This is a
    partial order, not a total one.
    
    :param other: The object to check
    :type other:  ``Vector2``
    
    :return: True if ``self`` dominates ``other``; False otherwise
    :rtype:  ``bool``
    """

Vector2.isZero.__doc__ = """
    Determines whether or not this object is 'close enough' to the origin.
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :return: True if this object is 'close enough' to the origin; False otherwise
    :rtype:  ``bool``
    """

Vector2.interpolant.__doc__ = """
    Interpolates this object with another, producing a new object
    
    The resulting value is::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    :param other: object to interpolate with
    :type other:  ``Vector2``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: the interpolation of this object and ``other`` via ``alpha``.
    :rtype:  ``Vector2``
    """

Vector2.interpolate.__doc__ = """
    Interpolates this object with another in place
    
    This method will modify the attributes of this oject.  The new attributes will
    be equivalent to::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    This method returns this object for chaining.
    
    :param other: object to interpolate with
    :type other:  ``Vector2``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: This object, newly modified
    """

Vector2.copy.__doc__ = """
    :return: A copy of this point
    :rtype:  ``Vector2``
    """

Vector2.list.__doc__ = """
    :return: A python list with the contents of this point.
    :rtype:  ``list``
    """

Vector2.clamp.__doc__ = """
    Clamps this point to the range [``low``, ``high``].
    
    Any value in this tuple less than ``low`` is set to ``low``.  Any value greater 
    than ``high`` is set to ``high``.
    
    This method returns this object for chaining.
    
    :param low: The low range of the clamp
    :type low:  ``int`` or ``float``
    
    :param high: The high range of the clamp
    :type high:  ``int`` or ``float``
    
    :return: This object, newly modified
    :rtype:  ``Vector2``
    """

# #mark -
# #mark Vector3 docs
Vector3.__eq__.__doc__ = """
    Compares this point with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.  Equivalence also requires type
    equivalence.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: True if ``self`` and ``other`` are equivalent
    :rtype:  ``bool``
    """

Vector3.__ne__.__doc__ = """
    Compares this object with ``other`` 
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :param other: The object to check
    :type other:  ``any``
    
    :return: False if ``self`` and ``other`` are equivalent objects. 
    :rtype:  ``bool``
    """

Vector3.__lt__.__doc__ = """
    Compares the lexicographic ordering of ``self`` and ``other``.
    
    Lexicographic ordering checks the x-coordinate first, and then y.
    
    :param other: The object to check
    :type other:  ``Vector3``
    
    :return: True if ``self`` is lexicographic kess than ``other``
    :rtype:  ``float``
    """

Vector3.__neg__.__doc__ = """
    Negates this point, producing a new object.
    
    :return: the negation of this tuple
    :rtype:  ``Vector3``
    """

Vector3.__abs__.__doc__ = """
    Creates a copy where each component of this tuple is its absolute value.
    
    :return: the absolute value of this tuple
    :rtype:  ``Vector3``
    """

Vector3.__mul__.__doc__ = """
    Multiples this object by a scalar, ``Vector3``, or a ``Matrix``, producing a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a point, then the
    result is pointwise multiplication. Finally, if is a matrix, then we use the
    matrix to transform the object.  We treat matrix transformation as multiplication
    on the right to make in-place multiplication easier.  See :class:`Matrix` doe more
    
    :param value: value to multiply by
    :type value:  ``int``, ``float``, ``Vector3`` or ``Matrix``
    
    :return: the altered object
    :rtype:  ``Vector3``
    """

Vector3.__rmul__.__doc__ = """
    Multiplies this object by a scalar or ``Vector3`` on the left.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar multiplication.  If it is a 2d tuple, then the
    result is pointwise multiplication. We do not allow matrix multiplication on 
    the left. 
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Vector3``
    
    :return: the scalar multiple of ``self`` and ``scalar``
    :rtype:  ``Vector3``
    """

Vector3.__truediv__.__doc__ = """
    Divides this object by a scalar or a ``Vector3`` on the right, producting a new object.
    
    The exact effect is determined by the type of value. If ``value`` is a scalar, 
    the result is standard scalar division.  If it is a ``Vector3``, then the
    result is pointwise division.
    
    The value returned has the same type as ``self`` (so if ``self`` is an instance
    of a subclass, it uses that object instead of the original class. The contents of 
    this object are not altered.
    
    :param value: The value to multiply by
    :type value:  ``int``, ``float``, or ``Vector3``
    
    :return: the division of ``self`` by ``value``
    :rtype:  ``Vector3``
    """

Vector3.__rtruediv__.__doc__ = """
    Divides a scalar or ``Vector3`` by this object.
    
    Dividing by a point means pointwise reciprocation, followed by multiplication.
    
    :param value: The value to divide
    :type value:  ``int``, ``float``, or ``Vector3``
    
    :return: the division of ``value`` by ``self``
    :rtype: 
    """
    
Vector3.under.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the first are greater 
    than or equal to the components of the second.  This is a partial order, not a total 
    one.
    
    :param other: The object to check
    :type other:  ``Vector3``
    
    :return: True if ``other`` dominates ``self``; False otherwise
    :rtype:  ``bool``
    """

Vector3.over.__doc__ = """
    Compares ``self`` to ``other`` under the domination partial order
    
    We say that one point dominates  another is all components of the 
    first are greater than or equal to the components of the second.  This is a
    partial order, not a total one.
    
    :param other: The object to check
    :type other:  ``Vector3``
    
    :return: True if ``self`` dominates ``other``; False otherwise
    :rtype:  ``bool``
    """

Vector3.isZero.__doc__ = """
    Determines whether or not this object is 'close enough' to the origin.
    
    This method uses ``numpy`` to test whether the coordinates are  "close enough".  
    It does not require exact equality for floats.
    
    :return: True if this object is 'close enough' to the origin; False otherwise
    :rtype:  ``bool``
    """

Vector3.interpolant.__doc__ = """
    Interpolates this object with another, producing a new object
    
    The resulting value is::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    :param other: object to interpolate with
    :type other:  ``Vector3``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: the interpolation of this object and ``other`` via ``alpha``.
    :rtype:  ``Vector3``
    """

Vector3.interpolate.__doc__ = """
    Interpolates this object with another in place
    
    This method will modify the attributes of this oject.  The new attributes will
    be equivalent to::
        
        alpha*self+(1-alpha)*other 
    
    according to the rules of addition and scalar multiplication.
    
    This method returns this object for chaining.
    
    :param other: object to interpolate with
    :type other:  ``Vector3``
    
    :param alpha: scalar to interpolate by
    :type alpha:  ``int`` or ``float``
    
    :return: This object, newly modified
    """

Vector3.copy.__doc__ = """
    :return: A copy of this point
    :rtype:  ``Vector3``
    """

Vector3.list.__doc__ = """
    :return: A python list with the contents of this point.
    :rtype:  ``list``
    """

Vector3.clamp.__doc__ = """
    Clamps this point to the range [``low``, ``high``].
    
    Any value in this tuple less than ``low`` is set to ``low``.  Any value greater 
    than ``high`` is set to ``high``.
    
    This method returns this object for chaining.
    
    :param low: The low range of the clamp
    :type low:  ``int`` or ``float``
    
    :param high: The high range of the clamp
    :type high:  ``int`` or ``float``
    
    :return: This object, newly modified
    :rtype:  ``Vector3``
    """