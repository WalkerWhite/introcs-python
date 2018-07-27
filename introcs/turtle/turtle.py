"""
The Turtle graphics tool

A graphics turtle is a pen that is controlled by direction and movement. The turtle 
is a cursor that that you control by moving it left, right, forward, or backward.  
As it moves, it draws a line of the same color as  the Turtle.

This is an updated version of the classic Python Turtle that provides better support
for Python 3. It also uses properties which provide better abstractions and protections
for students.

This class is built on the Tkinter canvas object.  That means we were able to add support 
for dashes and stroke width which did not exist in the original turtle.  We also have
proper support for speed 0 (which was always broken in the original turtle). The lack
of an instantaneous turtle has been the number one complaint at grading sessions since 
Cornell switched to Python.

:author:  Walker M. White (wmw2)
:version: July 24, 2018
"""
from ._drawtool import _DrawTool, Cursor
from PIL import Image
import math


class TurtleCursor(Cursor):
    """
    Instance is an image source for a ``Turtle`` cursor.
    
    Naively, this should just be an image file that we load.  However, Tkinter is horrible 
    for image graphics. Images take way too long to draw (one 32x32 image can take up to 
    16 milliseconds -- a full animation frame -- on a MacOS laptop).  And any antialiased
    alpha causes severe artifacts under rotation.
    
    The best solution we have found is for an in-memory image with solid colors vs 
    pure alpha.  To match our drawing tool, we allow for a two-toned image which displays
    both the edge and fill color separately.  Switching colors is done by pixel blitting.
    For a 32x32 image, this is not too bad, and honestly Tkinter is much slower to draw
    the image no matter what we do.
    
    The image is always oriented to the east.
    
    :ivar edge: The edge color
    :vartype edge: ``RGB``, ``HSV`` or ``str``
    
    :ivar fill: The edge color
    :vartype fill: ``RGB``, ``HSV`` or ``str``
    """
    
    def __init__(self,edge,fill):
        """
        Creates a new image source.
        
        :param edge: The edge color
        :type edge:  ``RGB``, ``HSV`` or ``str``
        
        :param fill: The edge color
        :type fill:  ``RGB``, ``HSV`` or ``str``
        """
        from ..geom import Matrix
        
        # Use our matrix class to build a shape out of ovals.
        # BODY
        self._body = Matrix.CreateScale(10,9,1)
        self._body.translate(14,16,0)
        self._body.invert()
        
        # HEAD
        self._head = Matrix.CreateScale(4,4,1)
        self._head.translate(26,16,0)
        self._head.invert()
        
        # TAIL
        #self._tail = Matrix.CreateTranslation(4,16,0)
        self._tail = Matrix.CreateScale(2,2,1)
        self._tail.translate(4,16,0)
        self._tail.invert()
        
        # LEG1
        self._leg1 = Matrix.CreateScale(3,6,1)
        self._leg1.rotate(35)
        self._leg1.translate(19,11,0)
        self._leg1.invert()
        
        # LEG2
        self._leg2 = Matrix.CreateScale(3,6,1)
        self._leg2.rotate(-35)
        self._leg2.translate(19,21,0)
        self._leg2.invert()
        
        # LEG3
        self._leg3 = Matrix.CreateScale(3,6,1)
        self._leg3.rotate(-35)
        self._leg3.translate(9,11,0)
        self._leg3.invert()
        
        # LEG4
        self._leg4 = Matrix.CreateScale(3,6,1)
        self._leg4.rotate(35)
        self._leg4.translate(9,21,0)
        self._leg4.invert()
        super().__init__(edge,fill)
    
    def _alloc(self):
        """
        Allocates the image.
        
        This creates a turtle using ovals.
        """
        from ..geom import Vector2
        data = []
        self._mark = []
        for y in range(32):
            for x in range(32):
                v = Vector2(x,y)
                if self._body.transform(v).length2() <= 1:
                    self._mark.append(2)
                    data.append(self.fill)
                else:
                    good = self._head.transform(v).length2() <= 1
                    good = good or self._tail.transform(v).length2() <= 1
                    good = good or self._leg1.transform(v).length2() <= 1
                    good = good or self._leg2.transform(v).length2() <= 1
                    good = good or self._leg3.transform(v).length2() <= 1
                    good = good or self._leg4.transform(v).length2() <= 1
                    if good:
                        self._mark.append(1)
                        data.append(self.edge)
                    else:
                        self._mark.append(0)
                        data.append((0,0,0,0))
        self._orig = Image.new('RGBA',(32,32))
        self._orig.putdata(data)
        return self._orig


