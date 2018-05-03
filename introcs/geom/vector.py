"""
Classes for representing vectors.

Vectors have magnitude and direction, but they do not have position.  Use the point classes
if you want position.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
from .tuple import Tuple2, Tuple3
import math

class Vector2(Tuple2):
    """
    An instance is a vector in 2D space.
    
    This class is a subclass of :class:``Tuple2`` and inherits all of its attributes and 
    methods.
    
    :ivar x: The x-coordinate
    :vartype x: ``float``
    
    :ivar y: The y-coordinate
    :vartype y: ``float``
    """
    
    # BUILT-IN METHODS
    def __init__(self, x=0, y=0):
        """
        Creates a new Vector2 value (x,y).
        
        All values are 0.0 by default.
        
        :return: a new Vector2 value (x,y).
        
        :param x: initial x value
        :type x:  ``int`` or ``float``
            
        :param y: initial y value
        :type y:  ``int`` or ``float``
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
    
    def __sub__(self, tail):
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
        
        if na*nb == 0:
            return 0
        return math.acos(self.dot(other)/(na*nb))
    
    def rotate(angle):
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
        ca = math.cos(a)
        cb = math.sin(a)
        self.x = self.x*ca - self.y*cb
        self.y = self.x*cb + self.y*ca
        return self
    
    def rotation(angle):
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
        ca = math.cos(a)
        cb = math.sin(a)
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
        dot  = self.dot(other)
        base = other.length2()
        self *= (dot/base)
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
    
    This class is a subclass of :class:``Tuple2`` and inherits all of its attributes and 
    methods.
    
    :ivar x: The x-coordinate
    :vartype x: ``float``
    
    :ivar y: The y-coordinate
    :vartype y: ``float``
    
    :ivar z: The z-coordinate
    :vartype z: ``float``
    """
    
    # BUILT-IN METHODS
    def __init__(self, x=0, y=0, z=0):
        """
        Creates a new Vector3 value (x,y).
        
        All values are 0.0 by default.
        
        :return: a new Vector3 value (x,y).
        
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
    
    def __sub__(self, tail):
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
        self.x = (self.y * other.z) - (self.z * other.y)
        self.y = (self.z * other.x) - (self.x * other.z)
        self.z = (self.x * other.y) - (self.y * other.x)
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
        dot  = self.dot(other)
        base = other.length2()
        self *= (dot/base)
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
