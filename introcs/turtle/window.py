"""
The drawing window for Python graphics

This module replaces the classic, singleton turtle window with a version that is safer
for modern implementations of Tkinter.  In particular, while the Window can be interacted
with in the main thread, it has an asynchronous drawing queue under the hood for 
processing Tkinter commands properly.

To understand this interface, pay close attention to the method names.  Any method that
is not hidden (no underscore) is safe to be accessed in the main thread.  The same is
true for hidden methods without the prefix ``_tk``, though those should be only be accessed
by a ``:class:_DrawTool`` object. These methods are expected to obtain a lock whenever 
they access attributes shared between the Tk thread and the main thread.

Methods that start with the prefix ``_tk`` are executed in the Tkinter thread and have
access to the full features of Tkinter. To prevent reentrant locks, we do not acquire a
lock in any method with prefix ``_tk_internal``. Those are assumed to be helper methods
inside of a lock.

While turtle windows may be resized, take great care when resizing them while
drawing.  Since the origin is typically the center of the window, resizing a
turtle window will shift the drawing implements (``Turtle`` and ``Pen`` objects)
to a new position.  For the most part, this should preserve coordinates, but
round-off error may be an issue.

:author:  Walker M. White (wmw2)
:version: July 24, 2018
"""
from ._context import _Context
import traceback
import random
import math
import time


class AttachmentError(Exception):
    """
    Instance is an error for an illegal drawing operation.
    
    This error is used to prevent drawing tools from using commands when they are unhooked
    from their window.
    """
    pass