class Turtle(_DrawTool):
    """
    An instance represents a graphics turtle.
    
    The turtle is attached to a window on creation, and this window cannot be changed.
    If the window is closed or deleted, the turtle can no longer be used.  Any attempt
    to call a graphics method after the window is disposed will result in an error.
    """
    # PRIVATE ATTRIBUTES:
    #    _tkkey   : A unique key for Tkinter
    #    _window  : The drawing screen
    
    # Whether or not this tool supports orientation
    _ORIENTS = True
    
    
    # MUTABLE PROPERTIES
    @property
    def heading(self):
        """
        The heading of this turtle in degrees.
        
        Heading is measured counter clockwise from due east.
        
        **Invariant**: Value must be a ``float``
        """
        return self._heading
    
    @heading.setter
    def heading(self,value):
        assert type(value) in [int, float], "%s is not a valid number" % repr(value)
        self._set_orientation(value)
    
    @property
    def speed(self):
        """
        The animation speed of this turtle.
        
        The speed is an integer from 0 to 10. Speeds from 1 to 10 enforce increasingly 
        faster animation of line drawing and cursor updates. Value 1 is the slowest speed 
        while 10 is the fastest speed.  Roughly, speed 1 draws 1 pixel per step, while
        speed 10 draws an entire line in a single step.
        
        Speed 0 is special.  Speed 0 means that no animation takes place at all.  The
        drawing commands will be remembered, but not shown on the screen.  To display
        the drawing, you must call the method :meth:`flush`. When that method is called,
        all of the drawing commands will be displayed instantly.  This is useful for 
        fast drawing.
        
        If the speed is currently 0, changing the speed will immediately flush any
        existing drawing commands.
        
        **Invariant**: Value must be an ``int`` in the range 0..10.
        """
        return self._speed
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 or value <= 10), "%s is outside the range 0..10" % repr(value)
        self._set_speed(value)

    @property
    def color(self):
        """
        The color of this turtle.
        
        All subsequent draw commands (forward/back) draw using this color. If the color 
        changes, it only affects future draw commands, not past ones.
        
        **Invariant**: Value must be either an additive color model (e.g. RGB or HSV) or 
        string representing a color name or a web color (e.g. ``'#f3CC02'``).
        """
        return self._edge
    
    @color.setter
    def color(self,value):
        assert (self._is_valid_color(value)), "%s is not a valid color input" % repr(value)
        self._set_color(value,value)
    
    @property
    def stroke(self):
        """
        The stroke width of this turtle.
        
        By default, the turtle draws lines that are one pixel wide.  Changing this value
        will increase (or decrease, if your implementation supports sub-pixel graphics)
        the stroke width.
        
        **Invariant**: Value must be either a positive ``float``
        """
        return self._width
    
    @stroke.setter
    def stroke(self,value):
        assert type(value) in [int, float], "%s is not a valid number" % repr(value)
        assert value > 0, "%s isnot positive" % repr(value)
        self._width = value
        self._mark = True
    
    @property
    def dash(self):
        """
        The dash pattern of this turtle.
        
        A dash pattern is a tuple of integers that specifes the dash in pixels.  Only
        odd values of the pattern are drawn.  For example, if the pattern is (10,10),
        the turtle will draw 10 pixels, and then stop drawing for 10 pixels.  After 20
        pixels that patterns repeat.  Similarly (10,5,5,10) will draw for 10 pixels, 
        stop for 5 pixels, draw for 10 pixels and the stop for 5 pixels before repeating.
        
        If this value is ``None``, the line will be solid.
        
        **Invariant**: Value must be ``None`` or a non-empty tuple of positive integers.
        """
        return self._dash
    
    @dash.setter
    def dash(self,value):
        if value is None:
            self._dash = None
            self._mark = True
            return
        
        assert type(value) in [tuple,list], '%s is neither a tuple nor a list' % repr(value)
        assert len(value) > 0, '%s is empty' % repr(value)
        assert min(map(lambda x : type(x) == int and x > 0, value)), '%s is not a valid dash pattern' % repr(value)
        self._dash = value
        self._mark = True
    
    @property
    def visible(self):
        """
        Whether the turtle's icon is visible.
        
        Drawing commands will still work while the turtle icon is hidden. There will just 
        be no indication of the turtle's current location on the screen.
        
        **Invariant**: Value must be a ``bool``
        """
        return self._visible
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._set_visible(value)
    
    @property
    def drawmode(self):
        """
        Whether the turtle is in draw mode.
        
        All drawing calls are active if an only if this mode is True
        
        **Invariant**: Value must be a ``bool``
        """
        return self._isdown
    
    @drawmode.setter
    def drawmode(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._isdown = value
        self._mark = True
    
    
    # IMMUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._x
    
    @property
    def y(self):
        """
        The y-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._y
    
    
    # BUILT-IN METHODS
    def __init__(self, screen, position=(0, 0), color='red', heading = 0, speed=10):
        """
        :param screen: window object that turtle will draw on.
        :type screen:  :class:`Window`
        
        :param position: initial turtle position (origin is screen center)
        :type position:  2D ``tuple``
        
        :param color: initial turtle color (default red)
        :type color: ``RGB``, ``HSV`` or ``str``
        
        :param heading: initial turtle directions (default 0)
        :type heading:  ``int`` or ``float``
        
        :param speed: initial turtle speed (default 10)
        :type speed:  ``int`` 0..10
        """
        super().__init__(screen,position,color,color,speed)
        self._heading = heading
        self._isdown = True
        
        self._image = TurtleCursor(color,color)
        self._image.edge = color
        self._image.fill = color
        self._cursor = self._image.read()
    
    def __repr__(self):
        """
        :return: An unambiguous string representation of this turtle. 
        :rtype:  ``bool``
        """
        return str(self.__class__)+str(self)
    
    def __str__(self):
        """
        :return: A readable string representation of this tuple. 
        :rtype:  ``bool``
        """
        return 'Turtle[position={}, color={}, heading={}]'.format((self.x,self.y), self.color, self.heading)
    
    # PUBLIC METHODS
    def forward(self,distance):
        """
        Moves the turtle forward by the given amount.
        
        This method draws a line if :attr:`drawmode` is True.
        
        :param distance: distance to move in pixels
        :type distance:  ``int`` or ``float``
        """
        assert (type(distance) in [int, float]), "%s is not a valid number" % repr(distance)
        # Figure out where we are going
        angle = self._heading*math.pi/180
        x = math.cos(angle)*distance+self._x
        y = math.sin(angle)*distance+self._y
        if self._isdown:
            color = self._to_internal_color(self.color)
            if self._dash:
                self._follow_line((self._x,self._y,x,y),fill=color,width=self._width,dash=self._dash)
            else:
                self._follow_line((self._x,self._y,x,y),fill=color,width=self._width)
        elif self._visible:
            block = self._speed > 0
            self._window._draw_icon(self,self._cursor,x,y,block=block)
        self._x = x
        self._y = y
        self._mark = True
    
    def backward(self,distance):
        """
        Moves the turtle backward by the given amount.
        
        This method draws a line if :attr:`drawmode` is True.
        
        :param distance: distance to move in pixels
        :type distance:  ``int`` or ``float``
        """
        assert (type(distance) in [int, float]), "%s is not a valid number" % repr(distance)
        # Figure out where we are going
        angle = self._heading*math.pi/180
        x = self._x-math.cos(angle)*distance
        y = self._y-math.sin(angle)*distance
        if self._isdown:
            color = self._to_internal_color(self.color)
            if self._dash:
                self._follow_line((self._x,self._y,x,y),fill=color,width=self._width,dash=self._dash)
            else:
                self._follow_line((self._x,self._y,x,y),fill=color,width=self._width)
        elif self._visible:
            block = self._speed > 0
            self._window._draw_icon(self,self._cursor,x,y,block=block)
        self._x = x
        self._y = y
        self._mark = True
    
    def right(self,degrees):
        """
        Turns the turtle to the right by the given amount.
        
        Nothing is drawn when this method is called.
        
        :param degrees: amount to turn right in degrees
        :type degrees:  ``int`` or ``float``
        """
        assert (type(degrees) in [int, float]), "%s is not a valid number" % repr(degrees)
        self._set_orientation(self._heading-degrees)
    
    def left(self,degrees):
        """
        Turns the turtle to the left by the given amount.
        
        Nothing is drawn when this method is called.
        
        :param degrees: amount to turn left in degrees
        :type degrees:  ``int`` or ``float``
        """
        assert (type(degrees) in [int, float]), "%s is not a valid number" % repr(degrees)
        self._set_orientation(self._heading+degrees)
    
    def move(self,x,y):
        """
        Moves the turtle to given position without drawing.
        
        This method does not draw, regardless of the :attr:`drawmode`.
        
        :param x: new x position for turtle
        :type x:  ``int`` or ``float``
        
        :param y: new y position for turtle
        :type y:  ``int`` or ``float``
        """
        assert (type(x) in [int, float]), "%s is not a valid number" % repr(x)
        assert (type(y) in [int, float]), "%s is not a valid number" % repr(y)
        self._x = x
        self._y = y
        self._mark = True
        if self._visible:
            block = self._speed > 0
            self._window._draw_icon(self,self._cursor,x,y,block=block)
    
    def clear(self):
        """
        Deletes the turtle's drawings from the :class:`Window`.
        
        This method does not move the turtle or alter its attributes.  It is different
        from the window's :meth:`~Window.clear` method in that no other turtles are
        affected and the turtle is not removed.
        """
        self._mark = True
        self._window._reset(self)
        
    def reset(self):
        """
        Deletes the turtle's drawings from the :class:`Window`.
        
        This method re-centers the turtle and resets all attributes to their defaults.
        This method is different from the window's :meth:`~Window.clear` method in that 
        no other turtles are affected and the turtle is not removed.
        """
        self._window._reset(self)
        self._x = 0
        self._y = 0
        self._odspd   = self._speed
        self._speed   = 10
        self._odvisib = self._visible
        self._visible = True
        self._heading = 0
        self._odedge = self._edge
        self._edge = '#008000'
        self._odfill = self._fill
        self._fill = '#008000'
        self._image.edge = self._edge
        self._image.fill = self._fill
        self._image.refresh()
        self._cursor = self._image.read()
        block = self._speed > 0
        self._window._draw_icon(self,self._cursor,x,y,block=block)
        self._mark = True
    
    def flush(self):
        """
        Forces a redraw of the associated :class:`Window`.
        
        This is the same as calling :meth:`~Window.flush` on the associated window. 
        It is necessary to update the graphics when the turtle speed is 0.
        """
        self._flush()
        self._mark = True



