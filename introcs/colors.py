"""
Classes for three different color models.

The classes are RGB, CMYK, HSV, representing the most popular color models. In addition,
we support string parsing for the TKinter color space.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""


def _nearclamp(value,floor,ceil, epsilon=1e-13):
    """
    Returns a clamped value if it is within espilson of the range. [INTERNAL FUNCTION]
    
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
    """
    # MUTABLE ATTRIBUTES
    @property
    def red(self):
        """
        The red channel.
        
        **Invariant**: Value must be an int between 0 and 255, inclusive.
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
        
        **Invariant**: Value must be an int between 0 and 255, inclusive.
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
        
        **Invariant**: Value must be an int between 0 and 255, inclusive.
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
        
        This value is used for transparency effects (but not always supported).
        
        **Invariant**: Value must be an int between 0 and 255, inclusive.
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
        :param r: initial red value
        :type r:  ``int`` 0..255
        
        :param g: initial green value
        :type g:  ``int`` 0..255
        
        :param b: initial blue value
        :type b:  ``int`` 0..255
        
        :param a: initial alpha value (default 255)
        :type a:  ``int`` 0..255
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
        Converts this color to an OpenGL value.
        
        This conversion allows this object to be used by graphics libraries that depend
        on OpenGL (e.g. Kivy)
        
        :return: a 4 element list of the attributes in the range 0 to 1
        :rtype:  ``list``
        """
        return [self.red/255.0, self.green/255.0, self.blue/255.0, self.alpha/255.0]
    
    def rgba(self):
        """
        Converts this color to an rgba value.
        
        This conversion allows this object to be used by graphics libraries that want
        integer color representation like PIL
        
        :return: a 4 element tuple of the attributes in the range 0 to 255
        :rtype:  ``tuple``
        """
        return (self.red, self.green, self.blue, self.alpha)
    
    def webColor(self):
        """
        Converts this color to a web color string.
        
        This conversion allows this object to be used by graphics libraries that depend
        on Tkinter (e.g. the drawing turtle).  The color will not contain alpha (nor will
        it premulitply any existing alpha) and will be a string in web form.
        
        :return: a string representing a web color
        :rtype:  ``str``
        """
        return '#%02x%02x%02x' % (self.red,self.green,self.blue)
    
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
        assert color[0] == '#' and len(color) == 7, "%s is not a valid web color" % repr(color)
        try:
            red = int(color[1:3],16)
        except:
            assert False, "red value %s is out of range" % repr(color[1:3])
        try:
            green = int(color[3:5],16)
        except:
            assert False, "green value %s is out of range" % repr(color[3:5])
        try:
            blue = int(color[5:7],16)
        except:
            assert False, "green value %s is out of range" % repr(color[5:7])
        
        return cls(red,green,blue)


class CMYK(object):
    """
    An instance is a CMYK color value.
    
    All color value ranges are inclusive.  So 100.0 is a valid cyan value, but 100.001 
    is not.
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def cyan(self):
        """
        The cyan channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._cyan
    
    @cyan.setter
    def cyan(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = _nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._cyan = float(value)
    
    @property
    def magenta(self):
        """
        The magenta channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._magenta
    
    @magenta.setter
    def magenta(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = _nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._magenta = float(value)
    
    @property
    def yellow(self):
        """
        The yellow channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._yellow
    
    @yellow.setter
    def yellow(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = _nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._yellow = float(value)
    
    @property
    def black(self):
        """
        The black channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive.
        """
        return self._black
    
    @black.setter
    def black(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = _nearclamp(value,0.0,100.0)
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % repr(value)
        self._black = float(value)
    
    # BUILT-IN METHODS
    def __init__(self, c, m, y, k):
        """
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
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def hue(self):
        """
        The hue channel.
        
        **Invariant**: Value must be a float between 0.0 and 360.0, not including 360.0.
        """
        return self._hue
    
    @hue.setter
    def hue(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = _nearclamp(value,0.0,None)
        assert (value >= 0.0 and value < 360.0), "value %s is outside of range [0.0,360.0)" % repr(value)
        self._hue = float(value)
    
    @property
    def saturation(self):
        """
        The staturation channel.
        
        **Invariant**: Value must be a float between 0.0 and 1.0, inclusive.
        """
        return self._saturation
    
    @saturation.setter
    def saturation(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = _nearclamp(value,0.0,1.0)
        assert (value >= 0.0 and value <= 1.0), "value %s is outside of range [0.0,1.0]" % repr(value)
        self._saturation = float(value)
    
    @property
    def value(self):
        """
        The value channel.
        
        **Invariant**: Value must be a float between 0.0 and 1.0, inclusive.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % repr(value)
        value = _nearclamp(value,0.0,1.0)
        assert (value >= 0.0 and value <= 1.0), "value %s is outside of range [0.0,1.0]" % repr(value)
        self._value = float(value)
    
    # BUILT-IN METHODS
    def __init__(self, h, s, v):
        """
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
        Converts thie color to an OpenGL value.
        
        This conversion allows this object to be used by graphics libraries that depend
        on OpenGL (e.g. Kivy).  The conversion first converts this object to the RGB
        color space.
        
        :return: a 4 element list of the attributes in the range 0 to 1
        :rtype:  ``list``
        """
        import colorsys
        rgb = colorsys.hsv_to_rgb(self.hue/360.0,self.saturation,self.value)
        return [rgb[0], rgb[1], rgb[2], 1.0]
    
    def rgba(self):
        """
        Converts this color to an rgba value.
        
        This conversion allows this object to be used by graphics libraries that want
        integer color representation like PIL. The conversion first converts this object 
        to the RGB color space.
        
        :return: a 4 element tuple of the attributes in the range 0 to 255
        :rtype:  ``tuple``
        """
        import colorsys
        rgb = colorsys.hsv_to_rgb(self.hue/360.0,self.saturation,self.value)
        return (int(round(rgb[0]*255)), int(round(rgb[1]*255)), int(round(rgb[2]*255)), 255)
    
    def webColor(self):
        """
        Converts this color to a web color string.
        
        This conversion allows this object to be used by graphics libraries that depend
        on Tkinter (e.g. the drawing turtle). The conversion first converts this object 
        to the RGB color space.
        
        :return: a string representing a web color
        :rtype:  ``str``
        """
        import colorsys
        rgb = colorsys.hsv_to_rgb(self.hue/360.0,self.saturation,self.value)
        rgb = tuple(map(lambda x : int(round(x*255)),rgb))
        return '#%02x%02x%02x' % rgb


# We removed the constants from earlier versions because all objects are mutable
# Support for webcolors and Tkinter names makes this less important.

# UTILITY FUNCTIONS
def is_tkcolor(name):
    """
    Checks if ``name`` is a valid TKinter color
    
    :param name: the color name
    :type name:  ``str``
    
    :return: True if name is the name of a supported color
    :rtype:  ``bool``
    """
    return name in TK_COLOR_MAP


def is_webcolor(name):
    """
    Checks if ``name`` is a valid web color
    
    :param name: the color value
    :type name:  ``str``
    
    :return: True if name is a valid web color
    :rtype:  ``bool``
    """
    if color[0] != '#' or len(color) == 7:
        return False
    try:
        red = int(color[1:3],16)
        green = int(color[3:5],16)
        blue = int(color[5:7],16)
        return True
    except:
        pass
    return False

def tk_webcolor(name):
    """
    Returns the web color equivalent of a TKinter color
    
    If ``name`` is not a valid TKinter color, this returns the code for White.
    
    :param name: the color name
    :type name:  ``str``
    
    :return: the web color equivalent of ``name``
    :rtype:  ``str``
    """
    try:
        return TK_COLOR_MAP[name]
    except:
        return '#FFFFFF'


# Unfortunately, this had to be done manually.
TK_COLOR_MAP = {
    'alice blue': '#F0F8FF',
    'AliceBlue' : '#F0F8FF',
    'antique white': '#FAEBD7',
    'AntiqueWhite': '#FAEBD7',
    'AntiqueWhite1': '#FFEFDB',
    'AntiqueWhite2': '#EEDFCC',
    'AntiqueWhite3': '#CDC0B0',
    'AntiqueWhite4': '#8B8378',
    'aquamarine': '#7FFFD4',
    'aquamarine1': '#7FFFD4',
    'aquamarine2': '#76EEC6',
    'aquamarine3': '#66CDAA',
    'aquamarine4': '#458B74',
    'azure': '#F0FFFF',
    'azure1': '#F0FFFF',
    'azure2': '#E0EEEE',
    'azure3': '#C1CDCD',
    'azure4': '#838B8B',
    'beige': '#F5F5DC',
    'bisque': '#FFE4C4',
    'bisque1': '#FFE4C4',
    'bisque2': '#EED5B7',
    'bisque3': '#CDB79E',
    'bisque4': '#8B7D6B',
    'black': '#000000',
    'blanched almond': '#FFEBCD',
    'BlanchedAlmond': '#FFEBCD',
    'blue': '#0000FF',
    'blue violet': '#8A2BE2',
    'blue1': '#0000FF',
    'blue2': '#0000EE',
    'blue3': '#0000CD',
    'blue4': '#00008B',
    'BlueViolet': '#8A2BE2',
    'brown': '#A52A2A',
    'brown1': '#FF4040',
    'brown2': '#EE3B3B',
    'brown3': '#CD3333',
    'brown4': '#8B2323',
    'burlywood': '#DEB887',
    'burlywood1': '#FFD39B',
    'burlywood2': '#EEC591',
    'burlywood3': '#CDAA7D',
    'burlywood4': '#8B7355',
    'cadet blue': '#5F9EA0',
    'CadetBlue': '#5F9EA0',
    'CadetBlue1': '#98F5FF',
    'CadetBlue2': '#8EE5EE',
    'CadetBlue3': '#7AC5CD',
    'CadetBlue4': '#53868B',
    'chartreuse': '#7FFF00',
    'chartreuse1': '#7FFF00',
    'chartreuse2': '#76EE00',
    'chartreuse3': '#66CD00',
    'chartreuse4': '#458B00',
    'chocolate': '#D2691E',
    'chocolate1': '#FF7F24',
    'chocolate2': '#EE7621',
    'chocolate3': '#CD661D',
    'chocolate4': '#8B4513',
    'coral': '#FF7F50',
    'coral1': '#FF7256',
    'coral2': '#EE6A50',
    'coral3': '#CD5B45',
    'coral4': '#8B3E2F',
    'cornflower blue': '#6495ED',
    'CornflowerBlue': '#6495ED',
    'cornsilk': '#FFF8DC',
    'cornsilk1': '#FFF8DC',
    'cornsilk2': '#EEE8CD',
    'cornsilk3': '#CDC8B1',
    'cornsilk4': '#8B8878',
    'cyan': '#00FFFF',
    'cyan1': '#00FFFF',
    'cyan2': '#00EEEE',
    'cyan3': '#00CDCD',
    'cyan4': '#008B8B',
    'dark blue': '#00008B',
    'dark cyan': '#008B8B',
    'dark goldenrod': '#B8860B',
    'dark gray': '#A9A9A9',
    'dark green': '#006400',
    'dark grey': '#A9A9A9',
    'dark khaki': '#BDB76B',
    'dark magenta': '#8B008B',
    'dark olive green': '#556B2F',
    'dark orange': '#FF8C00',
    'dark orchid': '#9932CC',
    'dark red': '#8B0000',
    'dark salmon': '#E9967A',
    'dark sea green': '#8FBC8F',
    'dark slate blue': '#483D8B',
    'dark slate gray': '#2F4F4F',
    'dark slate grey': '#2F4F4F',
    'dark turquoise': '#00CED1',
    'dark violet': '#9400D3',
    'DarkBlue': '#00008B',
    'DarkCyan': '#008B8B',
    'DarkGoldenrod': '#B8860B',
    'DarkGoldenrod1': '#FFB90F',
    'DarkGoldenrod2': '#EEAD0E',
    'DarkGoldenrod3': '#CD950C',
    'DarkGoldenrod4': '#8B6508',
    'DarkGray': '#A9A9A9',
    'DarkGreen': '#006400',
    'DarkGrey': '#A9A9A9',
    'DarkKhaki': '#BDB76B',
    'DarkMagenta': '#8B008B',
    'DarkOliveGreen': '#556B2F',
    'DarkOliveGreen1': '#CAFF70',
    'DarkOliveGreen2': '#BCEE68',
    'DarkOliveGreen3': '#A2CD5A',
    'DarkOliveGreen4': '#6E8B3D',
    'DarkOrange': '#FF8C00',
    'DarkOrange1': '#FF7F00',
    'DarkOrange2': '#EE7600',
    'DarkOrange3': '#CD6600',
    'DarkOrange4': '#8B4500',
    'DarkOrchid': '#9932CC',
    'DarkOrchid1': '#BF3EFF',
    'DarkOrchid2': '#B23AEE',
    'DarkOrchid3': '#9A32CD',
    'DarkOrchid4': '#68228B',
    'DarkRed': '#8B0000',
    'DarkSalmon': '#E9967A',
    'DarkSeaGreen': '#8FBC8F',
    'DarkSeaGreen1': '#C1FFC1',
    'DarkSeaGreen2': '#B4EEB4',
    'DarkSeaGreen3': '#9BCD9B',
    'DarkSeaGreen4': '#698B69',
    'DarkSlateBlue': '#483D8B',
    'DarkSlateGray': '#2F4F4F',
    'DarkSlateGray1': '#97FFFF',
    'DarkSlateGray2': '#8DEEEE',
    'DarkSlateGray3': '#79CDCD',
    'DarkSlateGray4': '#528B8B',
    'DarkSlateGrey': '#2F4F4F',
    'DarkTurquoise': '#00CED1',
    'DarkViolet': '#9400D3',
    'deep pink': '#FF1493',
    'deep sky blue': '#00BFFF',
    'DeepPink': '#FF1493',
    'DeepPink1': '#FF1493',
    'DeepPink2': '#EE1289',
    'DeepPink3': '#CD1076',
    'DeepPink4': '#8B0A50',
    'DeepSkyBlue': '#00BFFF',
    'DeepSkyBlue1': '#00BFFF',
    'DeepSkyBlue2': '#00B2EE',
    'DeepSkyBlue3': '#009ACD',
    'DeepSkyBlue4': '#00688B',
    'dim gray': '#696969',
    'dim grey': '#696969',
    'DimGray': '#696969',
    'DimGrey': '#696969',
    'dodger blue': '#1E90FF',
    'DodgerBlue': '#1E90FF',
    'DodgerBlue1': '#1E90FF',
    'DodgerBlue2': '#1C86EE',
    'DodgerBlue3': '#1874CD',
    'DodgerBlue4': '#104E8B',
    'firebrick': '#B22222',
    'firebrick1': '#FF3030',
    'firebrick2': '#EE2C2C',
    'firebrick3': '#CD2626',
    'firebrick4': '#8B1A1A',
    'floral white': '#FFFAF0',
    'FloralWhite': '#FFFAF0',
    'forest green': '#228B22',
    'ForestGreen': '#228B22',
    'gainsboro': '#DCDCDC',
    'ghost white': '#F8F8FF',
    'GhostWhite': '#F8F8FF',
    'gold': '#FFD700',
    'gold1': '#FFD700',
    'gold2': '#EEC900',
    'gold3': '#CDAD00',
    'gold4': '#8B7500',
    'goldenrod': '#DAA520',
    'goldenrod1': '#FFC125',
    'goldenrod2': '#EEB422',
    'goldenrod3': '#CD9B1D',
    'goldenrod4': '#8B6914',
    'gray': '#BEBEBE',
    'gray0': '#000000',
    'gray1': '#030303',
    'gray2': '#050505',
    'gray3': '#080808',
    'gray4': '#0A0A0A',
    'gray5': '#0D0D0D',
    'gray6': '#0F0F0F',
    'gray7': '#121212',
    'gray8': '#141414',
    'gray9': '#171717',
    'gray10': '#1A1A1A',
    'gray11': '#1C1C1C',
    'gray12': '#1F1F1F',
    'gray13': '#212121',
    'gray14': '#242424',
    'gray15': '#262626',
    'gray16': '#292929',
    'gray17': '#2B2B2B',
    'gray18': '#2E2E2E',
    'gray19': '#303030',
    'gray20': '#333333',
    'gray21': '#363636',
    'gray22': '#383838',
    'gray23': '#3B3B3B',
    'gray24': '#3D3D3D',
    'gray25': '#404040',
    'gray26': '#424242',
    'gray27': '#454545',
    'gray28': '#474747',
    'gray29': '#4A4A4A',
    'gray30': '#4D4D4D',
    'gray31': '#4F4F4F',
    'gray32': '#525252',
    'gray33': '#545454',
    'gray34': '#575757',
    'gray35': '#595959',
    'gray36': '#5C5C5C',
    'gray37': '#5E5E5E',
    'gray38': '#616161',
    'gray39': '#636363',
    'gray40': '#666666',
    'gray41': '#696969',
    'gray42': '#6B6B6B',
    'gray43': '#6E6E6E',
    'gray44': '#707070',
    'gray45': '#737373',
    'gray46': '#757575',
    'gray47': '#787878',
    'gray48': '#7A7A7A',
    'gray49': '#7D7D7D',
    'gray50': '#7F7F7F',
    'gray51': '#828282',
    'gray52': '#858585',
    'gray53': '#878787',
    'gray54': '#8A8A8A',
    'gray55': '#8C8C8C',
    'gray56': '#8F8F8F',
    'gray57': '#919191',
    'gray58': '#949494',
    'gray59': '#969696',
    'gray60': '#999999',
    'gray61': '#9C9C9C',
    'gray62': '#9E9E9E',
    'gray63': '#A1A1A1',
    'gray64': '#A3A3A3',
    'gray65': '#A6A6A6',
    'gray66': '#A8A8A8',
    'gray67': '#ABABAB',
    'gray68': '#ADADAD',
    'gray69': '#B0B0B0',
    'gray70': '#B3B3B3',
    'gray71': '#B5B5B5',
    'gray72': '#B8B8B8',
    'gray73': '#BABABA',
    'gray74': '#BDBDBD',
    'gray75': '#BFBFBF',
    'gray76': '#C2C2C2',
    'gray77': '#C4C4C4',
    'gray78': '#C7C7C7',
    'gray79': '#C9C9C9',
    'gray80': '#CCCCCC',
    'gray81': '#CFCFCF',
    'gray82': '#D1D1D1',
    'gray83': '#D4D4D4',
    'gray84': '#D6D6D6',
    'gray85': '#D9D9D9',
    'gray86': '#DBDBDB',
    'gray87': '#DEDEDE',
    'gray88': '#E0E0E0',
    'gray89': '#E3E3E3',
    'gray90': '#E5E5E5',
    'gray91': '#E8E8E8',
    'gray92': '#EBEBEB',
    'gray93': '#EDEDED',
    'gray94': '#F0F0F0',
    'gray95': '#F2F2F2',
    'gray96': '#F5F5F5',
    'gray97': '#F7F7F7',
    'gray98': '#FAFAFA',
    'gray99': '#FCFCFC',
    'gray100': '#FFFFFF',
    'green': '#00FF00',
    'green yellow': '#ADFF2F',
    'green1': '#00FF00',
    'green2': '#00EE00',
    'green3': '#00CD00',
    'green4': '#008B00',
    'GreenYellow': '#ADFF2F',
    'grey': '#BEBEBE',
    'grey0': '#000000',
    'grey1': '#030303',
    'grey2': '#050505',
    'grey3': '#080808',
    'grey4': '#0A0A0A',
    'grey5': '#0D0D0D',
    'grey6': '#0F0F0F',
    'grey7': '#121212',
    'grey8': '#141414',
    'grey9': '#171717',
    'grey10': '#1A1A1A',
    'grey11': '#1C1C1C',
    'grey12': '#1F1F1F',
    'grey13': '#212121',
    'grey14': '#242424',
    'grey15': '#262626',
    'grey16': '#292929',
    'grey17': '#2B2B2B',
    'grey18': '#2E2E2E',
    'grey19': '#303030',
    'grey20': '#333333',
    'grey21': '#363636',
    'grey22': '#383838',
    'grey23': '#3B3B3B',
    'grey24': '#3D3D3D',
    'grey25': '#404040',
    'grey26': '#424242',
    'grey27': '#454545',
    'grey28': '#474747',
    'grey29': '#4A4A4A',
    'grey30': '#4D4D4D',
    'grey31': '#4F4F4F',
    'grey32': '#525252',
    'grey33': '#545454',
    'grey34': '#575757',
    'grey35': '#595959',
    'grey36': '#5C5C5C',
    'grey37': '#5E5E5E',
    'grey38': '#616161',
    'grey39': '#636363',
    'grey40': '#666666',
    'grey41': '#696969',
    'grey42': '#6B6B6B',
    'grey43': '#6E6E6E',
    'grey44': '#707070',
    'grey45': '#737373',
    'grey46': '#757575',
    'grey47': '#787878',
    'grey48': '#7A7A7A',
    'grey49': '#7D7D7D',
    'grey50': '#7F7F7F',
    'grey51': '#828282',
    'grey52': '#858585',
    'grey53': '#878787',
    'grey54': '#8A8A8A',
    'grey55': '#8C8C8C',
    'grey56': '#8F8F8F',
    'grey57': '#919191',
    'grey58': '#949494',
    'grey59': '#969696',
    'grey60': '#999999',
    'grey61': '#9C9C9C',
    'grey62': '#9E9E9E',
    'grey63': '#A1A1A1',
    'grey64': '#A3A3A3',
    'grey65': '#A6A6A6',
    'grey66': '#A8A8A8',
    'grey67': '#ABABAB',
    'grey68': '#ADADAD',
    'grey69': '#B0B0B0',
    'grey70': '#B3B3B3',
    'grey71': '#B5B5B5',
    'grey72': '#B8B8B8',
    'grey73': '#BABABA',
    'grey74': '#BDBDBD',
    'grey75': '#BFBFBF',
    'grey76': '#C2C2C2',
    'grey77': '#C4C4C4',
    'grey78': '#C7C7C7',
    'grey79': '#C9C9C9',
    'grey80': '#CCCCCC',
    'grey81': '#CFCFCF',
    'grey82': '#D1D1D1',
    'grey83': '#D4D4D4',
    'grey84': '#D6D6D6',
    'grey85': '#D9D9D9',
    'grey86': '#DBDBDB',
    'grey87': '#DEDEDE',
    'grey88': '#E0E0E0',
    'grey89': '#E3E3E3',
    'grey90': '#E5E5E5',
    'grey91': '#E8E8E8',
    'grey92': '#EBEBEB',
    'grey93': '#EDEDED',
    'grey94': '#F0F0F0',
    'grey95': '#F2F2F2',
    'grey96': '#F5F5F5',
    'grey97': '#F7F7F7',
    'grey98': '#FAFAFA',
    'grey99': '#FCFCFC',
    'grey100': '#FFFFFF',
    'honeydew': '#F0FFF0',
    'honeydew1': '#F0FFF0',
    'honeydew2': '#E0EEE0',
    'honeydew3': '#C1CDC1',
    'honeydew4': '#838B83',
    'hot pink': '#FF69B4',
    'HotPink': '#FF69B4',
    'HotPink1': '#FF6EB4',
    'HotPink2': '#EE6AA7',
    'HotPink3': '#CD6090',
    'HotPink4': '#8B3A62',
    'indian red': '#CD5C5C',
    'IndianRed': '#CD5C5C',
    'IndianRed1': '#FF6A6A',
    'IndianRed2': '#EE6363',
    'IndianRed3': '#CD5555',
    'IndianRed4': '#8B3A3A',
    'ivory': '#FFFFF0',
    'ivory1': '#FFFFF0',
    'ivory2': '#EEEEE0',
    'ivory3': '#CDCDC1',
    'ivory4': '#8B8B83',
    'khaki': '#F0E68C',
    'khaki1': '#FFF68F',
    'khaki2': '#EEE685',
    'khaki3': '#CDC673',
    'khaki4': '#8B864E',
    'lavender': '#E6E6FA',
    'lavender blush': '#FFF0F5',
    'LavenderBlush': '#FFF0F5',
    'LavenderBlush1': '#FFF0F5',
    'LavenderBlush2': '#EEE0E5',
    'LavenderBlush3': '#CDC1C5',
    'LavenderBlush4': '#8B8386',
    'lawn green': '#7CFC00',
    'LawnGreen': '#7CFC00',
    'lemon chiffon': '#FFFACD',
    'LemonChiffon': '#FFFACD',
    'LemonChiffon1': '#FFFACD',
    'LemonChiffon2': '#EEE9BF',
    'LemonChiffon3': '#CDC9A5',
    'LemonChiffon4': '#8B8970',
    'light blue': '#ADD8E6',
    'light coral': '#F08080',
    'light cyan': '#E0FFFF',
    'light goldenrod': '#EEDD82',
    'light goldenrod yellow': '#FAFAD2',
    'light gray': '#D3D3D3',
    'light green': '#90EE90',
    'light grey': '#D3D3D3',
    'light pink': '#FFB6C1',
    'light salmon': '#FFA07A',
    'light sea green': '#20B2AA',
    'light sky blue': '#87CEFA',
    'light slate blue': '#8470FF',
    'light slate gray': '#778899',
    'light slate grey': '#778899',
    'light steel blue': '#B0C4DE',
    'light yellow': '#FFFFE0',
    'LightBlue': '#ADD8E6',
    'LightBlue1': '#BFEFFF',
    'LightBlue2': '#B2DFEE',
    'LightBlue3': '#9AC0CD',
    'LightBlue4': '#68838B',
    'LightCoral': '#F08080',
    'LightCyan': '#E0FFFF',
    'LightCyan1': '#E0FFFF',
    'LightCyan2': '#D1EEEE',
    'LightCyan3': '#B4CDCD',
    'LightCyan4': '#7A8B8B',
    'LightGoldenrod': '#EEDD82',
    'LightGoldenrod1': '#FFEC8B',
    'LightGoldenrod2': '#EEDC82',
    'LightGoldenrod3': '#CDBE70',
    'LightGoldenrod4': '#8B814C',
    'LightGoldenrodYellow': '#FAFAD2',
    'LightGray': '#D3D3D3',
    'LightGreen': '#90EE90',
    'LightGrey': '#D3D3D3',
    'LightPink': '#FFB6C1',
    'LightPink1': '#FFAEB9',
    'LightPink2': '#EEA2AD',
    'LightPink3': '#CD8C95',
    'LightPink4': '#8B5F65',
    'LightSalmon': '#FFA07A',
    'LightSalmon1': '#FFA07A',
    'LightSalmon2': '#EE9572',
    'LightSalmon3': '#CD8162',
    'LightSalmon4': '#8B5742',
    'LightSeaGreen': '#20B2AA',
    'LightSkyBlue': '#87CEFA',
    'LightSkyBlue1': '#B0E2FF',
    'LightSkyBlue2': '#A4D3EE',
    'LightSkyBlue3': '#8DB6CD',
    'LightSkyBlue4': '#607B8B',
    'LightSlateBlue': '#8470FF',
    'LightSlateGray': '#778899',
    'LightSlateGrey': '#778899',
    'LightSteelBlue': '#B0C4DE',
    'LightSteelBlue1': '#CAE1FF',
    'LightSteelBlue2': '#BCD2EE',
    'LightSteelBlue3': '#A2B5CD',
    'LightSteelBlue4': '#6E7B8B',
    'LightYellow': '#FFFFE0',
    'LightYellow1': '#FFFFE0',
    'LightYellow2': '#EEEED1',
    'LightYellow3': '#CDCDB4',
    'LightYellow4': '#8B8B7A',
    'lime green': '#32CD32',
    'LimeGreen': '#32CD32',
    'linen': '#FAF0E6',
    'magenta': '#FF00FF',
    'magenta1': '#FF00FF',
    'magenta2': '#EE00EE',
    'magenta3': '#CD00CD',
    'magenta4': '#8B008B',
    'maroon': '#B03060',
    'maroon1': '#FF34B3',
    'maroon2': '#EE30A7',
    'maroon3': '#CD2990',
    'maroon4': '#8B1C62',
    'medium aquamarine': '#66CDAA',
    'medium blue': '#0000CD',
    'medium orchid': '#BA55D3',
    'medium purple': '#9370DB',
    'medium sea green': '#3CB371',
    'medium slate blue': '#7B68EE',
    'medium spring green': '#00FA9A',
    'medium turquoise': '#48D1CC',
    'medium violet red': '#C71585',
    'MediumAquamarine': '#66CDAA',
    'MediumBlue': '#0000CD',
    'MediumOrchid': '#BA55D3',
    'MediumOrchid1': '#E066FF',
    'MediumOrchid2': '#D15FEE',
    'MediumOrchid3': '#B452CD',
    'MediumOrchid4': '#7A378B',
    'MediumPurple': '#9370DB',
    'MediumPurple1': '#AB82FF',
    'MediumPurple2': '#9F79EE',
    'MediumPurple3': '#8968CD',
    'MediumPurple4': '#5D478B',
    'MediumSeaGreen': '#3CB371',
    'MediumSlateBlue': '#7B68EE',
    'MediumSpringGreen': '#00FA9A',
    'MediumTurquoise': '#48D1CC',
    'MediumVioletRed': '#C71585',
    'midnight blue': '#191970',
    'MidnightBlue': '#191970',
    'mint cream': '#F5FFFA',
    'MintCream': '#F5FFFA',
    'misty rose': '#FFE4E1',
    'MistyRose': '#FFE4E1',
    'MistyRose1': '#FFE4E1',
    'MistyRose2': '#EED5D2',
    'MistyRose3': '#CDB7B5',
    'MistyRose4': '#8B7D7B',
    'moccasin': '#FFE4B5',
    'navajo white': '#FFDEAD',
    'NavajoWhite': '#FFDEAD',
    'NavajoWhite1': '#FFDEAD',
    'NavajoWhite2': '#EECFA1',
    'NavajoWhite3': '#CDB38B',
    'NavajoWhite4': '#8B795E',
    'navy': '#000080',
    'navy blue': '#000080',
    'NavyBlue': '#000080',
    'old lace': '#FDF5E6',
    'OldLace': '#FDF5E6',
    'olive drab': '#6B8E23',
    'OliveDrab': '#6B8E23',
    'OliveDrab1': '#C0FF3E',
    'OliveDrab2': '#B3EE3A',
    'OliveDrab3': '#9ACD32',
    'OliveDrab4': '#698B22',
    'orange': '#FFA500',
    'orange red': '#FF4500',
    'orange1': '#FFA500',
    'orange2': '#EE9A00',
    'orange3': '#CD8500',
    'orange4': '#8B5A00',
    'OrangeRed': '#FF4500',
    'OrangeRed1': '#FF4500',
    'OrangeRed2': '#EE4000',
    'OrangeRed3': '#CD3700',
    'OrangeRed4': '#8B2500',
    'orchid': '#DA70D6',
    'orchid1': '#FF83FA',
    'orchid2': '#EE7AE9',
    'orchid3': '#CD69C9',
    'orchid4': '#8B4789',
    'pale goldenrod': '#EEE8AA',
    'pale green': '#98FB98',
    'pale turquoise': '#AFEEEE',
    'pale violet red': '#DB7093',
    'PaleGoldenrod': '#EEE8AA',
    'PaleGreen': '#98FB98',
    'PaleGreen1': '#9AFF9A',
    'PaleGreen2': '#90EE90',
    'PaleGreen3': '#7CCD7C',
    'PaleGreen4': '#548B54',
    'PaleTurquoise': '#AFEEEE',
    'PaleTurquoise1': '#BBFFFF',
    'PaleTurquoise2': '#AEEEEE',
    'PaleTurquoise3': '#96CDCD',
    'PaleTurquoise4': '#668B8B',
    'PaleVioletRed': '#DB7093',
    'PaleVioletRed1': '#FF82AB',
    'PaleVioletRed2': '#EE799F',
    'PaleVioletRed3': '#CD687F',
    'PaleVioletRed4': '#8B475D',
    'papaya whip': '#FFEFD5',
    'PapayaWhip': '#FFEFD5',
    'peach puff': '#FFDAB9',
    'PeachPuff': '#FFDAB9',
    'PeachPuff1': '#FFDAB9',
    'PeachPuff2': '#EECBAD',
    'PeachPuff3': '#CDAF95',
    'PeachPuff4': '#8B7765',
    'peru': '#CD853F',
    'pink': '#FFC0CB',
    'pink1': '#FFB5C5',
    'pink2': '#EEA9B8',
    'pink3': '#CD919E',
    'pink4': '#8B636C',
    'plum': '#DDA0DD',
    'plum1': '#FFBBFF',
    'plum2': '#EEAEEE',
    'plum3': '#CD96CD',
    'plum4': '#8B668B',
    'powder blue': '#B0E0E6',
    'PowderBlue': '#B0E0E6',
    'purple': '#A020F0',
    'purple1': '#9B30FF',
    'purple2': '#912CEE',
    'purple3': '#7D26CD',
    'purple4': '#551A8B',
    'red': '#FF0000',
    'red1': '#FF0000',
    'red2': '#EE0000',
    'red3': '#CD0000',
    'red4': '#8B0000',
    'rosy brown': '#BC8F8F',
    'RosyBrown': '#BC8F8F',
    'RosyBrown1': '#FFC1C1',
    'RosyBrown2': '#EEB4B4',
    'RosyBrown3': '#CD9B9B',
    'RosyBrown4': '#8B6969',
    'royal blue': '#4169E1',
    'RoyalBlue': '#4169E1',
    'RoyalBlue1': '#4876FF',
    'RoyalBlue2': '#436EEE',
    'RoyalBlue3': '#3A5FCD',
    'RoyalBlue4': '#27408B',
    'saddle brown': '#8B4513',
    'SaddleBrown': '#8B4513',
    'salmon': '#FA8072',
    'salmon1': '#FF8C69',
    'salmon2': '#EE8262',
    'salmon3': '#CD7054',
    'salmon4': '#8B4C39',
    'sandy brown': '#F4A460',
    'SandyBrown': '#F4A460',
    'sea green': '#2E8B57',
    'SeaGreen': '#2E8B57',
    'SeaGreen1': '#54FF9F',
    'SeaGreen2': '#4EEE94',
    'SeaGreen3': '#43CD80',
    'SeaGreen4': '#2E8B57',
    'seashell': '#FFF5EE',
    'seashell1': '#FFF5EE',
    'seashell2': '#EEE5DE',
    'seashell3': '#CDC5BF',
    'seashell4': '#8B8682',
    'sienna': '#A0522D',
    'sienna1': '#FF8247',
    'sienna2': '#EE7942',
    'sienna3': '#CD6839',
    'sienna4': '#8B4726',
    'sky blue': '#87CEEB',
    'SkyBlue': '#87CEEB',
    'SkyBlue1': '#87CEFF',
    'SkyBlue2': '#7EC0EE',
    'SkyBlue3': '#6CA6CD',
    'SkyBlue4': '#4A708B',
    'slate blue': '#6A5ACD',
    'slate gray': '#708090',
    'slate grey': '#708090',
    'SlateBlue': '#6A5ACD',
    'SlateBlue1': '#836FFF',
    'SlateBlue2': '#7A67EE',
    'SlateBlue3': '#6959CD',
    'SlateBlue4': '#473C8B',
    'SlateGray': '#708090',
    'SlateGray1': '#C6E2FF',
    'SlateGray2': '#B9D3EE',
    'SlateGray3': '#9FB6CD',
    'SlateGray4': '#6C7B8B',
    'SlateGrey': '#708090',
    'snow': '#FFFAFA',
    'snow1': '#FFFAFA',
    'snow2': '#EEE9E9',
    'snow3': '#CDC9C9',
    'snow4': '#8B8989',
    'spring green': '#00FF7F',
    'SpringGreen': '#00FF7F',
    'SpringGreen1': '#00FF7F',
    'SpringGreen2': '#00EE76',
    'SpringGreen3': '#00CD66',
    'SpringGreen4': '#008B45',
    'steel blue': '#4682B4',
    'SteelBlue': '#4682B4',
    'SteelBlue1': '#63B8FF',
    'SteelBlue2': '#5CACEE',
    'SteelBlue3': '#4F94CD',
    'SteelBlue4': '#36648B',
    'tan': '#D2B48C',
    'tan1': '#FFA54F',
    'tan2': '#EE9A49',
    'tan3': '#CD853F',
    'tan4': '#8B5A2B',
    'thistle': '#D8BFD8',
    'thistle1': '#FFE1FF',
    'thistle2': '#EED2EE',
    'thistle3': '#CDB5CD',
    'thistle4': '#8B7B8B',
    'tomato': '#FF6347',
    'tomato1': '#FF6347',
    'tomato2': '#EE5C42',
    'tomato3': '#CD4F39',
    'tomato4': '#8B3626',
    'turquoise': '#40E0D0',
    'turquoise1': '#00F5FF',
    'turquoise2': '#00E5EE',
    'turquoise3': '#00C5CD',
    'turquoise4': '#00868B',
    'violet': '#EE82EE',
    'violet red': '#D02090',
    'VioletRed': '#D02090',
    'VioletRed1': '#FF3E96',
    'VioletRed2': '#EE3A8C',
    'VioletRed3': '#CD3278',
    'VioletRed4': '#8B2252',
    'wheat': '#F5DEB3',
    'wheat1': '#FFE7BA',
    'wheat2': '#EED8AE',
    'wheat3': '#CDBA96',
    'wheat4': '#8B7E66',
    'white': '#FFFFFF',
    'white smoke': '#F5F5F5',
    'WhiteSmoke': '#F5F5F5',
    'yellow': '#FFFF00',
    'yellow green': '#9ACD32',
    'yellow1': '#FFFF00',
    'yellow2': '#EEEE00',
    'yellow3': '#CDCD00',
    'yellow4': '#8B8B00',
    'YellowGreen': '#9ACD32',
}


