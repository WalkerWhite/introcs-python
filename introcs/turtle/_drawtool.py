"""
The basic drawing tool class

Because of the design of the new turtle system, it is cleaner to arrange most of the
drawing commands into a base class used by both ``Turtle`` and ``Pen``.  We would like
to avoid calling the 'friend' methods in ``Window`` from those two proper classes
(though it still happens in a few places).

:author:  Walker M. White (wmw2)
:version: July 24, 2018
"""
import datetime
import os, numpy
from PIL import Image, ImageTk
import traceback
import random
import math
import time
from .window import AttachmentError


class Cursor(object):
    """
    Instance is an image source for a drawing tool cursor.
    
    This is the turtle icon for the ``Turtle`` and the stylus for the ``Pen``.  Naively,
    this should just be an image file that we load.  However, Tkinter is horrible for
    image graphics. Images take way too long to draw (one 32x32 image can take up to 16 
    milliseconds -- a full animation frame -- on a MacOS laptop).  And any antialiased
    alpha causes severe artifacts under rotation.
    
    The best solution we have found is for an in-memory image with solid colors vs 
    pure alpha.  To match our drawing tool, we allow for a two-toned image which displays
    both the edge and fill color separately.  Switching colors is done by pixel blitting.
    For a 32x32 image, this is not too bad, and honestly Tkinter is much slower to draw
    the image no matter what we do.
    
    All images made by this class or subclass should be oriented to the east.
    
    :ivar edge: The edge color
    :vartype edge: ``RGB``, ``HSV`` or ``str``
    
    :ivar fill: The edge color
    :vartype fill: ``RGB``, ``HSV`` or ``str``
    """
    # PRIVATE ATTRIBUTES:
    #    _orig: The original PIL Image
    #    _mark: The tri-color (edge,fill,alpha) representation
    
    
    # MUTABLE PROPERTIES
    @property 
    def edge(self):
        """
        The edge or outline color.
        
        **invariant**: Value must be either an additive color model (e.g. RGB or HSV) or 
        string representing a color name or a web color (e.g. '#f3CC02').
        """
        return self._edge
    
    @edge.setter
    def edge(self,value):
        from .. import colors
        try:
            if type(value) == str:
                if value[0] == '#': 
                    data = colors.RGB.CreateWebColor(value).rgba()
                else:
                    data = colors.RGB.CreateName(value).rgba()
            else:
                data = value.rgba()
        except:
            traceback.print_exc()
            data = None
        assert data is not None, 'Value %s is not a valid color' % repr(value)
        self._edge = data
    
    @property 
    def fill(self):
        """
        The fill color.
        
        **invariant**: Value must be either an additive color model (e.g. RGB or HSV) or 
        string representing a color name or a web color (e.g. '#f3CC02').
        """
        return self._fill
    
    @fill.setter
    def fill(self,value):
        from .. import colors
        try:
            if type(value) == str:
                if value[0] == '#': 
                    data = colors.RGB.CreateWebColor(value).rgba()
                else:
                    data = colors.RGB.CreateName(value).rgba()
            else:
                data = value.rgba()
        except:
            traceback.print_exc()
            data = None
        assert data is not None, 'Value %s is not a valid color' % repr(value)
        self._fill = data
    
    
    # BUILT-IN METHODS
    def __init__(self,edge='#000000',fill = '#888888'):
        """
        Creates a new image source.
        
        :param edge: The edge color
        :type edge:  ``RGB``, ``HSV`` or ``str``
        
        :param fill: The edge color
        :type fill:  ``RGB``, ``HSV`` or ``str``
        """
        self._orig = None
        self._mark = None
        self.edge  = edge
        self.fill  = fill
        self._alloc()
    
    
    # PUBLIC METHODS
    def refresh(self):
        """
        Refreshes the image to use the current colors.
        
        For performance reasons, the image source does not apply colors until
        requested.
        """
        data = []
        for item in self._mark:
            if item == 2:
                data.append(self.fill)
            elif item == 1:
                data.append(self.edge)
            else:
                data.append((0,0,0,0))
        self._orig.putdata(data)
        return self._orig
    
    def read(self,angle=0):
        """
        Creates a Tkinter supported image from the image source.
        
        :param angle: The angle of rotation in degrees
        :type angle:  ``int`` or ``float``
        
        :return: A Tkinter image for this image source
        :rtype:  ``ImageTk``
        """
        if angle == 0:
            copy = self._orig.copy()
        else:
            copy = self._orig.rotate(angle)
        return ImageTk.PhotoImage(copy)
    
    
    # HIDDEN METHODS
    def _alloc(self):
        """
        Allocates the image.
        
        The base class is an example of an arrow to the right.
        """
        OUTER  = ( 8,  8, 26, 16,  8, 24)
        INNER  = ( 8, 12, 20, 16,  8, 20)
        
        data = []
        self._mark = []
        for y in range(32):
            for x in range(32):
                if self._inside(x,y,INNER):
                    self._mark.append(2)
                    data.append(self.fill)
                elif self._inside(x,y,OUTER):
                    self._mark.append(1)
                    data.append(self.edge)
                else:
                    self._mark.append(0)
                    data.append((0,0,0,0))
        self._orig = Image.new('RGBA',(32,32))
        self._orig.putdata(data)
        return self._orig
    
    def _inside(self,x,y,tris):
        """
        Checks if ``(x,y)`` is inside the triangle.
        
        :param x: The x-coordiante
        :type x:  ``int`` or ``float``
        
        :param y: The y-coordiante
        :type y:  ``int`` or ``float``
        
        :param tris: The triangle
        :type tris:  ``tuple`` of 6 numbers
        
        :return: True if ``(x,y)`` is in ``tris``, otherwise False
        :rtype:  ``ImageTk``
        """
        p  = abs((tris[0]*(tris[3]-tris[5]) + tris[2]*(tris[5]-tris[1])+ tris[4]*(tris[1]-tris[3]))/2.0)
        a1 = abs((x*(tris[3]-tris[5]) + tris[2]*(tris[5]-y)+ tris[4]*(y-tris[3]))/2.0)
        a2 = abs((tris[0]*(y-tris[5]) + x*(tris[5]-tris[1])+ tris[4]*(tris[1]-y))/2.0)
        a3 = abs((tris[0]*(tris[3]-y) + tris[2]*(y-tris[1])+ x*(tris[1]-tris[3]))/2.0)
        return numpy.allclose(p,a1+a2+a3)


