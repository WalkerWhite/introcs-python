"""
Classes for representing matrices.

We assume that all matrices at 4x4 matrices, allowing us to represent affine transforms
on homogeneous coordinates.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
import numpy as np


class Matrix(object):
    """
    An instance is a homongenous matrices for graphics transforms.
    
    This class is backed by numpy for fast computation.  There are no publicly accessible 
    attributes, as it is not safe to access the internals.
    """
    
    def __init__(self):
        """
        Creates a new 4x4 identify matrix
        """
        self._data = np.identity(4, dtype=np.float32)
    
    @classmethod
    def CreateTranslation(cls,x=0,y=0,z=0):
        """
        Creates a translation matrix for the given offset.
        
        :param x: x-coordinate of translation (default 0)
        :type x:  ``int`` or ``float``
        
        :param y: y-coordinate of translation (default 0)
        :type y:  ``int`` or ``float``
        
        :param z: z-coordinate of translation (default 0)
        :type z:  ``int`` or ``float``
        """
        result = cls()
        result.translate(x,y,z)
        return result
    
    @classmethod
    def CreateRotation(cls,ang=0,x=0,y=0,z=1):
        """
        Creates a rotation about the given axis.
        
        The rotation angle is given in degrees, not radians. Rotation is counterclockwise 
        around the angle of rotation.  The z-axis is the default axis of rotation.
        
        :param angle: angle of rotation in degrees (default 0)
        :type angle:  ``int`` or ``float``
        
        :param x: x-coordinate of rotation axis (default 0)
        :type x:  ``int`` or ``float``
        
        :param y: y-coordinate of rotation axis (default 0)
        :type y:  ``int`` or ``float``
        
        :param z: z-coordinate of rotation axis (default 1)
        :type z:  ``int`` or ``float``
        """
        result = cls()
        result.rotate(ang,x,y,z)
        return result
    
    @classmethod
    def CreateScale(cls,x=1,y=1,z=1):
        """
        Scales this matrix (in-place) by the given amount
        
        :param x: x-coordinate of the scale (default 1)
        :type x:  ``int`` or ``float``
        
        :param y: y-coordinate of the scale (default 1)
        :type Y:  ``int`` or ``float``
        
        :param z: z-coordinate of the scale (default 1)
        :type Z:  ``int`` or ``float``
        """
        result = cls()
        result.scale(x,y,z)
        return result
    
    def __str__(self):
        """
        :return: A readable string representation of this matrix.
        :rtype:  ``str``
        """
        return str(self._data)
    
    def __repr__(self):
        """
        :return: An unambiguous string representation of this point.
        :rtype:  ``str``
        """
        return str(self.__class__)+str(self)
    
    def __mul__(self,other):
        """
        Premultiplies this matrix by ``other``.
        
        This operation pre-multiplies the matrix on the right.  As a result, this allows 
        us to read graphics operations left to right (which is more natural). This 
        method does not modify this matrix.
        
        :param other: the matrix to pre-multiply
        :type other:  :class:`GMatrix`
        
        :return: The result of premultiplying this matrix by ``other``
        :rtype:  ``Matrix``
        """
        m = Matrix()
        np.dot(other._data,self._data,m._data)
        return m
    
    def __imul__(self,other):
        """
        Premultiplies this matrix by ``other`` in place.
        
        This operation pre-multiplies the matrix on the right.  As a result, this allows
        us to read graphics operations left to right (which is more natural).
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :return: This object, newly modified
        """
        tmp = np.dot(other._data,self._data)
        np.copyto(self._data,tmp)
        return self
    
    def copy(self):
        """
        :return: a copy of this matrix
        :rtype:  ``Matrix``
        """
        m = Matrix()
        np.copyto(m._data,self._data)
        return m
    
    def inverse(self):
        """
        :return: the inverse of this matrix
        :rtype:  :class:`GMatrix`
        """
        m = Matrix()
        np.copyto(m._data,np.linalg.inv(self._data))
        return m
    
    def invert(self):
        """
        Inverts this matrix in place.
        
        This method returns this object for chaining.
        
        :return: This object, newly modified
        """
        np.copyto(self._data,np.linalg.inv(self._data))
        return self
    
    def transpose(self):
        """
        :return: the transpose of this matrix
        :rtype:  ``Matrix``
        """
        m = Matrix()
        np.copyto(m._data,np.transpose(self._data))
        return m
    
    def translate(self,x=0,y=0,z=0):
        """
        Translates this matrix (in-place) by the given amount.
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param x: x-coordinate of translation (default 0)
        :type x:  ``int`` or ``float``
        
        :param y: y-coordinate of translation (default 0)
        :type y:  ``int`` or ``float``
        
        :param z: z-coordinate of translation (default 0)
        :type z:  ``int`` or ``float``
        
        :return: This object, newly modified
        """
        r = np.identity(4, dtype=np.float32)
        r[0,3] = x
        r[1,3] = y
        r[2,3] = z
        tmp = np.dot(self._data,r)
        np.copyto(self._data,tmp)
        return self
    
    def rotate(self,ang=0,x=0,y=0,z=1):
        """
        Rotates this matrix (in place) about the given axis
        
        The rotation angle is given in degrees, not radians. Rotation is counterclockwise 
        around the angle of rotation.  The z-axis is the default axis of rotation.
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param angle: angle of rotation in degrees (default 0)
        :type angle:  ``int`` or ``float``
        
        :param x: x-coordinate of rotation axis (default 0)
        :type x:  ``int`` or ``float``
        
        :param y: y-coordinate of rotation axis (default 0)
        :type y:  ``int`` or ``float``
        
        :param z: z-coordinate of rotation axis (default 1)
        :type z:  ``int`` or ``float``
        
        :return: This object, newly modified
        """
        # Formula taken from https://en.wikipedia.org/wiki/Rotation_matrix
        c = np.cos(np.radians(ang))
        s = np.sin(np.radians(ang))
        f = 1-c
        r = np.identity(4, dtype=np.float32)
        r[0] = [x*x*f+c,   x*y*f-z*s, x*z*f+y*s, 0]
        r[1] = [y*x*f+z*s, y*y*f+c,   y*z*f-x*s, 0]
        r[2] = [z*x*f-y*s, z*y*f+x*s, z*z*f+c,   0]
        tmp = np.dot(self._data,r)
        np.copyto(self._data,tmp)
        return self
    
    def scale(self,x=1,y=1,z=1):
        """
        Scales this matrix (in-place) by the given amount
        
        This method will modify the attributes of this oject. This method returns this
        object for chaining.
        
        :param x: x-coordinate of the scale (default 1)
        :type x:  ``int`` or ``float``
        
        :param y: y-coordinate of the scale (default 1)
        :type Y:  ``int`` or ``float``
        
        :param z: z-coordinate of the scale (default 1)
        :type Z:  ``int`` or ``float``
        
        :return: This object, newly modified
        """
        s = np.identity(4, dtype=np.float32)
        s[0,0] = x
        s[1,1] = y
        s[2,2] = z
        tmp = np.dot(self._data,s)
        np.copyto(self._data,tmp)
        return self
    
    def _transform(self,x=0,y=0,z=0):
        """
        Transforms the given point by this matrix.
        
        The value returned is a 3-element tuple of floats.
        
        :param x: x-coordinate to transform (default 0)
        :type x:  ``int`` or ``float``
        
        :param y: y-coordinate to transform (default 0)
        :type y:  ``int`` or ``float``
        
        :param z: z-coordinate to transform (default 0)
        :type z:  ``int`` or ``float``
        
        :return: The point (x,y,z) transformed by this matrix
        :rtype:  ``tuple``
        """
        b = np.array([x,y,z,1], dtype=np.float32)
        tmp = np.dot(self._data,b)
        return map(float,tuple(tmp[:-1]))
    
    def transform(self,value):
        """
        Transforms the given point or vector by this matrix.
        
        Value can be a point or vector of any dimenion.  This includes :class:`Point2`,
        :class:`Point3`, :class:`Vector2`, and :class:`Vector3`.  The value returned
        will have the same type as ``value``.
        
        :param value: the object to transform
        :type value:  point or vector
        
        :return: The value  transformed by this matrix
        :rtype:  ``type(value)``
        
        """
        from .tuple import Tuple2, Tuple3
        if isinstance(value,Tuple2):
            b = np.array([value.x,value.y,0,1], dtype=np.float32)
            tmp = np.dot(self._data,b)
            return type(value)(float(tmp[0]),float(tmp[1]))
        elif isinstance(value,Tuple3):
            b = np.array([value.x,value.y,value.z,1], dtype=np.float32)
            tmp = np.dot(self._data,b)
            return type(value)(float(tmp[0]),float(tmp[1]),float(tmp[2]))
        
        assert False, '%s is not a point or vector' % repr(value)
