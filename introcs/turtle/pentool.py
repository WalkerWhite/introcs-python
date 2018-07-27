"""
The Pen graphics tool

A graphics pen is like a ``Turtle`` except that it does not have a heading, and there 
is no ``drawmode`` attribute. Instead, the pen relies on explicit drawing commands 
such as :meth:`drawLine` or :meth:`drawCircle`.

Another difference with the pen is that it can draw solid shapes.  The pen has an 
attribute called ``solid``.  When this attribute is set to True, it will fill the 
insides of any polygon traced by its ``drawLine`` method. However, the fill will not 
be completed until ``solid`` is set to False, or the move method is invoked.

This class is built on the Tkinter canvas object.  That means we were able to add support 
for dashes and stroke width which did not exist in the original pen.  We also have
proper support for speed 0 (which was always broken in the original pen). The lack
of an instantaneous pen has been the number one complaint at grading sessions since 
Cornell switched to Python.

The one controversial decision about this class is making the begin/end fill feature an
attribute instead of a method.  We could have done this with the classic begin()/end()
methods.  But this is a state, and it is our policy that all state values should have
explicit attributes.  We find that this is necessary in the "objects early, classes late"
approach that we use at Cornell.

:author:  Walker M. White (wmw2)
:version: July 24, 2018
"""
from ._drawtool import _DrawTool, Cursor
from PIL import Image
import math


class StylusCursor(Cursor):
    """
    Instance is an image source for a ``Pen`` cursor.
    
    Naively, this should just be an image file that we load.  However, Tkinter is horrible 
    for image graphics. Images take way too long to draw (one 32x32 image can take up to 
    16 milliseconds -- a full animation frame -- on a MacOS laptop).  And any antialiased
    alpha causes severe artifacts under rotation.
    
    The best solution we have found is for an in-memory image with solid colors vs 
    pure alpha.  To match our drawing tool, we allow for a two-toned image which displays
    both the edge and fill color separately.  Switching colors is done by pixel blitting.
    For a 32x32 image, this is not too bad, and honestly Tkinter is much slower to draw
    the image no matter what we do.
    
    Since Pens are not orientable, we use a pointer style image for its cursor.
    
    :ivar edge: The edge color
    :vartype edge: ``RGB``, ``HSV`` or ``str``
    
    :ivar fill: The edge color
    :vartype fill: ``RGB``, ``HSV`` or ``str``
    """
    
    def _alloc(self):
        """
        Allocates the image.
        
        This creates a stylus pointing at the image origin.
        """
        BACK = (32, 10, 32,  0, 22,  0)
        TIPS = (16, 16, 32, 10, 22,  0)
        
        data = []
        self._mark = []
        for y in range(32):
            for x in range(32):
                if self._inside(x,y,BACK):
                    self._mark.append(2)
                    data.append(self.fill)
                elif self._inside(x,y,TIPS):
                    self._mark.append(1)
                    data.append(self.edge)
                else:
                    self._mark.append(0)
                    data.append((0,0,0,0))
        self._orig = Image.new('RGBA',(32,32))
        self._orig.putdata(data)
        return self._orig


