"""
A drawing window

This module replaces the singleton turtle window with a more general class, so that we
can support multiple windows.  

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
import turtle  # The TKinter version


# Private class.  Not publicly available. Emulates the Screen singleton.
class _Window(turtle.TurtleScreen):
    """
    This is an nternal private class to emulate the Screen singleton
    
    :ivar _root: Reference to the turtle screen root
    
    :ivar _canvas:  Reference to the internal drawing canvas
    
    :ivar _title:   Reference to the window title bar
    """
    
    # Copy of turtle.Screen, as non-singleton
    def __init__(self,x=100,y=100,width=800,height=800):
        """
        Creates a copy of turtle.Screen, as a non-singleton
        
        :return: a copy of turtle.Screen, as a non-singleton
        
        :param x: initial x coordinate (default 0)
        :type x:  ``int`` >= 0
        
        :param y: initial y coordinate (default 0)
        :type y:  ``int`` >= 0
        
        :param width: initial window width (default 800)
        :type width:  ``int`` > 0
        
        :param height: initial window height (default 800)
        :type height:  ``int`` > 0
        """
        self._title = turtle._CFG["title"]
        self._root = turtle._Root()
        self._root.title(self._title)
        self._root.ondestroy(self._destroy)
        
        canvwidth  = turtle._CFG["canvwidth"]
        canvheight = turtle._CFG["canvheight"]
        self._root.setupcanvas(width, height, canvwidth, canvheight)
        self._canvas = self._root._getcanvas()
        
        turtle.TurtleScreen.__init__(self, self._canvas)
        self._setup(x,y,width, height)
    
    
    def _setup(self, startx=turtle._CFG["leftright"], starty=turtle._CFG["topbottom"],
                     width=turtle._CFG["width"], height=turtle._CFG["height"]):
        """
        Sets the size and position of the main window.
        
        :param startx: initial x coordinate (default 0)
        :type startx:  ``int`` >= 0
        
        :param starty: initial y coordinate (default 0)
        :type starty:  ``int`` >= 0
        
        :param width: initial window width (default 800)
        :type width:  ``int`` > 0
        
        :param height: initial window height (default 800)
        :type height:  ``int`` > 0
        
        All parameters are optional."""
        if not hasattr(self._root, "set_geometry"):
            return
        
        sw = self._root.win_width()
        sh = self._root.win_height()
        if isinstance(width, float) and 0 <= width <= 1:
            width = sw*width
        if startx is None:
            startx = (sw - width) / 2
        if isinstance(height, float) and 0 <= height <= 1:
            height = sh*height
        if starty is None:
            starty = (sh - height) / 2
        self._root.set_geometry(width, height, startx, starty)
        self.update()
    
    def _destroy(self):
        """
        Destroys this window and its associated assets
        """
        root = self._root
        turtle.Turtle._pen = None
        turtle.Turtle._screen = None
        self._root = None
        self._canvas = None
        turtle.TurtleScreen._RUNNING = True
        root.destroy()


class Window(object):
    """
    An instance is a GUI windows that support turtle graphics
    
    You should construct a ``Window`` object before constructing a 
    :class:``Turtle`` or :class:``Pen``.  You should only need one ``Window`` object
    at any given time.
    
    :ivar x: The x coordinate for top left corner of window
    :vartype x: ``int`` >= 0
    
    :ivar y: The y coordinate for top left corner of window
    :vartype y: ``int`` >= 0
    
    :ivar width: The width of the window in pixels
    :vartype width: ``int`` > 0
    
    :ivar height: The height of the window in pixels
    :vartype height: ``int`` > 0
    
    :ivar title: The title displayed at top of window bar
    :vartype title: ``str``
    
    :ivar resizable: Whether or not the Window supports user resizing
    :vartype resizable: ``bool``
    
    :ivar refresh: How often to refresh the screen when drawing the turtle
    :vartype refresh: ``int`` >= 0
    
    :ivar turtles: The tuple of all turtles attached to this Window
    :vartype turtles: ``tuple``
    
    :ivar pens: The tuple of all pens attached to this Window
    :vartype pens: ``tuple``
    """
    
    # PRIVATE ATTRIBUTES:
    #    _frame: The backing store for this window
    
    # MUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x coordinate for top left corner of window
        
        **invariant**: x must be an ``int`` >= 0
        """
        return self._x
    
    @x.setter
    def x(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0), "%s is negative" % repr(value)
        self._x = value
        self._reshape()
    
    @property
    def y(self):
        """
        The y coordinate for top left corner of window
        
        **invariant**: y must be an ``int`` >= 0
        """
        return self._y
    
    @y.setter
    def y(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0), "%s is negative" % repr(value)
        self._y = value
        self._reshape()
    
    @property
    def width(self):
        """
        The width of the window in pixels
        
        **invariant**: width must be an ``int`` > 0
        """
        return self._width
    
    @width.setter
    def width(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value > 0), "%s is not positive" % repr(value)
        self._width = value
        self._reshape()
    
    @property
    def height(self):
        """
        The height of the window in pixels
        
        **invariant**: height must be an ``int`` > 0
        """
        return self._height
    
    @height.setter
    def height(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value > 0), "%s is not positive" % repr(value)
        self._height = value
        self._reshape()
    
    @property
    def title(self):
        """
        The title displayed at top of window bar
        
        **invariant**: title must be a ``str``
        """
        return self._frame._title
    
    @title.setter
    def title(self,value):
        assert (type(value) == str), "%s is not a string" % repr(value)
        self._frame._root.title(value)
        self._frame._title = value
    
    @property
    def resizable(self):
        """
        Whether or not the Window supports user resizing
        
        **invariant**: resizable must be a ``bool``
        """
        return self._frame._root.resizable() == '1 1'
    
    @resizable.setter
    def resizable(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._resizable = value
        flag = 1 if value else 0
        self._frame._root.resizable(flag, flag)
    
    @property
    def refresh(self):
        """
        How often to refresh the screen when drawing the turtle
        
        **invariant**: refresh must be an ``int`` >= 0
        """
        return self._refresh
    
    @refresh.setter
    def refresh(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0), "%s is negative" % repr(value)
        self._refresh = value
        self._frame.tracer(value,0)
    
    # IMMUTABLE PROPERTIES
    @property
    def turtles(self):
        """
        The tuple of all turtles attached to this Window
        
        *This attribute may not be altered directly*
        """
        return tuple(self._turtles)

    @property
    def pens(self):
        """
        The tuple of all pens attached to this Window
        
        *This attribute may not be altered directly*
        """
        return tuple(self._pencils)
    
    # UNUSED PROPERTIES
    @property 
    def scale(self):
        """
        The amount to scale the window, when put to page
        
        This attribute is ignored in the TKinter version of the Turtle.
        
        **invariant**: scale must be a float > 0"""
        return 1
    
    @property 
    def scale(self):
        """
        Whether Window has been used since last marking
        
        This attribute is ignored in the TKinter version of the Turtle.
        
        **invariant**: Value is a ``bool``
        """
        raise NotImplementedError('mark is not implemented in the Tkinter version')
    
    
    # BUILT-IN METHODS
    def __init__(self,x=100,y=100,width=800,height=800, scale=1):
        """
        Creates a new Window to support turtle graphics
        
        :param x: initial x coordinate (default 100)
        :type x: ``int`` >= 0
        
        :param y: initial y coordinate (default 100)
        :type y: ``int`` >= 0
        
        :param width: initial window width (default 800)
        :type width: ``int`` > 0
        
        :param height: initial window height (default 800)
        :type height: ``int`` > 0
        
        :param scale: initial window scale (INGORED)
        :type scale:  ``float`` > 0
        """
        assert (type(x) == int), "x-coordinate %s is not an int" % repr(x)
        assert (x > 0), "x-coordinate %s is negative" % repr(x)
        assert (type(y) == int), "y-coordinate %s is not an int" % repr(y)
        assert (y > 0), "y-coordinate %s is negative" % repr(y)
        assert (type(width) == int), "width %s is not an int" % repr(width)
        assert (width > 0), "width %s is negative" % repr(width)
        assert (type(height) == int), "height %s is not an int" % repr(height)
        assert (height > 0), "height %s is negative" % repr(height)
        
        self._frame = _Window(x,y,width,height)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.refresh = 1
        
        # Initialize the lists
        self._turtles = []
        self._pencils = []
    
    def __del__(self):
        """
        Destroys this window and its associated assets
        """
        try:
            self._frame._destroy()
        except:
            pass
        self._turtles = []
        self._pencils = []
        del self._frame
    
    # FRIEND METHODS
    def _reshape(self):
        """
        Resizex this window to the current set dimensions
        """
        self._frame._setup(width=self._width,height=self._height,
                           startx=self._x,starty=self._y)
    
    def _addTurtle(self,turt):
        """
        Adds a turtle to this window.
        
        :param turt: the graphics turtle
        :type turt:  ``Turtle``
        """
        from .turtle import Turtle
        assert (type(turt) == Turtle), "%s is not a valid Turtle object" % repr(turt)
        assert turt not in self._turtles, "%s is already a member of thiw Window" % repr(turt)
        self._turtles.append(turt)
    
    def _addPen(self,pen):
        """
        Adds a pen to this window.
        
        :param pen: the graphics pen
        :type pen:  ``Pen``
        """
        from .pen import Pen
        assert (type(pen) == Pen), "%s is not a valid graphics pen" % repr(pen)
        assert pen not in self._pencils, "%s is already a member of thiw Window" % repr(pen)
        self._pencils.append(pen)
    
    def _removeTurtle(self,turt):
        """
        Removes a turtle from this window.
        
        :param turt: the graphics turtle
        :type turt:  ``Turtle``
        """
        if turt in self._turtles:
            self._turtles.remove(turt)
    
    def _removePen(self,pen):
        """
        Removes a pen from this window.
        
        :param pen: the graphics pen
        :type pen:  ``Pen``
        """
        if pen in self._pencils:
            self._pencils.remove(pen)
    
    
    # PUBLIC METHODS
    def clear(self):
        """
        Erases the contents of this Window
        
        All Turtles and Pens are eliminated from the Window. Any attempt to use a 
        previously created :class:`Turtle` or :class:`Pen` will fail.
        """
        self._frame.clear()
        self._turtles = []
        self._gpens = []

    def bye(self):
        """
        Closes the graphics Window, deleting all assets.
        """
        self._frame._destroy()
        self._turtles = []
        self._gpens = []
        del self._frame

    def beep(self):
        """
        Plays an OS specific alert sound
        """
        self._frame._root.bell()

    def iconify(self):
        """
        Shrinks the window down to an icon, effectively hiding it
        """
        self._frame._root.iconify()

    def deiconify(self):
        """
        Expands the window from an icon so that it is visible
        """
        self._frame._root.deiconify()

    def setMaxSize(self,width,height):
        """
        Sets the maximum size for this window
        
        Any attempt to resize a dimension beyond the maximum size will fail.
        
        :param width: the maximum window width
        :type width: ``int`` > 0
        
        :param height: the maximum height width
        :type height: ``int`` > 0
        """
        assert (type(width) == int), "width %s is not an int" % repr(width)
        assert (width > 0), "width %s is negative" % repr(width)
        assert (type(height) == int), "height %s is not an int" % repr(height)
        assert (height > 0), "height %s is negative" % repr(height)
        self._frame._root.maxsize(width,height)

    def setMinSize(self,width,height):
        """
        Sets the minimum size for this window
        
        Any attempt to resize a dimension below the minimum size will fail.
        
        :param width: the maximum window width
        :type width: ``int`` > 0
        
        :param height: the maximum height width
        :type height: ``int`` > 0
        """
        assert (type(width) == int), "width %s is not an int" % repr(width)
        assert (width > 0), "width %s is negative" % repr(width)
        assert (type(height) == int), "height %s is not an int" % repr(height)
        assert (height > 0), "height %s is negative" % repr(height)
        self._frame._root.minsize(width,height)
    
    # UNSUPPORTED METHODS
    def flush(self):
        """
        Unsupported method for compatibility
        """
        pass
    
    def stroke(self, path, clr):
        """
        Unsupported method for compatibility
        """
        pass
    
    def fill(self, path, clr):
        """
        Unsupported method for compatibility
        """
        pass
    
    def write(self, fname):
        """
        Unsupported method for compatibility
        """
        pass


# TURTLE HELPERS
def is_valid_color(c):
    """
    Determines if ``c`` is a valid color for a Turtle or Pen.
    
    Turtles accept RGB, HSV, strings (for named colors), or tuples.
    
    :param c: a potential color value
    
    :return: True if c is a valid color value.
    :rtype:  ``bool``
    """
    from ..colors import RGB, HSV
    return type(c) in [RGB, HSV, str, tuple]


def to_valid_color(c):
    """
    Converts a color to the appropriate TKinter representation.
    
    This method allows us to support all color formats, while using a single
    color format for the backend.
    
    For the PyX backend, the unified color is a Tk-supported color value
    
    :param c: the color value
    :type c:  valid color
    
    :return: The given color value, converted to an internal format
    :rtype:  ``str`` or ``tuple``
    """
    from ..colors import RGB, HSV
    return c.tkColor() if (type(c) == RGB or type(c) == HSV) else c