class _DrawTool(object):
    """
    This class is an abstract class for drawing tool (``Turtle`` or ``Pen``)
    
    This is an abstract class. Attempts to instantiate this class will fail because
    it has no attached image source (the attributes are there, but are None).  To use
    this class, instantiate one of the subclasses instead.
    
    This class provides the underlying attributes and drawing methods for either of
    the two drawing tools. To keep the students from having to read inheritance
    documentation, there are almost no public methods, attributes, or properties 
    in this class.  The only exception is the marking attribute, which is used by
    autograders to track changes.
    
    There are a few things that make this class a bit more complicated than it needs
    to be.  First of all, we have recording attributes to measure changes in attributes
    (this is a hook for autograders).  Second, for performance reasons, we suppress
    unnecessary drawing commands as much as possible.
    """
    # PRIMARY PRIVATE ATTRIBUTES:
    #    _x : The x-coordinate
    #    _y : The x-coordinate
    #    _speed   : The animation speed
    #    _visible : The cursor visibility
    #    _heading : The tool orientation
    #    _edge    : The edge or outline color
    #    _edge    : The fill color
    #    _dash    : The dash pattern
    #    _width   : The stroke width
    #    _image   : The image source
    #    _cursor  : The cursor image
    #    _tkkey   : A unique key for Tkinter
    #    _window  : The drawing screen
    
    # Whether or not this tool supports orientation
    _ORIENTS = False
    
    # CLASS METHODS (UTILITIES)
    @classmethod
    def _is_valid_color(cls,c):
        """
        Determines if ``c`` is a valid color for a drawing tool.
        
        Tools accept RGB, HSV, or strings (for named and web colors)
        
        :param c: a potential color value
        
        :return: True if c is a valid color value.
        :rtype:  ``bool``
        """
        from .. import colors
        if type(c) in [colors.RGB, colors.HSV]:
            return True
        elif type(c) == str:
            return colors.is_tkcolor(c) or colors.is_webcolor(c)
        return False
    
    @classmethod
    def _to_internal_color(cls,c):
        """
        Converts a color to the appropriate TKinter representation.
        
        This method allows us to support all color formats, while using a single
        color format for the backend.
        
        :param c: the color value
        :type c:  valid color
    
        :return: The given color value, converted to an internal format
        :rtype:  ``str``
        """
        from .. import colors
        return c.webColor() if type(c) in [colors.RGB, colors.HSV] else c if c[0] == '#' else colors.tk_webcolor(c)
    
    
    # MUTABLE PROPERTIES
    @property
    def mark(self):
        """
        Whether the tool has been used since last marking
        
        **Invariant**: Value is a bool
        """
        return self._mark
    
    @mark.setter
    def mark(self,value):
        assert (type(value) == bool), "value %s is not a bool" % repr(value)
        self._mark = value
    
    
    # BUILT-IN METHODS
    def __init__(self, screen, position=(0, 0), edge='#000000', fill='#008000', speed=10):
        """
        Creates a new drawing tool to draw on the given screen.
        
        This is abstract initializer.  It does not initialize the image source for the
        cursor, since that is tool dependent.
        
        :param screen: window object that tool will draw on.
        :type screen:  :class:`Window`
        
        :param position: initial tool position (origin is screen center)
        :type position:  2D ``tuple``
        
        :param edge: initial edge color (default black)
        :type edge: ``RGB``, ``HSV`` or ``str``
        
        :param fill: initial fill color (default grey)
        :type fill: ``RGB``, ``HSV`` or ``str``
        
        :param speed: initial turtle speed (default 10)
        :type speed:  ``int`` 0..10
        """
        from .window import Window
        assert isinstance(screen,Window), "$s is not a Window object" % repr(screen)
        assert (type(speed) == int), "%s is not an int" % repr(speed)
        assert (self._is_valid_color(edge)), "%s is not a valid color input" % repr(edge)
        assert (self._is_valid_color(fill)), "%s is not a valid color input" % repr(fill)
        assert (type(speed) == int), "%s is not an int" % repr(speed)
        assert (speed >= 0 or speed <= 10), "%s is outside the range 0..10" % repr(speed)
        try:
            posgood = type(position[0]) in [int,float]
            posgood = posgood and type(position[1]) in [int,float]
        except:
            posgood = False
        assert posgood, "%s is not a valid position" % repr(position)
        
        self._tkkey  = datetime.datetime.utcnow().isoformat()+'-'+str(random.uniform(0,1))
        self._window = screen
        self._window._register(self)
        
        self._x = position[0]
        self._y = position[1]
        self._speed   = speed
        self._odspd   = None
        self._visible = True
        self._odvisib = None
        self._heading = 0
        self._odedge = None
        self._edge = edge
        self._odfill = None
        self._fill = fill
        self._dash  = None
        self._width = 1.0
        self._mark  = False
        
        # This is an abstract class
        self._image  = None
        self._cursor = None
    
    def __del__(self):
        """
        Deletes this drawing tool object, removing it from the window.
        """
        try:
            self._window._unregister(self)
        except:
            pass
    
    # HIDDEN ATTRIBUTES
    def _set_orientation(self,value,show=True):
        """
        Sets the orientation of this tool in degrees.
        
        Heading is measured counter clockwise from due east. If the tool is not orientable,
        this has no effect.
        
        :param value: The tool orientation
        :type value:  ``float``
        
        :param show: Whether to update the orientation on the window.
        :type show:  ``float``
        """
        if not self._window:
            raise AttachmentError('This drawing tool is no longer attached to its window')
        
        self._mark = True
        if not self._ORIENTS:
            return
        self._heading = value
        if self._speed == 0:
            return
        
        self._cursor = self._image.read(value)
        if self._visible and show:
            self._window._draw_icon(self,self._cursor,self._x,self._y)
    
    def _set_speed(self,value):
        """
        Sets the animation speed of this tool.
        
        The speed is an integer from 0 to 10. Speeds from 1 to 10 enforce increasingly 
        faster animation of line drawing and cursor updates. Value 1 is the slowest speed 
        while 10 is the fastest speed.  Roughly, speed 1 draws 1 pixel per step, while
        speed 10 draws an entire line in a single step.
        
        Speed 0 is special.  Speed 0 means that no animation takes place at all.  The
        drawing commands will be remembered, but not shown on the screen.  To display
        the drawing, you must call the method :meth:``flush``. When that method is called,
        all of the drawing commands will be displayed instantly.  This is useful for 
        fast drawing.
        
        If the speed is currently 0, changing the speed will immediately flush any
        existing drawing commands.
        
        :param value: The drawing speed
        :type value:  ``int`` in 0..10
        """
        self._odspd = self._speed
        self._speed = value
        self._mark = True
        
        if self._odspd == 0 and self._speed != 0:
            self._flush()
        
    
    def _set_color(self,edge,fill,show=True):
        """
        Sets the color(s) of this drawing tool.
        
        The edge color is used for lines, and borders.  The fill color is used for 
        solid shapes.
        
        The color values must be either an additive color model (e.g. RGB or HSV) or 
        string representing a color name or a web color (e.g. '#f3CC02').
        
        :param edge: The edge color
        :type edge:  ``RGB``, ``HSV`` or ``str``
        
        :param fill: The edge color
        :type fill:  ``RGB``, ``HSV`` or ``str``
        
        :param show: Whether to update the cursor color on the window.
        :type show:  ``float``
        """
        if not self._window:
            raise AttachmentError('This drawing tool is no longer attached to its window')
        
        self._odedge = self._edge
        self._edge = edge
        self._odfill = self._fill
        self._fill = fill
        self._image.edge = edge
        self._image.fill = fill
        self._image.refresh()
        self._mark = True
        if self._speed == 0:
            return
        
        if self._ORIENTS:
            self._cursor = self._image.read(self._heading)
        else:
            self._cursor = self._image.read()
        if self._visible and show:
            self._window._draw_icon(self,self._cursor,self._x,self._y)
    
    def _set_visible(self,value):
        """
        Sets the visibility of the drawing tools cursor.
        
        Drawing commands will still work while the cursor is hidden. There will just 
        be no indication of the tool's current location on the screen.
        
        :param value: The cursor visibility
        :type value:  ``bool``
        """
        if not self._window:
            raise AttachmentError('This drawing tool is no longer attached to its window')
                
        self._odvisib = self._visible
        self._visible = value
        self._mark = True
        if self._speed == 0:
            return
        
        if value and not self._odvisib:
            self._window._draw_icon(self,self._cursor,self._x,self._y)
        elif not value and self._odvisib:
            self._window._draw_icon(self,None,self._x,self._y)
    
    
    # DRAWING METHODS
    def _toolicon(self):
        """
        Provides the appropriate image for the tool visibility
        
        :return: The current image to send to the display
        :rtype:  ``ImageTk`` or ``None``
        """
        return self._cursor if self._visible else None

    def _flush(self):
        """
        Forces a redraw of the associated Window.
        """
        if not self._window:
            raise AttachmentError('This drawing tool is no longer attached to its window')
        
        # This was suppressed during speed 0
        if self._ORIENTS:
            self._cursor = self._image.read(self._heading)
        else:
            self._cursor = self._image.read()
        self._window._draw_icon(self,self._toolicon(),self._x,self._y)
        self._window.flush()
    
    
    def _follow_line(self,coords,**kw):
        """
        Animates the drawing along the path given by ``coords``.
        
        The value ``coords`` is an iterable of coordinates in Turtle space (which means 
        it has even length). When finished, the cursor is at the final pair of coordinates.
        
        This method supports all of the keyword arguments of the ``tk.Canvas`` method
        ``create_line``.  In addition to those keyword arguments, this method supports
        three other keywords: 'block', 'rollback', and ``track``.  
        
        If 'block' is True, this method will block until the drawing is finished; 
        otherwise drawing proceeds asynchronously.  The 'rollback' value is the number 
        of elements in the history to delete before processing this command. Finally,
        ``track`` instructs the cursor to change orientation as it turns corners.
        
        :param coords: The line path coordinates
        :type coords:  ``iterable`` of ``int`` or ``float``
        
        :param kw: The optional keyword arguments
        :type kw:  ``dict``
        """
        track = False
        if 'track' in kw:
            track = kw['track']
            del kw['track']
        if not self._speed:
            kw['block']  = False
        
        from .. geom import Vector2, Point2
        import math
        
        p = Point2(*coords[:2])
        for pos in range(2,len(coords),2):
            v = Point2(*coords[pos:pos+2])-p
            
            if track:
                angle = v.angle(Vector2(1,0))*180/math.pi
                if v.angle(Vector2(0,1)) > math.pi/2:
                    angle = 360-angle
                self._set_orientation(angle)
            
            length  = v.length() 
            perstep = length if self._speed in [0,10] else 2 ** (self._speed-1)
            stepcnt = math.ceil(length/perstep)
            for x in range(0,stepcnt):
                factor = min((x+1)*perstep/length,1)
                q = p+v*factor
                self._window._draw_line(self,self._toolicon(),(p.x,p.y,q.x,q.y),**kw)
                self._x = q.x
                self._y = q.y
                kw['rollback'] = 1
            kw['rollback'] = 0
            p = Point2(*coords[pos:pos+2])
    
    def _follow_arc(self,left,bottom,right,top,**kw):
        """
        Animates the drawing along an arc in the bounding box ``(left,right)x(bottom,top)``.
        
        All coordinates are given in Turtle space. The arc is a 90 degree arc unless the
        keyword arguments ``start`` and ``extent`` are specified.
        
        This method supports all of the keyword arguments of the ``tk.Canvas`` method
        ``create_line``.  In addition to those keyword arguments, this method supports
        three other keywords: 'block', 'rollback', and ``track``.  
        
        If 'block' is True, this method will block until the drawing is finished; 
        otherwise drawing proceeds asynchronously.  The 'rollback' value is the number 
        of elements in the history to delete before processing this command. Finally,
        ``track`` instructs the cursor to orient itself to the arc tangent at each step.
        
        :param left: The left side of the bounding box
        :type left:  ``int`` or ``float``
        
        :param bottom: The bottom side of the bounding box
        :type bottom:  ``int`` or ``float``
        
        :param right: The right side of the bounding box
        :type right:  ``int`` or ``float``
        
        :param top: The top side of the bounding box
        :type top:  ``int`` or ``float``
        
        :param kw: The optional keyword arguments
        :type kw:  ``dict``
        """
        import tkinter as tk
        track = False
        if 'track' in kw:
            track = kw['track']
            del kw['track']
        if 'style' in kw and kw['style'] == str:
            if kw['style'] == 'arc':
                kw['style'] = tk.ARC
            elif kw['style'] == 'pieslice':
                kw['style'] = tk.PIESLICE
            elif kw['style'] == 'cord':
                kw['style'] = tk.CORD
        
        start = kw['start'] if 'start' in kw else 0.0
        extnt = kw['extent'] if 'extent' in kw else 0.0
        perstep = length if self._speed in [0,10] else 2 ** (self._speed-1)
        stepcnt = math.ceil(extnt/perstep)
        for x in range(0,stepcnt):
            angle = min((x+1)*perstep,extnt)
            kw['extent'] = angle
            if track and extnt != 0:
                angle = self._arc_tangent(left,bottom,right,top,start,angle)
                self._set_orientation(angle,False)
            self._window._draw_arc(self,self._toolicon(),left,bottom,right,top,**kw)
            kw['rollback'] = 1
    
    def _arc_tangent(self,left,bottom,right,top,start,extent):
        """
        Computes the tangent angle for the cursor at the given extent.
        
        This method is only reliable when start != extent.  Otherwise, the direction
        is undefined.
        
        :param left: The left side of the bounding box
        :type left:  ``int`` or ``float``
        
        :param bottom: The bottom side of the bounding box
        :type bottom:  ``int`` or ``float``
        
        :param right: The right side of the bounding box
        :type right:  ``int`` or ``float``
        
        :param top: The top side of the bounding box
        :type top:  ``int`` or ``float``
        
        :param start: The start angle of the arc
        :type start:  ``int`` or ``float``
        
        :param extent: The extent angle of the arc
        :type extent:  ``int`` or ``float``
        """
        from .. geom import Vector2, Point2
        import math
        angle = start+extent
        angle  = math.pi*angle/180.0
        cx = (left+right)/2
        cy = (top+bottom)/2
        rx = (right-left)/2
        ry = (top-bottom)/2
        
        x = math.cos(angle)*rx+cx
        y = math.sin(angle)*ry+cy
        x0 = x-cx
        y0 = y-cy
        
        a  = x0/(rx*rx)
        b  = y0/(ry*ry)
        v = Vector2(-b,a) if extent > 0 else Vector2(a,b)
        result = v.angle(Vector2(1,0))*180/math.pi
        if x0 < 0:
            result = 360-result
        return result