class Pen(_DrawTool):
    """
    An instance represents a graphics pen.
    
    The pen is attached to a window on creation, and this window cannot be changed.
    If the window is closed or deleted, the pen can no longer be used.  Any attempt
    to call a graphics method after the window is disposed will result in an error.
    """
    # PRIVATE ATTRIBUTES:
    #    _tkkey   : A unique key for Tkinter
    #    _window  : The drawing screen
    
    # Whether or not this tool supports orientation
    _ORIENTS = False

    @property
    def speed(self):
        """
        The animation speed of this pen.
        
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
    def solid(self):
        """
        The solid status of this pen.
        
        If the solid status is True, then the pen will fill the insides of any polygon or 
        oval subsequently traced by its :meth:`drawLine` and :meth:`drawOval` method. 
        If the attribute changes, it only affects future draw commands, not past ones. 
        Switching this attribute between True and False allows the pen to draw both solid 
        and hollow shapes.
        
        **Invariant**: Value must be an ``bool``.
        """
        return self._solid
    
    @solid.setter
    def solid(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        if self._solid == value:
            return
        self._mark = True
        if value:
            self._begin_fill()
        else:
            self._end_fill()
    
    @property
    def edgecolor(self):
        """
        The outline color of this pen.
        
        The pen color is used for drawing lines and circles. All subsequent draw commands 
        draw using this color. If the color changes, it only affects future draw commands, 
        not past ones.
        
        This color is only used for lines and the border of circles.  It is not the color 
        used for filling in solid areas (if the :attr:`solid` attribute  is True).  See the 
        attribute :attr:`fillcolor` for solid shapes.
        
        **Invariant**: Value must be either an additive color model (e.g. RGB or HSV) or 
        string representing a color name or a web color (e.g. ``'#f3CC02'``).
        """
        return self._edge
    
    @edgecolor.setter
    def edgecolor(self,value):
        assert (self._is_valid_color(value)), "%s is not a valid color input" % repr(value)
        if self._solid:
            self._end_fill()
            self._begin_fill()
        self._set_color(value,self._fill)
    
    @property
    def fillcolor(self):
        """
        The fill color of this pen.
        
        The fill color is used for filling in solid shapes. If the ``solid`` attribute is 
        True, all subsequent draw commands fill their insides using this color.  If the 
        color changes, it only affects future draw commands, not past ones.
        
        This color is only used for filling in the insides of solid shapes.  It is not 
        the color used for the shape border.  See the attribute :attr:`edgecolor` for the 
        border color.
        
        **Invariant**: Value must be either an additive color model (e.g. RGB or HSV) or 
        string representing a color name or a web color (e.g. ``'#f3CC02'``).
        """
        return self._fill
    
    @fillcolor.setter
    def fillcolor(self,value):
        assert (self._is_valid_color(value)), "%s is not a valid color input" % repr(value)
        if self._solid:
            self._end_fill()
            self._begin_fill()
        self._set_color(self._edge,value)
    
    @property
    def stroke(self):
        """
        The stroke width of this pen.
        
        By default, the pen draws lines that are one pixel wide.  Changing this value
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
        The dash pattern of this pen.
        
        A dash pattern is a tuple of integers that specifes the dash in pixels.  Only
        odd values of the pattern are drawn.  For example, if the pattern is (10,10),
        the turtle will draw 10 pixels, and then stop drawing for 10 pixels.  After 20
        pixels that patterns repeat.  Similarly (10,5,5,10) will draw for 10 pixels, 
        stop for 5 pixels, draw for 10 pixels and the stop for 5 pixels before repeating.
        
        If this value is ``None``, the line will be solid. The dash only applies to lines and 
        borders.  The interior of solid shapes are not dashed.
        
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
        Whether the pen's icon is visible.
        
        Drawing commands will still work while the pen icon is hidden. There will just 
        be no indication of the turtle's current location on the screen.
        
        **Invariant**: Value must be a ``bool``
        """
        return self._visible
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._set_visible(value)
    
    
    # IMMUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x-coordinate of this pen.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._x
    
    @property
    def y(self):
        """
        The y-coordinate of this pen.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._y
    
    @property
    def color(self):
        """
        The colors (outline and fill) of this pen.
        
        This method returns the attributes :attr:`edgecolor` and :attr:`fillcolor` as a 
        tuple (in that order).
        
        *This attribute may not be (directly) altered*
        """
        return (self._edge,self._fill)
    
    
    # BUILT-IN METHODS
    def __init__(self, screen, position=(0, 0), edgecolor='black',fillcolor='red', speed=10):
        """
        :param screen: window object that turtle will draw on.
        :type screen:  ``Window``
        
        :param position: initial pen position (origin is screen center)
        :type position:  2D ``tuple``
        
        :param edgecolor: initial edge color (default black)
        :type edgecolor: ``RGB``, ``HSV`` or ``str``
        
        :param fillcolor: initial fill color (default red)
        :type fill: ``RGB``, ``HSV`` or ``str``
        
        :param speed: initial pen speed (default 10)
        :type speed:  ``int`` 0..10
        """
        super().__init__(screen,position,edgecolor,fillcolor,speed)
        self._solid = False
        self._shist = []
        
        self._image = StylusCursor(edgecolor,fillcolor)
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
        return 'Pen(position={}, edgecolor={}, fillcolor={})'.format((self.x,self.y), self.edgecolor, self.fillcolor)
    

    # DRAWING METHODS
    def move(self,x,y):
        """
        Moves the pen to given position without drawing.
        
        If the :attr:`solid` attribute is currently True, this method will complete the fill 
        before moving to the new region. The space between the original position and (x,y) 
        will not be connected.
        
        :param x: new x position for turtle
        :type x:  ``int`` or ``float``
        
        :param y: new y position for turtle
        :type y:  ``int`` or ``float``
        """
        assert (type(x) in [int, float]), "%s is not a valid number" % repr(x)
        assert (type(y) in [int, float]), "%s is not a valid number" % repr(y)
        if self._solid:
            self._end_fill()
            self._begin_fill()
        
        self._x = x
        self._y = y
        self._mark = True
        if self._visible:
            self._window._draw_icon(self,self._cursor,x,y,block=self._speed > 0)
    
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
        x = self._x + dx
        y = self._y + dy
        self.drawTo(x,y)
    
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
        self._mark = True
        if self._solid:
            self._shist.append(x)
            self._shist.append(y)
        edge = self._to_internal_color(self._edge)
        if self._dash:
            self._follow_line((self._x,self._y,x,y),fill=edge,width=self._width,dash=self._dash)
        else:
            self._follow_line((self._x,self._y,x,y),fill=edge,width=self._width)
    
    def drawOval(self, xradius, yradius):
        """
        Draws a oval with the given radii.
        
        The center of the circle is the current pen coordinates. When done, the position 
        of the pen will remain unchanged.
        
        If :attr:`solid` is true, this will fill the shape when done.
        
        :param xradius: radius of the x-axis
        :type xradius:  ``int`` or ``float``
        
        :param yradius: radius of the y-axis
        :type yradius:  ``int`` or ``float``
        """
        assert (type(xradius) in [int, float]), "%s is not a valid number" % repr(r)
        assert (type(yradius) in [int, float]), "%s is not a valid number" % repr(r)
        self._mark = True
        if self._solid:
            self._end_fill()
            self._begin_fill()
        
        pcolor = self._to_internal_color(self.edgecolor)
        fcolor = self._to_internal_color(self.fillcolor)
        
        kw = {'style':'arc','outline':pcolor,'width':self._width,'start':0,'extent':359, 'block':self._speed > 0}
        if self._dash:
            kw['dash'] = self._dash
        
        self._follow_arc(self.x-xradius,self.y-yradius,self.x+xradius,self.y+yradius,**kw)
        del kw['start']
        del kw['extent']
        del kw['style']
        if self._solid:
            kw['fill'] = fcolor
        self._window._draw_oval(self,self._toolicon(),self.x-xradius,self.y-yradius,self.x+xradius,self.y+yradius,**kw)
    
    def drawRectangle(self, width, height):
        """
        Draws a rectangle with the given width and height.
        
        The current pen coordinates are the bottom left corner of the rectangle. When 
        done, the position of the pen will remain unchanged.
        
        If :attr:`solid` is true, this will fill the shape when done.
        
        :param width: the rectangle width
        :type width:  ``int`` or ``float``
        
        :param height: the rectangle height
        :type height:  ``int`` or ``float``
        """
        assert (type(width) in [int, float]), "%s is not a valid number" % repr(r)
        assert (type(height) in [int, float]), "%s is not a valid number" % repr(r)
        self._mark = True
        if self._solid:
            self._end_fill()
            self._begin_fill()
        
        pcolor = self._to_internal_color(self.edgecolor)
        fcolor = self._to_internal_color(self.fillcolor)
        
        kw = {'fill':pcolor,'width':self._width,'block':self._speed > 0}
        if self._dash:
            kw['dash'] = self._dash
        coords = (self.x,self.y,self.x+width,self.y,self.x+width,self.y+height,self.x,self.y+height,self.x,self.y)
        self._follow_line(coords,**kw)
        kw['outline'] = pcolor
        if self._solid:
            kw['fill'] = fcolor
        else:
            del kw['fill']
        self._window._draw_rectangle(self,self._toolicon(),self.x,self.y,self.x+width,self.y+height,**kw)
    
    
    # PUBLIC METHODS
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
        self._odedge = self._edge
        self._edge = 'back'
        self._odfill = self._fill
        self._fill  = 'red'
        self._dash  = None
        self._width = 1.0
        self._solid = False
        self._shist = []
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
    
    
    # HIDDEN HELPERS
    def _begin_fill(self):
        """
        Starts a fill operation.
        
        This method builds a polygon starting from the current position.
        """
        self._solid = True
        self._shist.append(self.x)
        self._shist.append(self.y)
    
    def _end_fill(self):
        """
        Completes a fill operation.
        
        This method does nothing if only two vertices have been recorded in the
        fill operation.
        """
        pcolor = self._to_internal_color(self.edgecolor)
        fcolor = self._to_internal_color(self.fillcolor)
        kw = {'fill':fcolor,'width':self._width, 'block':self._speed > 0}
        if self._dash:
            kw['dash'] = self._dash
        kw['rollback'] = len(self._shist)//2-1
        
        if len(self._shist) > 4:
            coords = self._shist[-2:]+self._shist[:-2]
            self._window._draw_polygon(self,self._toolicon(),coords,**kw)
            del kw['rollback']
            kw['fill'] = pcolor
            self._window._draw_line(self,self._toolicon(),self._shist,**kw)
        
        self._shist.clear()
        self._solid = False
