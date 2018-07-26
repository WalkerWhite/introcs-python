"""
The base tuple classes for points and vectors.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""
from functools import total_ordering

@total_ordering
class Tuple2(object):
    """
    An instance is a tuple in 2D space.
    
    This serves as the base class for both Point2 and Vector2.
    
    :ivar x: The x-coordinate
    :vartype x: ``float``

    :ivar y: The y-coordinate
    :vartype y: ``float``
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def x(self):
        """
        The x coordinate
        
        **Invariant**: Value must be an ``int`` or  ``float``.
        """
        return self._x
    
    @x.setter
    def x(self, value):
        assert type(value) in [int,float]
        self._x = float(value)
    
    @property
    def y(self):
        """
        The y coordinate
        
        **Invariant**: Value must be an ``int`` or  ``float``.
        """
        return self._y
    
    @y.setter
    def y(self, value):
        assert type(value) in [int,float]
        self._y = float(value)
    
    
    # OBJECT REPRESENTATION
    def __init__(self, x=0, y=0):
        """
        Creates a new ``Tuple2`` value (x,y).
        
        All values are 0.0 by default.
        
        :return: a new ``Tuple2`` value (x,y).
        
        :param x: initial x value
        :type x:  ``int`` or ``float``
            
        :param y: initial y value
        :type y:  ``int`` or ``float``
        """
        self.x = x
        self.y = y
    
    def __str__(self):
        """
        :return: A readable string representation of this object. 
        :rtype:  ``bool``
        """
        return "("+str(self.x)+","+str(self.y)+")"
    
    def __repr__(self):
        """
        :return: An unambiguous string representation of this object.
        :rtype:  ``bool``
        """
        return "%s%s" % (self.__class__,self.__str__())
    
    
    # COMPARISON
    def __eq__(self, other):
        """
        Compares this object with ``other`` 
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.  Equivalence also requires type
        equivalence.
        
        :param other: The object to check
        
        :return: True if ``self`` and ``other`` are equivalent
        :rtype:  ``bool``
        """
        import numpy
        return (type(other) == type(self) and numpy.allclose(self.list(),other.list()))
    
    def __ne__(self, other):
        """
        Compares this object with ``other`` 
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.
        
        :param other: The object to check
        
        :return: False if ``self`` and ``other`` are equivalent objects. 
        :rtype:  ``bool``
        """
        return not self == other
    
    def __lt__(self,other):
        """
        Compares the lexicographic ordering of ``self`` and ``other``.
        
        Lexicographic ordering checks the x-coordinate first, and then y.
        
        :param other: The object to check
        :type other:  ``type(self)``
        
        :return: True if ``self`` is lexicographic kess than ``other``
        :rtype:  ``float``
        """
        assert isinstance(other, type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        import numpy
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
    
    def under(self,other):
        """
        Compares ``self`` to ``other`` under the domination partial order
        
        We say that one point or vector dominates  another is all components of the 
        first are greater than or equal to the components of the second.  This is a
        partial order, not a total one.
        
        :param other: The object to check
        :type other:  ``type(self)``
        
        :return: True if ``other`` dominates ``self``; False otherwise
        :rtype:  ``bool``
        """
        assert isinstance(other, type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        return self.x <= other.x and self.y <= other.y
    
    def over(self,other):
        """
        Compares ``self`` to ``other`` under the domination partial order
        
        We say that one point or vector dominates  another is all components of the 
        first are greater than or equal to the components of the second.  This is a
        partial order, not a total one.
        
        :param other: The object to check
        :type other:  ``type(self)``
        
        :return: True if ``self`` dominates ``other``; False otherwise
        :rtype:  ``bool``
        """
        assert isinstance(other, type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        return self.x >= other.x and self.y >= other.y
    
    def __bool__(self):
        """
        Computes the boolean value of this tuple.
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.
        
        :return: True if this object is 'close enough' to the origin; False otherwise
        :rtype:  ``bool``
        """
        return not self.isZero()
    
    def isZero(self):
        """
        Determines whether or not this object is 'close enough' to the origin.
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.
        
        :return: True if this object is 'close enough' to the origin; False otherwise
        :rtype:  ``bool``
        """
        import numpy
        return numpy.allclose([self.x,self.y],[0,0])
    
    
    # ARITHMETIC
    def __neg__(self):
        """
        Negates this tuple, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :return: the negation of this tuple
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = -result.x
        result.y = -result.y
        return result
    
    def __pos__(self):
        """
        Positivizes this tuple, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :return: a copy of this tuple
        :rtype:  ``type(self)``
        """
        return self.copy()
    
    def __abs__(self): 
        """
        Creates a copy where each component of this tuple is its absolute value.
        
        :return: the absolute value of this tuple
        :rtype:  ``type(self)``
        """
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self
    
    def __add__(self, other):
        """
        Adds the odject to another, producing a new object
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param other: object to add
        :type other:  ``type(self)``
        
        :return: the sum of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x += other.x
        result.y += other.y
        return result
    
    def __iadd__(self, other):
        """
        Adds ``other`` to this object in place.
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param other: tuple value to add
        :type other:  ``type(self)``
        
        :return: This object, newly modified
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        """
        Subtracts ``other`` from this object, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param other: object to subtract
        :type other:  ``type(self)``
        
        :return: the difference of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x -= other.x
        result.y -= other.y
        return result
    
    def __isub__(self, other):
        """
        Subtracts ``other`` from this object in place
        
        This method will modify the attributes of this oject.  This method returns this
        object for chaining.
        
        :param other: object to subtract
        :type other:  ``type(self)``
        
        :return: This object, newly modified
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x -= other.x
        self.y -= other.y
        return self
    
    def _imul_scalar_(self,scalar):
        """
        Multiplies this object by a scalar in place
        
        :param scalar: scalar to multiply by
        :type scalar:  ``int`` or ``float``
        """
        assert type(scalar) in [int,float], "%s is not a number" % repr(scalar)
        self.x *= scalar
        self.y *= scalar
    
    def _imul_tuple_(self,object):
        """
        Multiplies this object by another Tuple in place
        
        :param object: the tuple multiply by
        :type object:  ``type(self)``
        """
        assert isinstance(object,Tuple2), "%s is not a 2d tuple" % repr(object)
        self.x *= object.x
        self.y *= object.y
    
    def _imul_matrix_(self,matrix):
        """
        Transforms this object by a matrix in place
        
        :param matrix: matrix to transform with
        :type matrix:  :class:`Matrix`
        """
        from .matrix import Matrix
        import numpy as np
        assert isinstance(matrix,Matrix), "%s is not a matrix" % repr(matrix)
        b = np.array([self.x,self.y,0,1], dtype=np.float32)
        tmp = np.dot(matrix._data,b)
        self.x = float(tmp[0])
        self.y = float(tmp[1])
    
    def __mul__(self, value):
        """
        Multiples this object by a scalar, ``Tuple2``, or a matrix, producing a new object.
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar multiplication.  If it is a 2d tuple, then the
        result is pointwise multiplication. Finally, if is a matrix, then we use the
        matrix to transform the object.  We treat matrix transformation as multiplication
        orn the right to make in-place multiplication easier.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class.
        
        :param value: value to multiply by
        :type value:  ``int``, ``float``, :class:`Tuple2` or :class:`Matrix`
        
        :return: the altered object
        :rtype:  ``type(self)``
        """
        from .matrix import Matrix
        result = self.copy()
        if type(value) in [int,float]:
            result._imul_scalar_(value)
        elif isinstance(value,Tuple2):
            result._imul_tuple_(value)
        elif isinstance(value,Matrix):
            result._imul_matrix_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return result
    
    def __imul__(self, value):
        """
        Multiples this object by a scalar, Tuple2, or a matrix in place
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar multiplication.  If it is a 2d tuple, then the
        result is pointwise multiplication. Finally, if is a matrix, then we use the
        matrix to transform the object.  We treat matrix transformation as multiplication
        orn the right to make in-place multiplication easier.
        
        This method will modify the attributes of this oject.  This method returns this
        object for chaining.
        
        :param value: value to multiply by
        :type value:  ``int``, ``float``, or :class:`Matrix`
        
        :return: This object, newly modified
        """
        from .matrix import Matrix
        if type(value) in [int,float]:
            self._imul_scalar_(value)
        elif isinstance(value,Tuple2):
            self._imul_tuple_(value)
        elif isinstance(value,Matrix):
            self._imul_matrix_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return self
    
    def __rmul__(self, value):
        """
        Multiplies this object by a scalar or ``Tuple2`` on the left.
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar multiplication.  If it is a 2d tuple, then the
        result is pointwise multiplication. We do not allow matrix multiplication on 
        the left. 
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance 
        of a subclass, it uses that object instead of the original class. The contents 
        of this object are not altered.
        
        :param value: The value to multiply by
        :type value:  ``int``, ``float``, or ``Tuple2``
        
        :return: the scalar multiple of ``self`` and ``scalar``
        :rtype:  ``type(self)``
        """
        return self.__mul__(value)
    
    def _idiv_scalar_(self,scalar):
        """
        Divides this object by a scalar in place
        
        :param scalar: scalar to multiply by
        :type scalar:  ``int`` or ``float``
        """
        assert type(scalar) in [int,float], "%s is not a number" % repr(scalar)
        self.x /= scalar
        self.y /= scalar
    
    def _idiv_tuple_(self,object):
        """
        Divides this object by another tuple in place
        
        :param object: the tuple multiply by
        :type object:  ``type(self)``
        """
        assert isinstance(object,Tuple2), "%s is not a 2d tuple" % repr(object)
        self.x /= object.x
        self.y /= object.y
    
    def __truediv__(self, value):
        """
        Divides this object by a scalar or a tuple on the right, producting a new object.
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar division.  If it is a 2d tuple, then the
        result is pointwise division.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param value: The value to multiply by
        :type value:  ``int``, ``float``, or ``Tuple2``
        
        :return: the division of ``self`` by ``value``
        :rtype:  ``type(self)``
        """
        result = self.copy()
        if type(value) in [int,float]:
            result._idiv_scalar_(value)
        elif isinstance(value,Tuple2):
            result._idiv_tuple_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return result
    
    def __itruediv__(self, value):
        """
        Divides this object by a scalar or a tuple on the right in place
         
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar division.  If it is a 2d tuple, then the
        result is pointwise division.
       
        This method will modify the attributes of this oject.  This method returns this
        object for chaining.
        
        :param value: The value to multiply by
        :type value:  ``int``, ``float``, or ``Tuple2``
        
        :return: This object, newly modified
        """
        if type(value) in [int,float]:
            self._idiv_scalar_(value)
        elif isinstance(value,Tuple2):
            self._idiv_tuple_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return self
    
    def __rtruediv__(self, value):
        """
        Divides a scalar or tuple by this object.
        
        Dividing by a tuple means pointwise reciprocation, followed by multiplication.
        
        :param value: The value to divide
        :type value:  ``int``, ``float``, or ``Tuple2``
        
        :return: the division of ``value`` by ``self``
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = 1/result.x
        result.y = 1/result.y
        return result * value
    
    # LINEAR ALGEBRA
    def interpolant(self, other, alpha):
        """
        Interpolates this object with another, producing a new object
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered. The resulting value is::
            
            alpha*self+(1-alpha)*other 
        
        according to the rules of addition and scalar multiplication.
        
        :param other: object to interpolate with
        :type other:  ``type(self)``
        
        :param alpha: scalar to interpolate by
        :type alpha:  ``int`` or ``float``
        
        :return: the interpolation of this object and ``other`` via ``alpha``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        assert (type(alpha) in [int,float]), "%s is not a number" % repr(alpha)
        return alpha*self+(1-alpha)*other
    
    def interpolate(self, other, alpha):
        """
        Interpolates this object with another in place
        
        This method will modify the attributes of this oject.  The new attributes will
        be equivalent to::
            
            alpha*self+(1-alpha)*other 
        
        according to the rules of addition and scalar multiplication.
        
        This method returns this object for chaining.
        
        :param other: object to interpolate with
        :type other:  ``type(self)``
        
        :param alpha: scalar to interpolate by
        :type alpha:  ``int`` or ``float``
        
        :return: This object, newly modified
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        assert (type(alpha) in [int,float]), "%s is not a number" % repr(alpha)
        self.x = alpha*self.x+(1-alpha)*other.x
        self.y = alpha*self.y+(1-alpha)*other.y
        return self
    
    
    # ADDITIONAL METHODS
    def copy(self):
        """
        :return: A copy of this tuple
        :rtype:  ``type(self)``
        """
        import copy
        return copy.copy(self)
    
    def list(self):
        """
        :return: A python list with the contents of this tuple.
        :rtype:  ``list``
        """
        return [self.x,self.y]
    
    def clamp(self,low,high): 
        """
        Clamps this tuple to the range [``low``, ``high``].
        
        Any value in this tuple less than ``low`` is set to ``low``.  Any value greater 
        than ``high`` is set to ``high``.
        
        This method returns this object for chaining.
        
        :param low: The low range of the clamp
        :type low:  ``int`` or ``float``
        
        :param high: The high range of the clamp
        :type high:  ``int`` or ``float``
        
        :return: This object, newly modified
        :rtype:  ``type(self)``
        """
        assert (type(low) in [int,float]), "%s is not a number" % repr(scalar)
        assert (type(high) in [int,float]), "%s is not a number" % repr(scalar)
        self.x = max(low,min(high,self.x))
        self.y = max(low,min(high,self.y))
        return self


@total_ordering
class Tuple3(object):
    """
    An instance is a tuple in 3D space.
    
    This serves as the base class for both Point3 and Vector3.
    
    :ivar x: The x-coordinate
    :vartype x: ``float``
    
    :ivar y: The y-coordinate
    :vartype y: ``float``
    
    :ivar z: The z-coordinate
    :vartype z: ``float``
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def x(self):
        """
        The x coordinate
        
        **Invariant**: Value must be an ``int`` or  ``float``.
        """
        return self._x
    
    @x.setter
    def x(self, value):
        assert type(value) in [int,float]
        self._x = float(value)
    
    @property
    def y(self):
        """
        The y coordinate
        
        **Invariant**: Value must be an ``int`` or  ``float``.
        """
        return self._y
    
    @y.setter
    def y(self, value):
        assert type(value) in [int,float]
        self._y = float(value)
    
    @property
    def z(self):
        """
        The z coordinate
        
        **Invariant**: Value must be an ``int`` or  ``float``.
        """
        return self._z
    
    @z.setter
    def z(self, value):
        assert type(value) in [int,float]
        self._z = float(value)
    
    
    # OBJECT REPRESENTATION
    def __init__(self, x=0, y=0, z=0):
        """
        Creates a new Tuple3 value (x,y,z).
        
        All values are 0.0 by default.
        
        :return: a new Tuple3 value (x,y,z).
        
        :param x: initial x value
        :type x:  ``int`` or ``float``
        
        :param y: initial y value
        :type y:  ``int`` or ``float``
        
        :param z: initial z value
        :type z:  ``int`` or ``float``
        """
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        """
        :return: A readable string representation of this object. 
        :rtype:  ``bool``
        """
        return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"
    
    def __repr__(self):
        """
        :return: An unambiguous string representation of this object. 
        :rtype:  ``bool``
        """
        return "%s%s" % (self.__class__,self.__str__())
    
    
    # COMPARISON
    def __eq__(self, other):
        """
        Compares this object with ``other`` 
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.  Equivalence also requires type
        equivalence.
        
        :param other: The object to check
        
        :return: True if ``self`` and ``other`` are equivalent
        :rtype:  ``bool``
        """
        import numpy
        return (type(other) == type(self) and numpy.allclose(self.list(),other.list()))
    
    def __ne__(self, other):
        """
        Compares this object with ``other`` 
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.
        
        :param other: The object to check
        
        :return: False if ``self`` and ``other`` are equivalent objects. 
        :rtype:  ``bool``
        """
        return not self == other
    
    def __lt__(self,other):
        """
        Compares the lexicographic ordering of ``self`` and ``other``.
        
        Lexicographic ordering checks the x-coordinate first, and then y.
        
        :param other: The object to check
        :type other:  ``type(self)``
        
        :return: True if ``self`` is lexicographic kess than ``other``
        :rtype:  ``float``
        """
        assert isinstance(other, type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        import numpy
        if self.x == other.x:
            if self.y == other.y:
                return self.z < other.z
            else:
                return self.y < other.y
        return self.x < other.x
    
    def under(self,other):
        """
        Compares ``self`` to ``other`` under the domination partial order
        
        We say that one point or vector dominates  another is all components of the 
        first are greater than or equal to the components of the second.  This is a
        partial order, not a total one.
        
        :param other: The object to check
        :type other:  ``type(self)``
        
        :return: True if ``other`` dominates ``self``; False otherwise
        :rtype:  ``bool``
        """
        assert isinstance(other, type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        return self.x <= other.x and self.y <= other.y and self.z <= other.z
    
    def over(self,other):
        """
        Compares ``self`` to ``other`` under the domination partial order
        
        We say that one point or vector dominates  another is all components of the 
        first are greater than or equal to the components of the second.  This is a
        partial order, not a total one.
        
        :param other: The object to check
        :type other:  ``type(self)``
        
        :return: True if ``self`` dominates ``other``; False otherwise
        :rtype:  ``bool``
        """
        assert isinstance(other, type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        return self.x >= other.x and self.y >= other.y and self.z >= other.z
    
    def __bool__(self):
        """
        Computes the boolean value of this tuple.
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.
        
        :return: True if this object is 'close enough' to the origin; False otherwise
        :rtype:  ``bool``
        """
        return not self.isZero()
    
    def isZero(self):
        """
        Determines whether or not this object is 'close enough' to the origin.
        
        This method uses ``numpy`` to test whether the coordinates are  "close enough".  
        It does not require exact equality for floats.
        
        :return: True if this object is 'close enough' to the origin; False otherwise
        :rtype:  ``bool``
        """
        import numpy
        return numpy.allclose([self.x,self.y,self.z],[0,0,0])
    
    
    # ARITHMETIC
    def __neg__(self):
        """
        Negates this tuple, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :return: the negation of this tuple
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = -result.x
        result.y = -result.y
        result.z = -result.z
        return result
    
    def __pos__(self):
        """
        Positivizes this tuple, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :return: a copy of this tuple
        :rtype:  ``type(self)``
        """
        return self.copy()
    
    def __abs__(self): 
        """
        Creates a copy where each component of this tuple is its absolute value.
        
        :return: the absolute value of this tuple
        :rtype:  ``type(self)``
        """
        self.x = abs(self.x)
        self.y = abs(self.y)
        self.z = abs(self.z)
        return self
    
    def __add__(self, other):
        """
        Adds the odject to another, producing a new object
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param other: object to add
        :type other:  ``type(self)``
        
        :return: the sum of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x += other.x
        result.y += other.y
        result.z += other.z
        return result
    
    def __iadd__(self, other):
        """
        Adds ``other`` to this object in place.
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param other: tuple value to add
        :type other:  ``type(self)``
        
        :return: This object, newly modified
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __sub__(self, other):
        """
        Subtracts ``other`` from this object, producing a new object.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param other: object to subtract
        :type other:  ``type(self)``
        
        :return: the difference of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x -= other.x
        result.y -= other.y
        result.z -= other.z
        return result
    
    def __isub__(self, other):
        """
        Subtracts ``other`` from this object in place
        
        This method will modify the attributes of this oject.  This method returns this
        object for chaining.
        
        :param other: object to subtract
        :type other:  ``type(self)``
        
        :return: This object, newly modified
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    
    def _imul_scalar_(self,scalar):
        """
        Multiplies this object by a scalar in place
        
        :param scalar: scalar to multiply by
        :type scalar:  ``int`` or ``float``
        """
        assert type(scalar) in [int,float], "%s is not a number" % repr(scalar)
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
    
    def _imul_tuple_(self,object):
        """
        Multiplies this object by another Tuple in place
        
        :param object: the tuple multiply by
        :type object:  ``type(self)``
        """
        assert isinstance(object,Tuple3), "%s is not a 2d tuple" % repr(object)
        self.x *= object.x
        self.y *= object.y
        self.z *= object.z
    
    def _imul_matrix_(self,matrix):
        """
        Transforms this object by a matrix in place
        
        :param matrix: matrix to transform with
        :type matrix:  :class:`Matrix`
        """
        from .matrix import Matrix
        import numpy as np
        assert isinstance(matrix,Matrix), "%s is not a matrix" % repr(matrix)
        b = np.array([self.x,self.y,self.z,1], dtype=np.float32)
        tmp = np.dot(matrix._data,b)
        self.x = float(tmp[0])
        self.y = float(tmp[1])
        self.z = float(tmp[2])
    
    def __mul__(self, value):
        """
        Multiples this object by a scalar, Tuple3, or a matrix, producing a new object.
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar multiplication.  If it is a 3d tuple, then the
        result is pointwise multiplication. Finally, if is a matrix, then we use the
        matrix to transform the object.  We treat matrix transformation as multiplication
        orn the right to make in-place multiplication easier.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class.
        
        :param value: value to multiply by
        :type value:  ``int``, ``float``, :class:`Tuple2` or :class:`Matrix`
        
        :return: the altered object
        :rtype:  ``type(self)``
        """
        from .matrix import Matrix
        result = self.copy()
        if type(value) in [int,float]:
            result._imul_scalar_(value)
        elif isinstance(value,Tuple3):
            result._imul_tuple_(value)
        elif isinstance(value,Matrix):
            result._imul_matrix_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return result
    
    def __imul__(self, value):
        """
        Multiples this object by a scalar, Tuple3, or a matrix in place
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar multiplication.  If it is a 3d tuple, then the
        result is pointwise multiplication. Finally, if is a matrix, then we use the
        matrix to transform the object.  We treat matrix transformation as multiplication
        orn the right to make in-place multiplication easier.
        
        This method will modify the attributes of this oject.  This method returns this
        object for chaining.
        
        :param value: value to multiply by
        :type value:  ``int``, ``float``, or :class:`Matrix`
        
        :return: This object, newly modified
        """
        from .matrix import Matrix
        if type(value) in [int,float]:
            self._imul_scalar_(value)
        elif isinstance(value,Tuple3):
            self._imul_tuple_(value)
        elif isinstance(value,Matrix):
            self._imul_matrix_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return self
    
    def __rmul__(self, value):
        """
        Multiplies this object by a scalar or Tuple3 on the left.
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar multiplication.  If it is a 3d tuple, then the
        result is pointwise multiplication.  We do not allow matrix multiplication on 
        the left. 
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance 
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param value: The value to multiply by
        :type value:  ``int``, ``float``, or ``Tuple3``
        
        :return: the scalar multiple of ``self`` and ``scalar``
        :rtype:  ``type(self)``
        """
        return self.__mul__(value)
    
    def _idiv_scalar_(self,scalar):
        """
        Divides this object by a scalar in place
        
        :param scalar: scalar to multiply by
        :type scalar:  ``int`` or ``float``
        """
        assert type(scalar) in [int,float], "%s is not a number" % repr(scalar)
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
    
    def _idiv_tuple_(self,object):
        """
        Divides this object by another tuple in place
        
        :param object: the tuple multiply by
        :type object:  ``type(self)``
        """
        assert isinstance(object,Tuple3), "%s is not a 2d tuple" % repr(object)
        self.x /= object.x
        self.y /= object.y
        self.z /= object.z
    
    def __truediv__(self, value):
        """
        Divides this object by a scalar or a tuple on the right, producting a new object.
        
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar division.  If it is a 3d tuple, then the
        result is pointwise division.
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered.
        
        :param value: The value to multiply by
        :type value:  ``int``, ``float``, or ``Tuple3``
        
        :return: the division of ``self`` by ``value``
        :rtype:  ``type(self)``
        """
        result = self.copy()
        if type(value) in [int,float]:
            result._idiv_scalar_(value)
        elif isinstance(value,Tuple3):
            result._idiv_tuple_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return result
    
    def __itruediv__(self, value):
        """
        Divides this object by a scalar or a tuple on the right in place
         
        The exact effect is determined by the type of value. If ``value`` is a scalar, 
        the result is standard scalar division.  If it is a 2d tuple, then the
        result is pointwise division.
       
        This method will modify the attributes of this oject.  This method returns this
        object for chaining.
        
        :param value: The value to multiply by
        :type value:  ``int``, ``float``, or ``Tuple2``
        
        :return: This object, newly modified
        """
        if type(value) in [int,float]:
            self._idiv_scalar_(value)
        elif isinstance(value,Tuple3):
            self._idiv_tuple_(value)
        else:
            assert False, "%s is not a valid value" % repr(value)
        
        return self
    
    def __rtruediv__(self, value):
        """
        Divides a scalar or tuple by this object.
        
        Dividing by a tuple means pointwise reciprocation, followed by multiplication.
        
        :param value: The value to divide
        :type value:  ``int``, ``float``, or ``Tuple3``
        
        :return: the division of ``value`` by ``self``
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = 1/result.x
        result.y = 1/result.y
        result.z = 1/result.z
        return result * value
    
    # LINEAR ALGEBRA
    def interpolant(self, other, alpha):
        """
        Interpolates this object with another, producing a new object
        
        The value returned has the same type as ``self`` (so if ``self`` is an instance
        of a subclass, it uses that object instead of the original class. The contents of 
        this object are not altered. The resulting value is::
            
            alpha*self+(1-alpha)*other 
        
        according to the rules of addition and scalar multiplication.
        
        :param other: tuple value to interpolate with
        :type other:  ``type(self)``
        
        :param alpha: scalar to interpolate by
        :type alpha:  ``int`` or ``float``
        
        :return: the interpolation of this object and ``other`` via ``alpha``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        assert (type(alpha) in [int,float]), "%s is not a number" % repr(alpha)
        return alpha*self+(1-alpha)*other
    
    def interpolate(self, other, alpha):
        """
        Interpolates this object with another in place
        
        This method will modify the attributes of this oject.  The new attributes will
        be equivalent to::
            
            alpha*self+(1-alpha)*other 
        
        according to the rules of addition and scalar multiplication.
        
        This method returns this object for chaining.
        
        :param other: tuple value to interpolate with
        :type other:  ``type(self)``
        
        :param alpha: scalar to interpolate by
        :type alpha:  ``int`` or ``float``
        
        :return: This object, newly modified
        """
        assert isinstance(other,type(self)), "%s is not of type %s" % (repr(other), repr(type(self)))
        assert (type(alpha) in [int,float]), "%s is not a number" % repr(alpha)
        self.x = alpha*self.x+(1-alpha)*other.x
        self.y = alpha*self.y+(1-alpha)*other.y
        self.z = alpha*self.z+(1-alpha)*other.z
        return self
    
    
    # ADDITIONAL METHODS
    def copy(self):
        """
        :return: A copy of this tuple
        :rtype:  ``type(self)``
        """
        import copy
        return copy.copy(self)
    
    def list(self):
        """
        :return: A python list with the contents of this tuple.
        :rtype:  ``list``
        """
        return [self.x,self.y,self.z]
    
    def clamp(self,low,high): 
        """
        Clamps this tuple to the range [``low``, ``high``].
        
        Any value in this tuple less than ``low`` is set to ``low``.  Any value greater 
        than ``high`` is set to ``high``.
        
        This method returns this object for chaining.
        
        :param low: The low range of the clamp
        :type low:  ``int`` or ``float``
        
        :param high: The high range of the clamp
        :type high:  ``int`` or ``float``
        
        :return: This object, newly modified
        :rtype:  ``type(self)``
        """
        assert (type(low) in [int,float]), "%s is not a number" % repr(scalar)
        assert (type(high) in [int,float]), "%s is not a number" % repr(scalar)
        self.x = max(low,min(high,self.x))
        self.y = max(low,min(high,self.y))
        self.z = max(low,min(high,self.z))
        return self

