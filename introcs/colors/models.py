"""
Classes for three different color models.

The classes are RGB, CMYK, HSV, representing the most popular color models.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


def nearclamp(value,floor,ceil, epsilon=1e-13):
    """
    Returns a clamped value if it is within espilson of the range.
    
    If value is more than epsilon less than floor or epsilon greater than ceil, nothing
    happens.  Otherwise, the value is clamped to within [floor,ceil]
    
    :return: a clamped value if it is within espilson of the range
    :rtype:  ``int`` or ``float``
    
    :param value: The value to clamp
    :type value:  ``int`` or ``float``
    
    :param floor: The minimum of the range (or None if -infinity)
    :type floor:  ``int``, ``float``, or ``None``
    
    :param ceil: The maximum of the range (or None if infinity)
    :type ceil:  ``int``, ``float``, or ``None``
    
    :param epsilon: The margin of error
    :type epsilon:  ``int`` or ``float``
    """
    if not ceil is None and (value > ceil):
        value = min(value,ceil) if value < ceil+epsilon else value
    if  not floor is None and (value < floor):
        value = max(value,floor) if value > floor-epsilon else value
    return value


class RGB(object):
    """
    An instance is a RGB color value.
    
    All color value ranges are inclusive.  So 255 is a valid red value, but 256 is not.
    
    :ivar red: The red channel
    :vartype red: ``int`` 0..255
    
    :ivar green: The green channel
    :vartype green: ``int`` 0..255
    
    :ivar blue: The blue channel
    :vartype blue: ``int`` 0..255
    
    :ivar alpha: The alpha channel
    :vartype alpha: ``int`` 0..255
    """
    # MUTABLE ATTRIBUTES
    @property
    def red(self):
        """
        The red channel.
        
        **invariant**: Value must be an int between 0 and 255, inclusive.
        """
        return self._red
    
    @red.setter
    def red(self, value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 and value <= 255), "%s is outside of range [0,255]" % repr(value)
        self._red = value
    
    @property
    def green(self):
        """
        The green channel.
        
        **invariant**: Value must be an int between 0 and 255, inclusive.
        """
        return self._green
    
    @green.setter
    def green(self, value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 and value <= 255), "%s is outside of range [0,255]" % repr(value)
        self._green = value
    
    @property
    def blue(self):
        """
        The blue channel.
        
        **invariant**: Value must be an int between 0 and 255, inclusive.
        """
        return self._blue
    
    @blue.setter
    def blue(self, value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 and value <= 255), "%s is outside of range [0,255]" % repr(value)
        self._blue = value
    
    @property
    def alpha(self):
        """
        The alpha channel.
        
        Used for transparency effects (but not in this course).
        
        **invariant**: Value must be an int between 0 and 255, inclusive.
        """
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 and value <= 255), "%s is outside of range [0,255]" % repr(value)
        self._alpha = value
    
    # BUILT-IN METHODS
    def __init__(self, r, g, b, a=255):
        """
        Creates a new RGB value (r,g,b,a).
        
        All color value ranges are inclusive.  So 255 is a valid red value, but 256 is not.
        
        :return: a new RGB value (r,g,b,a).
        
        :param r: initial red value
        :type r:  ``int` 0..255
        
        :param g: initial green value
        :type g:  ``int` 0..255
        
        :param b: initial blue value
        :type b:  ``int` 0..255
        
        :param a: initial alpha value (default 255)
        :type a:  ``int` 0..255
        """        
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
    
    def __eq__(self, other):
        """
        :return: True if self and ``other`` are equivalent RGB colors. 
        :rtype:  ``bool``
        
        :param other: The object to check
        """
        return (type(other) == RGB and self.red == other.red and 
                self.green == other.green and self.blue == other.blue and
                self.alpha == other.alpha)
    
    def __ne__(self, other):
        """
        :return: True if self and ``other`` are not equivalent RGB colors. 
        :rtype:  ``bool``
        
        :param other: The object to check
        """
        return (type(other) != RGB or self.red != other.red or 
                self.green != other.green or self.blue != other.blue or
                self.alpha != other.alpha)
    
    def __str__(self):
        """
        :return: A readable string representation of this color. 
        :rtype:  ``bool``
        """
        return "("+str(self.red)+","+str(self.green)+","+str(self.blue)+","+str(self.alpha)+")"
    
    def __repr__(self):
        """
        :return: An unambiguous String representation of this color. 
        :rtype:  ``bool``
        """
        return "(red="+str(self.red)+",green="+str(self.green)+",blue="+str(self.blue)+",alpha="+str(self.alpha)+")"
    
    
    # PUBLIC METHODS
    def glColor(self):
        """
        Returns an OpenGL version of this color.
        
        This conversion allows this object to be used by graphics libraries that depend
        on OpenGL (e.g. Kivy)
        
        :return: a 4 element list of the attributes in the range 0 to 1
        :rtype:  ``list``
        """
        return [self.red/255.0, self.green/255.0, self.blue/255.0, self.alpha/255.0]
    
    def tkColor(self):
        """
        Returns an Tkinter version of this color.
        
        This conversion allows this object to be used by graphics libraries that depend
        on Tkinter (e.g. the drawing turtle).
        
        :return: a 3 element list of the attributes in the range 0 to 1
        :rtype:  ``tuple``
        """
        return (self.red/255.0, self.green/255.0, self.blue/255.0)
    
    # CLASS METHODS FOR TKinter SUPPORT
    @classmethod
    def CreateName(cls,name):
        """
        Creates a new RGB object with the given color name.
        
        Color name conversion is handled by the standard RGB color space.  If the color
        is not valid, this method will fire an assert.
        
        :param name: the color name
        :type name:  ``str``
        
        :raise: ``ValueError`` if ``name`` is not a valid color name.
        
        :return: a new RGB value
        """
        from .tkcolor import is_tkcolor, tk_webcolor
        assert type(name) == str, "%s is not a string" % repr(name)
        if not is_tkcolor(name):
            raise ValueError("%s is not a valid color name" % repr(name))
        return cls.CreateWebColor(tk_webcolor(name))
    
    @classmethod
    def CreateWebColor(cls,color):
        """
        Creates a new RGB object from the given web color string.
        
        A web color string is a 6-digit hexadecimal string starting with a hashtag (#).  
        It does not include an alpha value. If the string is not , this method will
        fire an assert.
        
        :param color: the web color
        :type color:  hexadecimal ``str``
        
        :return: a new RGB value
        """
        assert type(color) == str, "%s is not a string" % repr(color)
        assert color[0] == '#' and len(color) == 7, "% is not a valid web color" % repr(color)
        try:
            red = int(color[1:3],16)
        except:
            assert false, "red value %s is out of range" % repr(color[1:3])
        try:
            green = int(color[3:5],16)
        except:
            assert false, "green value %s is out of range" % repr(color[3:5])
        try:
            blue = int(color[5:7],16)
        except:
            assert false, "green value %s is out of range" % repr(color[5:7])
        
        return cls(red,green,blue)


class CMYK(object):
    """
    An instance is a CMYK color value.
    
    All color value ranges are inclusive.  So 100.0 is a valid cyan value, but 100.001 
    is not.
    
    :ivar cyan: The cyan channel
    :vartype cyan: ``float`` 0..100
    
    :ivar magenta: The magenta channel
    :vartype magenta: ``float`` 0..100
    
    :ivar yellow: The yellow channel
    :vartype yellow: ``float`` 0..100
    
    :ivar black: The black channel
    :vartype black: ``float`` 0..100
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def cyan(self):
        """
        The cyan channel.
        
        **invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._cyan
    
    @cyan.setter
    def cyan(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._cyan = float(value)
    
    @property
    def magenta(self):
        """
        The magenta channel.
        
        **invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._magenta
    
    @magenta.setter
    def magenta(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._magenta = float(value)
    
    @property
    def yellow(self):
        """
        The yellow channel.
        
        **invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._yellow
    
    @yellow.setter
    def yellow(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._yellow = float(value)
    
    @property
    def black(self):
        """
        The black channel.
        
        **invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._black
    
    @black.setter
    def black(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._black = float(value)
    
    # BUILT-IN METHODS
    def __init__(self, c, m, y, k):
        """
        Creates a new CMYK color (c,m,y,k).
        
        All color value ranges are inclusive.  So 100.0 is a valid cyan value, but 100.001 
        is not.
    
        :return: a new CMYK value (c,m,y,k).
        
        :param c: initial cyan value
        :type c:  ``float`` 0.0..100.0
        
        :param m: initial magenta value
        :type m:  ``float`` 0.0..100.0
        
        :param y: initial yellow value
        :type y:  ``float`` 0.0..100.0
        
        :param k: initial black value
        :type k:  ``float`` 0.0..100.0
        """
        self.cyan = c
        self.magenta = m
        self.yellow = y
        self.black = k
    
    def __eq__(self, other):
        """
        :return: True if self and ``other`` are equivalent CMYK colors. 
        :rtype:  ``bool``
        
        :param other: The object to check
        """
        return (type(other) == CMYK and self.cyan == other.cyan and 
                self.magenta == other.magenta and self.yellow == other.yellow and
                self.black == other.black)   
    
    def __ne__(self, other):
        """
        :return: True if self and ``other`` are not equivalent CMYK colors. 
        :rtype:  ``bool``
        
        :param other: The object to check
        """
        return (type(other) != CMYK or self.cyan != other.cyan or 
                self.magenta != other.magenta or self.yellow != other.yellow or
                self.black != other.black)
    
    def __str__(self):
        """
        :return: A readable string representation of this color. 
        :rtype:  ``bool``
        """
        return "("+str(self.cyan)+","+str(self.magenta)+","+str(self.yellow)+","+str(self.black)+")"
    
    def __repr__(self):
        """
        :return: An unambiguou string representation of this color. 
        :rtype:  ``bool``
        """
        return "(cyan="+str(self.cyan)+",magenta="+str(self.magenta)+",yellow="+str(self.yellow)+",black="+str(self.black)+")"


class HSV(object):
    """
    An instance is a HSV color value.
    
    The ``hue`` range is not inclusive on the high end.  So 359.99999 is a valid hue, but
    360.0 is not.  All other color values are inclusive.
    
    :ivar hue: The hue channel
    :vartype hue: ``float`` 0.0..360.0, not including 360.0
    
    :ivar saturation: The saturation channel
    :vartype saturation: ``float`` 0.0..1.0
    
    :ivar value: The value channel
    :vartype value: ``float`` 0.0..1.0
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def hue(self):
        """
        The hue channel.
        
        **invariant**: Value must be a float between 0.0 and 360.0, not including 360.0.
        """
        return self._hue
    
    @hue.setter
    def hue(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = nearclamp(value,0.0,None)
        assert (value >= 0.0 and value < 360.0), "value %s is outside of range [0.0,360.0)" % repr(value)
        self._hue = float(value)
    
    @property
    def saturation(self):
        """
        The staturation channel.
        
        **invariant**: Value must be a float between 0.0 and 1.0, inclusive.
        """
        return self._saturation
    
    @saturation.setter
    def saturation(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = nearclamp(value,0.0,1.0)
        assert (value >= 0.0 and value <= 1.0), "value %s is outside of range [0.0,1.0]" % repr(value)
        self._saturation = float(value)
    
    @property
    def value(self):
        """
        The value channel.
        
        **invariant**: Value must be a float between 0.0 and 1.0, inclusive.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = nearclamp(value,0.0,1.0)
        assert (value >= 0.0 and value <= 1.0), "value %s is outside of range [0.0,1.0]" % repr(val)
        self._value = float(value)
    
    # BUILT-IN METHODS
    def __init__(self, h, s, v):
        """
        Creates a new HSV color (h,s,v).
        
        The ``hue`` range is not inclusive on the high end.  So 359.99999 is a valid hue, 
        but 360.0 is not.  All other color values are inclusive.
        
        :return: a new HSV color (h,s,v).
        
        :param h: the initial hue
        :type h: ``float`` 0.0..360.0, not including 360.0
        
        :param s: the initial saturation 
        :type s:  ``float`` 0.0..1.0
        
        :param v: the initial value
        :type v:  ``float`` 0.0..1.0
        """
        self.hue = h
        self.saturation = s
        self.value = v
    
    def __eq__(self, other):
        """
        :return: True if self and ``other`` are equivalent HSV colors. 
        :rtype:  ``bool``
        
        :param other: The object to check
        """
        return (type(other) == HSV and self.hue == other.hue and 
                self.saturation == other.saturation and self.value == other.value)
    
    def __ne__(self, other):
        """
        :return: True if self and ``other`` are not equivalent HSV colors. 
        :rtype:  ``bool``
        
        :param other: The object to check
        """
        return (type(other) != HSV or self.hue != other.hue or 
                self.saturation != other.saturation or self.value != other.value)
    
    def __str__(self):
        """
        :return: A readable string representation of this color. 
        :rtype:  ``bool``
        """
        return "("+str(self.hue)+","+str(self.saturation)+","+str(self.value)+")"
    
    def __repr__(self):
        """
        :return: An unambiguous string representation of this color. 
        :rtype:  ``bool``
        """
        return "(hue="+str(self.hue)+",saturation="+str(self.saturation)+",value="+str(self.value)+")"
    
    
    # PUBLIC METHODS
    def glColor(self):
        """
        Returns an OpenGL version of this color.
        
        This conversion allows this object to be used by graphics libraries that depend
        on OpenGL (e.g. Kivy).  The conversion first converts this object to the RGB
        color space.
        
        :return: a 4 element list of the attributes in the range 0 to 1
        :rtype:  ``list``
        """
        import colorsys
        rgb = colorsys.hsv_to_rgb(self.hue/360.0,self.saturation,self.value)
        return [rgb[0], rgb[1], rgb[2], 1.0]
    
    def tkColor(self):
        """
        Returns an Tkinter version of this color.
        
        This conversion allows this object to be used by graphics libraries that depend
        on Tkinter (e.g. the drawing turtle). The conversion first converts this object 
        to the RGB color space.
        
        :return: a 3 element list of the attributes in the range 0 to 1
        :rtype:  ``tuple``
        """
        import colorsys
        return colorsys.hsv_to_rgb(self.hue/360.0,self.saturation,self.value)

