"""
The drawing turtle

This is an alternate version of Turtle that is much easier to understand than the 
TKinter version (which does not make proper use of properties).

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


class Turtle(object):
    """
    An instance represents a graphics turtle.
    
    A graphics turtle is a pen that is controlled by direction and movement. The turtle 
    is a cursor that that you control by moving it left, right, forward, or backward.  
    As it moves, it draws a line of the same color as  the Turtle.
    
    :ivar heading: The heading of this turtle in degrees.
    :vartype heading: ``float``
    
    :ivar speed: The animation speed of this turtle.
    :vartype speed: ``int`` in 0..10
    
    :ivar color: The color of this turtle
    
    :ivar visible: Whether the turtle's icon is visible
    :vartype visible: ``bool``
    
    :ivar drawmode: Whether the turtle is in draw mode.
    :vartype drawmode: ``bool``
    
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
    def heading(self):
        """
        The heading of this turtle in degrees.
        
        Heading is measured counter clockwise from due east.
        
        **invariant**: Value must be a ``float``
        """
        return float(self._turtle.heading())
    
    @heading.setter
    def heading(self,value):
        assert type(value) in [int, float], "%s is not a valid number" % repr(value)
        self._turtle.setheading(value)
    
    @property
    def speed(self):
        """
        The animation speed of this turtle.
        
        The speed is an integer from 0 to 10. Speed = 0 means that no animation takes 
        place. The methods forward/back makes turtle jump and likewise left/right make 
        the turtle turn instantly.
        
        Speeds from 1 to 10 enforce increasingly faster animation of line drawing and 
        turtle turning. 1 is the slowest speed while 10 is the fastest (non-instantaneous) 
        speed.
        
        **invariant**: Value must be an ``int`` in the range 0..10.
        """
        return self._turtle.speed()
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 or value <= 10), "%s is outside the range 0..10" % repr(value)
        self._turtle.speed(value)

    @property
    def color(self):
        """
        The color of this turtle.
        
        All subsequent draw commands (forward/back) draw using this color. If the color 
        changes, it only affects future draw commands, not past ones.
        
        **invariant**: Value must be either a string with a color name, a 3 element tuple 
        of floats between 0 and 1 (inclusive), or an object in an additive color model 
        (e.g. RGB or HSV).
        """
        return self._color
    
    @color.setter
    def color(self,value):
        from .window import is_valid_color, to_valid_color
        assert (is_valid_color(value)), "%s is not a valid color input" % repr(value)
        self._turtle.color(to_valid_color(value))
        self._color = self._turtle.color()[0]
    
    @property
    def visible(self):
        """
        Whether the turtle's icon is visible.
        
        Drawing commands will still work while the turtle icon is hidden. There will just 
        be no indication of the turtle's current location on the screen.
        
        **Invariant**: Value must be a ``bool``
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
    def drawmode(self):
        """
        Whether the turtle is in draw mode.
        
        All drawing calls are active if an only if this mode is True
        
        **invariant**: Value must be a ``bool``
        """
        return self._turtle.isdown()
    
    @drawmode.setter
    def drawmode(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        if value and not self._turtle.isdown():
            self._turtle.pendown()
        elif not value and self._turtle.isdown():
            self._turtle.penup()
    
    
    # IMMUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._turtle.xcor()
    
    @property
    def y(self):
        """
        The y-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._turtle.ycor()
    
    
    # BUILT-IN METHODS
    def __init__(self,screen,position=(0, 0), color='red', heading=180, speed=0):
        """
        Creates a new turtle to draw on the given screen.
        
        :param screen: window object that turtle will draw on.
        :type screen:  :class:`Window`
        
        :param position: initial turtle position (origin is screen center)
        :type position:  2D ``tuple``
        
        :param color: initial turtle color (default red)
        :type color: see ``color``
        
        :param heading: initial turtle directions (default 180)
        :type heading:  ``int`` or ``float``
        
        :param speed: initial turtle speed (default 0)
        :type speed:  ``int`` 0..10
        """
        from .window import Window, is_valid_color
        import turtle
        assert type(screen) == Window, "$s is not a Window object" % repr(screen)
        assert (is_valid_color(color)), "%s is not a valid color input" % repr(color)
        self._turtle = turtle.RawTurtle(screen._frame)
        self._turtle.hideturtle()

        self._screen = screen
        screen._addTurtle(self)
        self._turtle.shape('turtle')
        self._turtle.penup()
        self.color = color
        self._turtle.setposition(position)
        self._turtle.setheading(heading)
        self._turtle.speed(speed)
        self._turtle.pendown()
        self._turtle.showturtle()
    
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
    
    def __del__(self):
        """
        Deletes this turtle object, removing it from the window.
        """
        self.clear()
        self._screen._removeTurtle(self)
        del self._turtle
    
    
    # PUBLIC METHODS
    def forward(self,distance):
        """
        Moves the turtle forward by the given amount.
        
        This method draws a line if drawmode is True.
        
        :param distance: distance to move in pixels
        :type distance:  ``int`` or ``float``
        """
        assert (type(distance) in [int, float]), "%s is not a valid number" % repr(distance)
        self._turtle.forward(distance)
    
    def backward(self,distance):
        """
        Moves the turtle backward by the given amount.
        
        This method draws a line if drawmode is True.
        
        :param distance: distance to move in pixels
        :type distance:  ``int`` or ``float``
        """
        assert (type(distance) in [int, float]), "%s is not a valid number" % repr(distance)
        self._turtle.backward(distance)
    
    def right(self,degrees):
        """
        Turns the turtle to the right by the given amount.
        
        Nothing is drawn when this method is called.
        
        :param degrees: amount to turn right in degrees
        :type degrees:  ``int`` or ``float``
        """
        assert (type(degrees) in [int, float]), "%s is not a valid number" % repr(degrees)
        self._turtle.right(degrees)
    
    def left(self,degrees):
        """
        Turns the turtle to the left by the given amount.
        
        Nothing is drawn when this method is called.
        
        :param degrees: amount to turn left in degrees
        :type degrees:  ``int`` or ``float``
        """
        assert (type(degrees) in [int, float]), "%s is not a valid number" % repr(degrees)
        self._turtle.left(degrees)
    
    def move(self,x,y):
        """
        Moves the turtle to given position without drawing.
        
        This method does not draw, regardless of the drawmode.
        
        :param x: new x position for turtle
        :type x:  ``int`` or ``float``
        
        :param y: new y position for turtle
        :type y:  ``int`` or ``float``
        """
        assert (type(x) in [int, float]), "%s is not a valid number" % repr(x)
        assert (type(y) in [int, float]), "%s is not a valid number" % repr(y)
        d = self._turtle.isdown()
        if d:
            self._turtle.penup()
        self._turtle.setposition(x,y)
        if d:
            self._turtle.pendown()
    
    def clear(self):
        """
        Deletes the turtle's drawings from the window.
        
        This method does not move the turtle or alter its attributes.
        """
        try:
            self._turtle.clear()
        except:
            pass
        
    def reset(self):
        """
        Deletes the turtle's drawings from the window.
        
        This method re-centers the turtle and resets all attributes to their defaults.
        """
        self._turtle.clear()
        self._turtle.setposition((0,0))        
        self._turtle.shape('turtle')
        self.color = 'red'
        self.heading = 180
        self.speed = 0
    
    def flush(self):
        """Unsupported method for compatibility"""
        pass
