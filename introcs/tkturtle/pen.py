"""
The drawing pen

In TKinter, turtles (which draw lines) and pens (which can draw solids) are conflated.
Here we separate them to make it easier for beginners.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


class Pen(object):
    """
    An instance represents a graphics pen.
    
    A graphics pen is like a turtle except that it does not have a heading, and there is 
    no drawmode ``attribute``. Instead, the pen relies on explicit drawing commands such
    as :meth:`drawLine` or :meth:`drawCircle`.
    
    Another difference with the pen is that it can draw solid shapes.  The pen has an 
    attribute called ``fill``.  When this attribute is set to True, it will fill the 
    insides of any polygon traced by its drawLine method. However, the fill will not be 
    completed until fill is set to False, or the move method is invoked.
    
    :ivar speed: The animation speed of this pen.
    :vartype speed: ``int`` in 0..10
    
    :ivar fill: Whether the pen's is drawing a solid shape
    :vartype fill: ``bool``
    
    :ivar pencolor: The outlining color of this pen
    
    :ivar fillcolor: The solid color of this pen
    
    :ivar visible: Whether the pen's icon is visible
    :vartype visible: ``bool``
    
    :ivar origin: the pen origin in the draw window
    :vartype origin: 2D ``tuple``
    
    :ivar x: The x-coordinate of this turtle
    :vartype x: ``float``
    
    :ivar y: The t-coordinate of this turtle
    :vartype y: ``float``
    """
    # PRIVATE ATTRIBUTES:
    #    _screen: Reference to the Tkinter drawing canvas
    #    _turtle: Reference to the TK turtle primitive
    
    
    # MUTABLE PROPERTIES
    @property
    def speed(self):
        """
        The animation speed of this pen.
        
        The speed is an integer from 0 to 10. Speed = 0 means that no animation takes 
        place. The :meth:`drawLine` and :meth:`drawCircle` methods happen instantly with 
        no animation.
        
        Speeds from 1 to 10 enforce increasingly faster animation of line drawing. 1 is 
        the slowest speed while 10 is the fastest (non-instantaneous) speed.
        
        **invariant**: Value must be an ``int`` in the range 0..10.
        """
        return self._turtle.speed()
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 or value <= 10), "%s is outside the range 0..10" % repr(value)
        self._turtle.speed(value)
    
    @property
    def fill(self):
        """
        The fill status of this pen.
        
        If the fill status is True, then the pen will fill the insides of any polygon or 
        circle subsequently traced by its :meth:`drawLine` and :meth:`drawCircle` method. 
        If the attribute changes, it only affects future draw commands, not past ones. 
        Switching this attribute between True and False allows the pen to draw both solid 
        and hollow shapes.
        
        **invariant**: Value must be an ``bool``.
        """
        return self._turtle.filling()
    
    @fill.setter
    def fill(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        if self._turtle.filling() == value:
            return
        
        if value:
            self._turtle.begin_fill()
        else:
            self._turtle.end_fill()
    
    @property
    def color(self):
        """
        Silent, unsupported property requested by a beta tester
        """
        assert False, 'Pen does not have a color; use pencolor or fillcolor'
    
    @color.setter
    def color(self,value):
        assert False, 'Pen does not have a color; use pencolor or fillcolor'
    
    @property
    def pencolor(self):
        """
        The pen color of this pen.
        
        The pen color is used for drawing lines and circles. All subsequent draw commands 
        draw using this color. If the color changes, it only affects future draw commands, 
        not past ones.
        
        This color is only used for lines and the border of circles.  It is not the color 
        used for filling in solid areas (if the ``fill`` attribute  is True).  See the 
        attribute ``fillcolor`` for solid shapes.
        
        **invariant**: Value must be either a string with a color name, a 3 element tuple 
        of floats between 0 and 1 (inclusive), or an object in an additive color model 
        (e.g. RGB or HSV).
        """
        return self._pencolor
    
    @pencolor.setter
    def pencolor(self,value):
        from .window import is_valid_color, to_valid_color
        assert (is_valid_color(value)), "%s is not a valid color input" % repr(value)
        self._turtle.color(to_valid_color(value),self._fillcolor)
        self._pencolor = self._turtle.color()[0]
    
    @property
    def fillcolor(self):
        """
        The fill color of this turtle.
        
        The fill color is used for filling in solid shapes. If the ``fill`` attribute is 
        True, all subsequent draw commands fill their insides using this color.  If the 
        color changes, it only affects future draw commands, not past ones.
        
        This color is only used for filling in the insides of solid shapes.  It is not 
        the color used for the shape border.  See the attribute ``pencolor`` for the 
        border color.
        
        **invariant**: Value must be either a string with a color name, a 3 element tuple 
        of floats between 0 and 1 (inclusive), or an object in an additive color model 
        (e.g. RGB or HSV).
        """
        return self._fillcolor

    @fillcolor.setter
    def fillcolor(self,value):
        from .window import is_valid_color, to_valid_color
        assert (is_valid_color(value)), "%s is not a valid color input" % repr(value)
        self._turtle.color(self._pencolor,to_valid_color(value))
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[1]
    
    @property
    def visible(self):
        """
        Whether the pen's icon is visible.
        
        Drawing commands will still work while the pen icon is hidden. There will just be 
        no indication of the pen's current location on the screen.
        
        **invariant**: Value must be a ``bool``
        """
        return self._turtle.isvisible()
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        if value and not self._turtle.isvisible():
            self._turtle.showturtle()
        elif not value and self._turtle.isvisible():
            self._turtle.hideturtle()
    
    
    @property
    def origin(self):
        """
        The pen origin in the draw window.
        
        This property is used by the Window to reset the pen. This is a "friend" property 
        and the invariant is not enforced.
        
        **invariant**: Value is pair of numbers
        """
        return self._origin
    
    @origin.setter
    def origin(self,value):
        self._origin = value
    
    
    # IMMUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x-coordinate of this pen.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._turtle.xcor()
    
    @property
    def y(self):
        """
        The y-coordinate of this pen.
        
        To change the y coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._turtle.ycor()
    
    
    # BUILT-IN METHODS
    def __init__(self,screen,position=(0, 0), color='red', speed=0):
        """
        Creates a new pen to draw on the given screen.
        
        The color will be assigned to both the pencolor and the fillcolor.
        
        :param screen: window object that pen will draw on.
        :type screen:  :class:`Window`
        
        :param position: initial pen position (origin is screen center)
        :type position:  2D ``tuple``
        
        :param color: initial pen color (default red)
        :type color: see ``color``
        
        :param heading: initial pen directions (default 180)
        :type heading:  ``int`` or ``float``
        
        :param speed: initial pen speed (default 0)
        :type speed:  ``int`` 0..10
        """
        from .window import Window, is_valid_color
        import turtle
        assert type(screen) == Window, "$s is not a Window object" % repr(screen)
        assert (is_valid_color(color)), "%s is not a valid color input" % repr(color)
        self._turtle = turtle.RawTurtle(screen._frame)
        self._turtle.hideturtle()
        
        self._screen = screen
        screen._addPen(self)
        self._turtle.shape('classic')
        
        self._turtle.penup()
        self._turtle.setposition(position)
        self._turtle.color(color)
        self._turtle.speed(speed)
        self._turtle.pendown()
        self._turtle.showturtle()
        
        # Record current color
        # "pair" seems unused
        #pair = self._turtle.color() 
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[0]
    
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
        return 'Pen(position={}, pencolor={}, fillcolor={})'.format(self._turtle.position(), self.pencolor, self.fillcolor)
    
    def __del__(self):
        """
        Deletes this pen object, removing it from the window.
        """
        self._screen._removePen(self)
        del self._turtle
    
    
    # DRAWING METHODS
    def move(self,x,y):
        """
        Moves the pen to given position without drawing.
        
        If the ``fill`` attribute is currently True, this method will complete the fill 
        before moving to the new region. The space between the original position and (x,y) 
        will not be connected.
        
        :param x: new x position for turtle
        :type x:  ``int`` or ``float``
        
        :param y: new y position for turtle
        :type y:  ``int`` or ``float``
        """
        assert (type(x) in [int, float]), "%s is not a valid number" % repr(x)
        assert (type(y) in [int, float]), "%s is not a valid number" % repr(y)
        fstate = self._turtle.filling()
        dstate = self._turtle.isdown()
        if fstate: # only need to do this if in mid-fill
            self._turtle.end_fill()
        if dstate:
            self._turtle.penup()
        self._turtle.setposition(x,y)
        if dstate:
            self._turtle.pendown()
        if fstate: # only need to do this if in mid-fill
            self._turtle.begin_fill()
    
    def drawLine(self, dx, dy):
        """
        Draws a line segment (dx,dy) from the current pen position
        
        The line segment will run from (x,y) to (x+dx,y+dy), where (x,y) is the current 
        pen position.  When done, the pen will be at position (x+dx,y+dy)
        
        :param dx: change in the x position
        :type dx:  ``int`` or ``float``
        
        :param dy: change in the y position
        :type dy:  ``int`` or ``float``
        """
        assert (type(dx) in [int, float]), "%s is not a valid number" % repr(dx)
        assert (type(dy) in [int, float]), "%s is not a valid number" % repr(dy)
        x = self._turtle.xcor()
        y = self._turtle.ycor()
        self._turtle.setposition(x+dx, y+dy)
    
    def drawTo(self, x, y):
        """
        Draws a line from the current pen position to (x,y)
        
        When done, the pen will be at (x, y).
        
        :param x: finishing x position for line
        :type x:  ``int`` or ``float``
        
        :param y: finishing y position for line
        :type y:  ``int`` or ``float``
        """
        assert (type(x) in [int, float]), "%s is not a valid number" % repr(x)
        assert (type(y) in [int, float]), "%s is not a valid number" % repr(y)
        self._turtle.setposition(x, y)
    
    def drawCircle(self, r):
        """
        Draws a circle of radius r centered on the pen.
        
        The center of the circle is the current pen coordinates. When done, the position 
        of the pen will remain unchanged
        
        :param r: radius of the circle
        :type r:  ``int`` or ``float``
        """
        assert (type(r) in [int, float]), "%s is not a valid number" % repr(r)
        x = self._turtle.xcor()
        y = self._turtle.ycor()
        
        # Move the pen into position
        dstate = self._turtle.isdown()
        if dstate:
            self._turtle.penup()
        self._turtle.setposition(x, y-r)
        if dstate:
            self._turtle.pendown()
        
        # Draw the circle and fill if necessary
        self._turtle.circle(r)
        self.flush()
        
        # Return the pen to the position
        if dstate:
            self._turtle.penup()
        self._turtle.setposition(x, y)
        if dstate:
            self._turtle.pendown()
    
    
    # PUBLIC METHODS
    def clear(self):
        """
        Deletes the pen's drawings from the window.
        
        This method does not move the pen or alter its attributes.
        """
        try:
            self._turtle.clear()
        except:
            pass
    
    def reset(self):
        """
        Deletes the pen's drawings from the window.
        
        This method re-centers the pen and resets all attributes to their defaults.
        """
        self._turtle.clear()
        self._turtle.setposition((0,0))        
        self._turtle.shape('classic')
        self._turtle.color('red')
        self.speed = 0
        
        #pair = self._turtle.color()
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[0]
    
    def flush(self):
        """
        Fills in the current drawing, but retains state.
        
        Normally, an object is not filled until you set the state to  False.  Calling this
        method executes this fill, without setting the state to False.  If fill is False, 
        this method does nothing.
        """
        if self.fill:
            self._turtle.end_fill()
            self._turtle.begin_fill()