class Window(object):
    """
    An instance is a GUI windows that support turtle graphics
    
    You should construct a ``Window`` object before constructing a :class:`Turtle` or 
    :class:`Pen`. While you should only need one ``Window`` object at any given time,
    you may have as many as you want.  Deleteing a ``Window`` object will close the
    window, making the associated turtles and pens invalid.
    """
    # PRIVATE ATTRIBUTES:
    #    _tkkey     : A unique key for Tkinter
    #    _drawtool  : A reference to each draw tool and its cursor
    #    _history   : The drawing history for each draw tool
    #    _commands  : Queued drawing commands
    #    _adjusts   : Queued window adjustment commands
    #    _refreshed : Whether the window has been refreshed
    # NOTE: The memory residency requirements of Tkinter force a reference cycle
    # between a drawing tool and its window. We need to be very careful that we do
    # not get deadlocks in the garbage collector (happened during initial design).
    
    # How long to sleep before waiting for a response
    SLEEP_TIME = 0.005
    
    # MUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x coordinate for top left corner of window
        
        Screen coordinates have their origin in the top left corner, with y increasing
        downwards.
        
        **invariant**: x must be an ``int`` >= 0
        """
        return self._x
    
    @x.setter
    def x(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0), "%s is negative" % repr(value)
        self._adjusts.append(('x',value))
        _Context.Instance().refresh()
        self._x = value
    
    @property
    def y(self):
        """
        The y coordinate for top left corner of window
        
        Screen coordinates have their origin in the top left corner, with y increasing
        downwards.
        
        **invariant**: y must be an ``int`` >= 0
        """
        return self._y
    
    @y.setter
    def y(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0), "%s is negative" % repr(value)
        self._adjusts.append(('y',value))
        _Context.Instance().refresh()
        self._y = value
    
    @property
    def width(self):
        """
        The width of the drawing canvas in pixels
        
        The width specified is the width of the internal drawing canvas. The width does 
        not include the border or window frame (title, close buttons, etc.)
        
        **invariant**: width must be an ``int`` > 0
        """
        return self._width
    
    @width.setter
    def width(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value > 0), "%s is not positive" % repr(value)
        self._adjusts.append(('width',value))
        _Context.Instance().refresh()
        self._width = value
    
    @property
    def height(self):
        """
        The height of the drawing canvas in pixels
        
        The height specified is the height of the internal drawing canvas. The height does 
        not include the border or window frame (title, close buttons, etc.)
        
        **invariant**: height must be an ``int`` > 0
        """
        return self._height
    
    @height.setter
    def height(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value > 0), "%s is not positive" % repr(value)
        self._adjusts.append(('height',value))
        _Context.Instance().refresh()
        self._height = value
    
    @property
    def title(self):
        """
        The title displayed at top of window bar
        
        **invariant**: title must be a ``str``
        """
        return self._title
    
    @title.setter
    def title(self,value):
        assert (type(value) == str), "%s is not a string" % repr(value)
        self._adjusts.append(('title',value))
        _Context.Instance().refresh()
        self._title = value
    
    @property
    def resizable(self):
        """
        Whether or not the Window supports user resizing
        
        **invariant**: resizable must be a ``bool``
        """
        return self._resizable
    
    @resizable.setter
    def resizable(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._resizable = value
        self._adjusts.append(('lock',value,value))
        _Context.Instance().refresh()
    
    @property
    def mark(self):
        """
        Whether Window has been used since last marking
        
        This attribute is a hook for autograders
        
        **Invariant**: Value is a bool"""
        return self._mark
    
    @mark.setter
    def mark(self,value):
        assert (type(value) == bool), "value %s is not a bool" % repr(value)
        self._mark = value
    
    
    # IMMUTABLE PROPERTIES
    @property
    def turtles(self):
        """
        The tuple of all turtles attached to this Window
        
        *This attribute may not be altered directly*
        """
        from .turtle import Turtle
        with self._lock:
            items = [item[0] for item in self._drawtool.values()]
        return tuple(filter(lambda x: isinstance(x,Turtle), items))

    @property
    def pens(self):
        """
        The tuple of all pens attached to this Window.
        
        *This attribute may not be altered directly*
        """
        from .pentool import Pen
        with self._lock:
            items = [item[0] for item in self._drawtool.values()]
        return tuple(filter(lambda x: isinstance(x,Pen), items))
    
    @property
    def speed(self):
        """
        The speed of the last drawing tool to draw to this Window.
        
        This value is none if the Window has never been draw on. This attribute is a hook 
        for autograders.
        
        *This attribute may not be altered directly*
        """
        return self._lastspeed
    
    @property
    def visibility(self):
        """
        The visibility of the last drawing tool to draw to this Window.
        
        This value is none if the Window has never been draw on. This attribute is a hook 
        for autograders.
        
        *This attribute may not be altered directly*
        """
        return self._lastvisib
    
    
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
    def __init__(self, x=50, y=50, width=700, height=700, scale=1):
        """
        :param x: initial x coordinate (default 50)
        :type x: ``int`` >= 0
        
        :param y: initial y coordinate (default 50)
        :type y: ``int`` >= 0
        
        :param width: initial window width (default 700)
        :type width: ``int`` > 0
        
        :param height: initial window height (default 700)
        :type height: ``int`` > 0
        
        :param scale: initial window scale (INGORED)
        :type scale:  ``float`` > 0
        """
        import datetime
        self._tkkey = datetime.datetime.utcnow().isoformat()+'-'+str(random.uniform(0,1))
        
        # Main thread attributes
        self._title = 'Python Turtle Graphics'
        self._mark  = False
        self._x = x
        self._y = y
        self._width  = width
        self._height = height
        self._mark   = False
        self._lastspeed = None
        self._lastvisib = None
        
        self._active = False
        self._clear  = False
        
        # Shared attributes
        self._history  = {}
        self._drawtool = {}
        self._commands = []
        self._adjusts  = []
        
        # To ensure consistency across platforms
        self._refreshed = False
        
        import threading
        self._lock = threading.Lock()
        _Context.Instance().alloc(self,x,y,width,height)
    
    def __del__(self):
        """
        Destroys this window and its associated assets
        """
        self.dispose()
    
    
    # PUBLIC METHODS
    def clear(self):
        """
        Erases the contents of this Window
        
        All Turtles and Pens are eliminated from the Window. Any attempt to use a 
        previously created :class:`Turtle` or :class:`Pen` will fail.
        """
        with self._lock:
            self._clear = True
            self._refreshed = True
        _Context.Instance().refresh()
    
    def dispose(self):
        """
        Closes the graphics Window, deleting all assets.
        """
        context = _Context.Instance()
        context.dealloc(self)
    
    def flush(self):
        """
        Displays any pending drawing commands on the screen.
        
        This command is necessary when :class:`Turtle` or :class:`Pen` speed is set to 0.  
        When that happens, the drawing tool will not force a refresh until this command is
        executed.
        """
        with self._lock:
            self._refreshed = True
        
        _Context.Instance().refresh()
    
    def iconify(self):
        """
        Shrinks the Window down to an icon, effectively hiding it
        """
        self._adjusts.append(['iconify'])
        self.flush()
    
    def deiconify(self):
        """
        Expands the Window from an icon so that it is visible
        """
        self._adjusts.append(['deiconify'])
        self.flush()
    
    def setPosition(self,x,y):
        """
        Sets the position of this Window
        
        Screen coordinates have their origin in the top left corner, with y increasing
        downwards.
        
        :param x: the left edge of the window
        :type width: ``int`` > 0
        
        :param y: the top edge of the window
        :type height: ``int`` > 0
        """
        assert (type(x) == int), "x %s is not an int" % repr(width)
        assert (x > 0), "x %s is negative" % repr(width)
        assert (type(y) == int), "y %s is not an int" % repr(height)
        assert (y > 0), "y %s is negative" % repr(height)
        self._adjusts.append(('pos',x,y))
        self.flush()
    
    def setSize(self,width,height):
        """
        Sets the size for this Window
        
        The size specified is the actual the size of the internal drawing canvas. The
        size does not include the border or window frame (title, close buttons, etc.)
        
        :param width: the window width
        :type width: ``int`` > 0
        
        :param height: the height width
        :type height: ``int`` > 0
        """
        assert (type(width) == int), "width %s is not an int" % repr(width)
        assert (width > 0), "width %s is negative" % repr(width)
        assert (type(height) == int), "height %s is not an int" % repr(height)
        assert (height > 0), "height %s is negative" % repr(height)
        self._adjusts.append(('size',width,height))
        self.flush()
    
    def setMaxSize(self,width,height):
        """
        Sets the maximum size for this Window
        
        The size specified is the maximum the size of the internal drawing canvas. The
        size does not include the border or window frame (title, close buttons, etc.)
        
        Any attempt to resize a dimension beyond the maximum size will fail.
        
        :param width: the maximum Window width
        :type width: ``int`` > 0
        
        :param height: the maximum Window height
        :type height: ``int`` > 0
        """
        assert (type(width) == int), "width %s is not an int" % repr(width)
        assert (width > 0), "width %s is negative" % repr(width)
        assert (type(height) == int), "height %s is not an int" % repr(height)
        assert (height > 0), "height %s is negative" % repr(height)
        self._adjusts.append(('maxsize',width,height))
        self.flush()
    
    def setMinSize(self,width,height):
        """
        Sets the minimum size for this window
        
        The size specified is the minimum the size of the internal drawing canvas. The
        size does not include the border or window frame (title, close buttons, etc.)
        
        Any attempt to resize a dimension below the minimum size will fail.
        
        :param width: the minimum Window width
        :type width: ``int`` > 0
        
        :param height: the minimum Window height
        :type height: ``int`` > 0
        """
        assert (type(width) == int), "width %s is not an int" % repr(width)
        assert (width > 0), "width %s is negative" % repr(width)
        assert (type(height) == int), "height %s is not an int" % repr(height)
        assert (height > 0), "height %s is negative" % repr(height)
        self._adjusts.append(('maxsize',width,height))
        self.flush()
    
    def beep(self):
        """
        Plays an OS specific alert sound
        """
        self._adjusts.append(['bell'])
        self.flush()
    
    
    # UNSUPPORTED METHODS
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
    
    
    # Turtle Friend Methods
    def _register(self,tool):
        """
        Adds a drawing tool to this Window.
        
        :param tool: the drawing tool
        :type tool:  ``_DrawTool``
        """
        with self._lock:
            if not self._window:
                raise AttachmentError('This window has been disposed')
        
            self._drawtool[tool._tkkey] = [tool,None,None]
            self._history[tool._tkkey]  = []
            self._mark = True
    
    def _unregister(self,tool):
        """
        Removes a drawing tool from this Window.
        
        :param tool: the drawing tool
        :type tool:  ``_DrawTool``
        """
        with self._lock:
            if not tool._tkkey in self._drawtool:
                self.tool._windpw = None  # Just to be sure
                return
        
        self._queue_command(None,None,(0,0),self._tk_internal_remove_tool,[tool._tkkey],{'block':False})
        self._mark = True
    
    def _reset(self,tool):
        """
        Deletes the full history of a tool.
        
        :param tool: the drawing tool
        :type tool:  ``_DrawTool``
        """
        with self._lock:
            if not tool._tkkey in self._drawtool:
                raise AttachmentError('This drawing tool is no longer attached to its window')
            steps = len(self._history[tool._tkkey])
        
        self._queue_command(None,None,(0,0),self._tk_internal_delete_history,[tool._tkkey,steps],{'block':False})
        self._mark = True
    
    def _queue_command(self,key,icon,pos,cmd,args,kw):
        """
        Queues a drawing command to be processed by the Tkinter thread.
        
        The drawing command may actually be a sequence of drawing commands, for deleting 
        shapes, drawing a new shape, and drawing the icon.  However, this method ensures 
        that they are always packaged together as an atomic operation. Both ``icon`` and 
        ``cmd`` may be ``None``, making each of those drawing commands optional.
        
        In addition to the standard key word arguments, this method supports three other
        keywords: 'block', 'rollback', and 'noicon'.  If 'block' is true, this method
        will block until the drawing is finished; otherwise drawing proceeds 
        asynchronously.  The 'rollback' value is the number of elements in the history
        to delete before processing this command.  Finally 'noicon' will not update 
        the icon on the screen. All of these are useful for controlling animation.
        
        :param key: The drawing tool identifier key
        :type key: ``str``
        
        :param icon: The icon for the drawing tool (None if not visible)
        :type icon:  ``ImageTk`` or ``None``
        
        :param pos: The canvas coordinates for the tool icon
        :type pos:  ``tuple`` of  (``int``,``int``)
        
        :param cmd: The drawing function
        :type cmd:  ``callable`` or ``None``
        
        :param args: The positional arguments for ``cmd``
        :type args:  ``list`` or ``tuple``
        
        :param kw: The keyword arguments for ``cmd``
        :type kw:  ``dict``
        """
        rollback = 0
        blocking = True
        noicon = False
        if 'rollback' in kw:
            rollback = kw['rollback']
            del kw['rollback']
        
        if 'block' in kw:
            blocking = kw['block']
            del kw['block']
        
        if 'noicon' in kw:
            noicon = kw['noicon']
            del kw['noicon']
        
        try:
            with self._lock:
                if key and not noicon:
                    self._commands.append((None,self._tk_internal_delete_icon,[key],{}))
                if rollback:
                    self._commands.append((None,self._tk_internal_delete_history,[key,rollback],{}))
                if cmd:
                    self._commands.append((key,cmd,args,kw))
                if icon and not noicon:
                    self._commands.append((None,self._tk_internal_draw_icon,[key,icon,pos],{}))
            
            if blocking:
                self.flush()
                while self._commands:
                    time.sleep(self.SLEEP_TIME)
        except:
            traceback.print_exc()
            pass
    
    def _convert_coords(self,x,y):
        """
        Converts the coordinates ``(x,y)`` from Turtle space to screen space.
        
        :param x: The x coordinate in Turtle space
        :type x:  ``int`` or ``float``
        
        :param y: The y coordinate in Turtle space
        :type y:  ``int`` or ``float``
        
        :return: The screen coordinates for ``(x,y)``
        :rtype:  ``tuple`` of  (``int``,``int``)
        """
        cx = self._canvas._currw/2
        cy = self._canvas._currh/2
        return (x+cx,cy-y)
    
    def _draw_icon(self,tool,icon,x,y,**kw):
        """
        Draws the icon at position ``(x,y)``.
        
        If ``icon`` is None, nothing is drawn (and the previous icon is erased). The 
        coordinates are given in Turtle space.
        
        This method supports two keywords: 'block' and 'rollback'.  If 'block' is true, 
        this method will block until the drawing is finished; otherwise drawing proceeds 
        asynchronously.  The 'rollback' value is the number of elements in the history
        to delete before processing this command.  Both of these are useful for
        controlling animation.
        
        :param tool: The drawing tool
        :type tool: ``_DrawTool``
        
        :param icon: The icon for the drawing tool (None if not visible)
        :type icon:  ``ImageTk`` or ``None``
        
        :param x: The x-coordinate of the icon
        :type x:  ``int`` or ``float``
        
        :param y: The y-coordinate of the icon
        :type y:  ``int`` or ``float``
        
        :param kw: The optional keyword arguments
        :type kw:  ``dict``
        """
        with self._lock:
            if not tool._tkkey in self._drawtool:
                raise AttachmentError('This drawing tool is no longer attached to its window')
        
        self._lastspeed = tool._speed
        self._lastvisib = tool._visible
        self._mark = True
        
        pos = self._convert_coords(x,y)
        self._queue_command(tool._tkkey,icon,pos,None,[],kw)
    
    def _draw_line(self,tool,icon,coords,**kw):
        """
        Draws a line path following coords.
        
        The value ``coords`` is an iterable of coordinates in Turtle space (which means 
        it has even length). If ``icon`` is not None, it is displayed at the final pair
        of coordinates.  Both the icon and the line path are grouped together (with the 
        icon on top), making this an atomic drawing operation.
        
       This method supports all of the keyword arguments of the ``tk.Canvas`` method
        ``create_line``. In addition, this method supports three other keywords: 'block', 
        'rollback', and 'noicon'.  If 'block' is true, this method will block until the 
        drawing is finished; otherwise drawing proceeds asynchronously.  The 'rollback' 
        value is the number of elements in the history to delete before processing this 
        command.  Finally 'noicon' will not update the icon on the screen. All of these 
        are useful for controlling animation.
        
        :param tool: The drawing tool
        :type tool: ``_DrawTool``
        
        :param icon: The icon for the drawing tool (None if not visible)
        :type icon:  ``ImageTk`` or ``None``
        
        :param coords: The line path coordinates
        :type coords:  ``iterable`` of ``int`` or ``float``
        
        :param kw: The optional keyword arguments
        :type kw:  ``dict``
        """
        with self._lock:
            if not tool._tkkey in self._drawtool:
                raise AttachmentError('This drawing tool is no longer attached to its window')
        
        self._lastspeed = tool._speed
        self._lastvisib = tool._visible
        self._mark = True
        
        convs = []
        for x in range(0,len(coords),2):
            convs.extend(self._convert_coords(coords[x],coords[x+1]))
        self._queue_command(tool._tkkey,icon,convs[-2:],self._canvas.create_line,convs,kw)
    
    def _draw_arc(self,tool,icon,left,bottom,right,top,**kw):
        """
        Draws an arc in the bounding box ``(left,right)x(bottom,top)``.
        
        All coordinates are given in Turtle space. If ``icon`` is not None, it is 
        displayed at the end of the arc.  Both the icon and the arc are grouped together 
        (with the icon on top), making this an atomic drawing operation.
        
        This method supports all of the keyword arguments of the ``tk.Canvas`` method
        ``create_arc``. In addition, this method supports three other keywords: 'block', 
        'rollback', and 'noicon'.  If 'block' is true, this method will block until the 
        drawing is finished; otherwise drawing proceeds asynchronously.  The 'rollback' 
        value is the number of elements in the history to delete before processing this 
        command.  Finally 'noicon' will not update the icon on the screen. All of these 
        are useful for controlling animation.
        
        :param tool: The drawing tool
        :type tool: ``_DrawTool``
        
        :param icon: The icon for the drawing tool (None if not visible)
        :type icon:  ``ImageTk`` or ``None``
        
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
        with self._lock:
            if not tool._tkkey in self._drawtool:
                raise AttachmentError('This drawing tool is no longer attached to its window')
        
        import tkinter as tk
        left, bottom = self._convert_coords(left,bottom)
        right,top = self._convert_coords(right,top)
        
        self._lastspeed = tool._speed
        self._lastvisib = tool._visible
        self._mark = True
        
        # Find the position
        x = 0
        y = 0
        if icon:
            center = ((left+right)/2.0,(top+bottom)/2.0)
            radius = ((right-left)/2.0,(top-bottom)/2.0)
            angle  = kw['start'] if 'start' in kw else 0.0
            angle  += kw['extent'] if 'extent' in kw else 90.0
            angle  = math.pi*angle/180.0
            x = math.cos(angle)*radius[0]+center[0]
            y = math.sin(angle)*radius[1]+center[1]
        self._queue_command(tool._tkkey,icon,(x,y),self._canvas.create_arc,[left,top,right,bottom],kw)
    
    def _draw_oval(self,tool,icon,left,bottom,right,top,**kw):
        """
        Draws an oval in the bounding box ``(left,right)x(bottom,top)``.
        
        All coordinates are given in Turtle space. If ``icon`` is not None, it is 
        displayed at the center of the oval  Both the icon and the oval are grouped 
        together (with the icon on top), making this an atomic drawing operation.
        
        This method supports all of the keyword arguments of the ``tk.Canvas`` method
        ``create_oval``. In addition, this method supports three other keywords: 'block', 
        'rollback', and 'noicon'.  If 'block' is true, this method will block until the 
        drawing is finished; otherwise drawing proceeds asynchronously.  The 'rollback' 
        value is the number of elements in the history to delete before processing this 
        command.  Finally 'noicon' will not update the icon on the screen. All of these 
        are useful for controlling animation.
        
        :param tool: The drawing tool
        :type tool: ``_DrawTool``
        
        :param icon: The icon for the drawing tool (None if not visible)
        :type icon:  ``ImageTk`` or ``None``
        
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
        with self._lock:
            if not tool._tkkey in self._drawtool:
                raise AttachmentError('This drawing tool is no longer attached to its window')
        
        self._lastspeed = tool._speed
        self._lastvisib = tool._visible
        self._mark = True
        
        left, bottom = self._convert_coords(left,bottom)
        right,top = self._convert_coords(right,top)
        center = ((left+right)/2.0,(top+bottom)/2.0)
        self._queue_command(tool._tkkey,icon,center,self._canvas.create_oval,[left,top,right,bottom],kw)
    
    def _draw_rectangle(self,tool,icon,left,bottom,right,top,**kw):
        """
        Draws a rectangle in the bounding box ``(left,right)x(bottom,top)``.
        
        All coordinates are given in Turtle space. If ``icon`` is not None, it is 
        displayed at bottom left corner  Both the icon and the rectangle are grouped 
        together (with the icon on top), making this an atomic drawing operation.
        
        This method supports all of the keyword arguments of the ``tk.Canvas`` method
        ``create_rectangle``. In addition, this method supports three other keywords: 'block', 
        'rollback', and 'noicon'.  If 'block' is true, this method will block until the 
        drawing is finished; otherwise drawing proceeds asynchronously.  The 'rollback' 
        value is the number of elements in the history to delete before processing this 
        command.  Finally 'noicon' will not update the icon on the screen. All of these 
        are useful for controlling animation.
        
        :param tool: The drawing tool
        :type tool: ``_DrawTool``
        
        :param icon: The icon for the drawing tool (None if not visible)
        :type icon:  ``ImageTk`` or ``None``
        
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
        with self._lock:
            if not tool._tkkey in self._drawtool:
                raise AttachmentError('This drawing tool is no longer attached to its window')
        
        self._lastspeed = tool._speed
        self._lastvisib = tool._visible
        self._mark = True
        
        left, bottom = self._convert_coords(left,bottom)
        right,top = self._convert_coords(right,top)
        self._queue_command(tool._tkkey,icon,(left,bottom),self._canvas.create_rectangle,[left,top,right,bottom],kw)
    
    def _draw_polygon(self,tool,icon,coords,**kw):
        """
        Draws the two dimensional polygon specified by ``coords``.
        
        The value ``coords`` is an iterable of coordinates in Turtle space (which means 
        it has even length). If ``icon`` is not None, it is displayed at the first 
        (and last) polygon vertex.  Both the icon and the polygon are grouped 
        together (with the icon on top), making this an atomic drawing operation.
        
        This method supports all of the keyword arguments of the ``tk.Canvas`` method
        ``create_polygon``. In addition, this method supports three other keywords: 'block', 
        'rollback', and 'noicon'.  If 'block' is true, this method will block until the 
        drawing is finished; otherwise drawing proceeds asynchronously.  The 'rollback' 
        value is the number of elements in the history to delete before processing this 
        command.  Finally 'noicon' will not update the icon on the screen. All of these 
        are useful for controlling animation.
        
        :param tool: The drawing tool
        :type tool: ``_DrawTool``
        
        :param icon: The icon for the drawing tool (None if not visible)
        :type icon:  ``ImageTk`` or ``None``
        
        :param coords: The polygon coordinates
        :type coords:  ``iterable`` of ``int`` or ``float``
        
        :param kw: The optional keyword arguments
        :type kw:  ``dict``
        """
        with self._lock:
            if not tool._tkkey in self._drawtool:
                raise AttachmentError('This drawing tool is no longer attached to its window')
        
        self._lastspeed = tool._speed
        self._lastvisib = tool._visible
        self._mark = True
        
        convs = []
        for x in range(0,len(coords),2):
            convs.extend(self._convert_coords(coords[x],coords[x+1]))
        self._queue_command(tool._tkkey,icon,convs[:2],self._canvas.create_polygon,convs,kw)
    
    
    # TK Entry Points
    def _tk_update(self):
        """
        Performs a single update in the Tkinter thread
        
        This method processes all graphics and window modification commands.
        """
        with self._lock:
            # The garbage collector will cause a deadlock if we do not do this.
            import copy
            gcblock = copy.copy(self._drawtool)
            if self._clear:
                import tkinter as tk
                self._canvas.delete(tk.ALL)
                for key in tuple(self._drawtool.keys()):
                    self._tk_internal_remove_tool(key)
                self._drawtool.clear()
                self._history.clear()
                self._commands.clear()
                self._clear = False
            if self._refreshed:
                for cmnd in self._commands:
                    self._tk_internal_execute(cmnd)
                self._refreshed = False
            self._commands.clear()
            for cmnd in self._adjusts:
                self._tk_internal_adjust(cmnd)
            self._adjusts.clear()
    
    def _tk_resize(self,event):
        """
        Responds to a Tkinter resize request.
        
        This request only applies to the outer panel.  We need to resize the canvas
        to match.  In addition, we need to shift all objects to recenter them and
        preserve Turtle coordinates.
        
        :param event: The resize event
        :type event:  ``tk.Event``
        """
        w = self._window.winfo_width()-self._canvas._dw
        h = self._window.winfo_height()-self._canvas._dh
        self._canvas._lastw = self._canvas._currw
        self._canvas._lasth = self._canvas._currh
        self._canvas._currw = w
        self._canvas._currh = h
        dw = self._canvas._currw-self._canvas._lastw
        dh = self._canvas._currh-self._canvas._lasth
        self._canvas.config(width=w,height=h)
        if dw or dh:
            self._canvas.move('all',dw/2.0,dh/2.0)
            _Context.Instance().refresh()
    
    def _tk_dispose(self):
        """
        Disposes of all Tkinter assets.
        
        This is called by the Tkinter context on clean-up.
        """
        import copy
        with self._lock:
            if not self._window:
                return
            
            # The garbage collector will cause a deadlock if we do not do this.
            gcblock = copy.copy(self._drawtool)
            for key in tuple(self._drawtool.keys()):
                self._tk_internal_remove_tool(key)
            self._drawtool.clear()
            self._history.clear()
            self._commands.clear()
            self._window.destroy()
            self._window = None
    
    
    # Internal TK Helpers
    def _tk_internal_execute(self,cmd):
        """
        Executes a drawing command.
        
        The drawing command is a four element tuple of: the drawing tool key, the
        callable function, the positional arguments, and the keyword arguments.
        
        :param cmd: The drawing command
        :type cmd:  ``tuple`` of (``str``, ``callable``, ``list``, ``dict``)
        """
        if cmd[0] is None:
            cmd[1](*cmd[2],**cmd[3])
            return
        
        try:
            hist = self._history[cmd[0]]
            item = cmd[1](*cmd[2],**cmd[3])
            hist.append(item)
        except:
            traceback.print_exc()
            pass
    
    def _tk_internal_adjust(self,cmd):
        """
        Executes a window adjustment command.
        
        The adjustment command is a tuple consisting of a string followed by one or more 
        arguments.
        
        :param cmd: The window adjustment command
        :type cmd:  ``tuple`` of (``str``, ...)
        """
        if cmd[0] == 'title':
            self._window.title(cmd[1])
        elif cmd[0] == 'x':
            self._window.geometry('+%d+%d' % (cmd[1],self._window.winfo_y()))
        elif cmd[0] == 'y':
            self._window.geometry('+%d+%d' % (self._window.winfo_x(),cmd[1]))
        elif cmd[0] == 'pos':
            self._window.geometry('+%d+%d' % (cmd[1],cmd[2]))
        elif cmd[0] == 'width':
            self._canvas._currw = cmd[1]
            self._panels.config(width=cmd[1]+self._canvas._dw,height=self._panels.winfo_height())
        elif cmd[0] == 'height':
            self._canvas._currh = cmd[1]
            self._panels.config(width=self._panels.winfo_width(),height=cmd[1]+self._canvas._dh)
        elif cmd[0] == 'size':
            self._canvas._currw = cmd[1]
            self._canvas._currh = cmd[2]
            self._panels.config(width=cmd[1]+self._canvas._dw,height=cmd[2]+self._canvas._dh)
        elif cmd[0] == 'lock':
            self._window.resizable(*cmd[1:])
        elif cmd[0] == 'minsize':
            self._window.minsize(cmd[1]+self._canvas._dw,cmd[2]+self._canvas._dh)
        elif cmd[0] == 'maxsize':
            self._window.maxsize(cmd[1]+self._canvas._dw,cmd[2]+self._canvas._dh)
        elif cmd[0] == 'iconify':
            self._window.iconify()
        elif cmd[0] == 'deiconify':
            self._window.deiconify()
        elif cmd[0] == 'bell':
            self._window.bell()
    
    def _tk_internal_delete_icon(self,key):
        """
        Drawing command to delete a drawing tool icon.
        
        This is a callable for sending to the drawing queue.
        
        :param key: The drawing tool identifier key
        :type key: ``str``
        """
        try:
            refs = self._drawtool[key]
            icon = refs[2]
            if icon:
                self._canvas.delete(icon)
                refs[1] = None
                refs[2] = None
        except:
            traceback.print_exc()
            pass
    
    def _tk_internal_draw_icon(self,key,icon,pos):
        """
        Drawing command to draw a drawing tool icon.
        
        This is a callable for sending to the drawing queue.
        
        :param key: The drawing tool identifier key
        :type key: ``str``
        """
        from PIL import ImageTk
        try:
            refs = self._drawtool[key]
            refs[2] = self._canvas.create_image(pos,image=icon)
            refs[1] = icon
        except:
            traceback.print_exc()
            pass
    
    def _tk_internal_delete_history(self,key,steps):
        """
        Drawing command to delete (part of) the history of a drawing tool.
        
        Elements are deleted in the reverse order that they were drawn. This is a 
        callable for sending to the drawing queue.
        
        :param key: The drawing tool identifier key
        :type key: ``str``
        
        :param steps: The number of commands to delete, from the most recent
        :type steps: ``int`` >= 0
        """
        try:
            hist = self._history[key]
            for x in range(steps):
                item = hist.pop()
                self._canvas.delete(item)
        except:
            pass
    
    def _tk_internal_remove_tool(self,key):
        """
        Drawing command to completely delete a tool and its history.
        
        :param key: The drawing tool identifier key
        :type key: ``str``
        """
        try:
            for item in self._history[key]:
                self._canvas.delete(item)
            refs = self._drawtool[key]
            if refs[2]:
                self._canvas.delete(refs[2])
            refs[0]._window = None
            del self._drawtool[key]
            del self._history[key]
        except:
            traceback.print_exc()
            pass

