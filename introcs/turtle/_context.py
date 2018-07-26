"""
TKinter context support for turtle graphics.

This is the heart of the great Turtle refactor.  The problem with the old turtle is that
some platforms force Tkinter in the main thread, but always process OS events, and other
platforms force a separate thread for Tkinter to prevent event hanging.  This module
allows us to provide the correct context for either platform.

A context is essentially the main Tkinter application.  It is created when we allocate
the first window, and destroyed either when we destroy the last window or quit Python.

:author:  Walker M. White (wmw2)
:version: July 24, 2018
"""
import threading
import os, time


class _TK_Thread(threading.Thread):
    """
    An instance is a separate thread for processing Tkinter commands.
    
    This is necessary on Windows and Linux platforms, but not on OS.  Because this thread
    can hang Python, we need to be sure to kill it when no longer needed (typically when
    the last window is destroyed).
    """
    # PRIVATE ATTRIBUTES:
    #   _initd:   Whether the thread is initialized
    #   _active:  Whether the thread is alive   
    #   _context: The associated Tkinter context
    #   _root   : The Tkinter root
    
    # The refresh rate in milliseconds
    REFRESH = 1
    
    def __init__(self,context):
        """
        Creates and starts a Tkinter thread
        
        :param context: The application context communicating with this thread
        :type context:  ``_AsyncContext``
        """
        super().__init__()
        self._initd   = True
        self._active  = True
        self._context = context
        self.start()
        
        # Block until the thread is past its initialization stage
        while self._initd:
            time.sleep(self.REFRESH/1000)
    
    def _poll(self):
        """
        Processes an update as part of the main loop.
        
        The method is registered with the after() command and reregisters itself to
        keep itself active.  Its primary purpose is to poll the application context.
        """
        if not self._active:
            self._root.quit()
        else:
            self._context._tk_update()
        
        self._root.after(self.REFRESH,self._poll)
    
    def run(self):
        """
        Runs the main Tkinter thread.
        
        This thread will continue until the Tk main loop is disposed.
        """
        import tkinter as tk
        
        # The root window is not useful (other than being active).  Hide it
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW",self.dispose)
        label = tk.Label(root,text='Root App')
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (1, 1, w, h))
        self._root = root
        
        self._context._root = root
        self._initd = False
        
        self._root.after(self.REFRESH,self._poll)
        self._root.mainloop()
        self._root.destroy()
    
    def dispose(self):
        """
        Disposes of this Tkinter thread
        
        This command will cause the thread to exit the main loop after the next
        loop iteration. The object can be safely garbage collected.
        """
        self._active = False


class _AsyncContext(object):
    """
    An instance is an asynchronized Tkinter application context for Windows/Linux.
    
    An application context is used to allocate all Tkinter objects, ensuring that they
    are in the proper thread. It is also used to force refreshes of the graphics
    state.
    
    Since there can only be one Tkinter application at a timem this is a singleton
    class.  The only and only object should be accessed through the ``instance()``
    classmethod.
    
    Asynchronized contexts are processed in a seperate thread, because the mainloop
    is required and not optional on these platforms. The main thread communicates
    with the context via shared queues (and locks).
    """
    
    # The singleton instance
    _INSTANCE = None
    
    # The size of the bevel border
    _BORDER  = 3
    # The size of the pre-bevel padding
    _PADDING = 7
    
    @classmethod
    def Instance(cls):
        """
        Returns the single instance, allocating the instance if necessary.
        
        :return: The singleton context instance
        :rtype:  ``_SyncContext``
        """
        if not cls._INSTANCE:
            cls._INSTANCE = cls()
        return cls._INSTANCE
    
    def __init__(self):
        """
        Creates a new Tkinter application context.
        
        This context will allocate the Tkinter ojects in a separate thread.
        """
        self._root = None
        self._bkgd = None
        self._window = {}
        self._create = []
        self._delete = []
        self._lock = threading.Lock()
    
    def alloc(self,obj,x,y,width,height):
        """
        Allocates a new window object with the given dimensions.
        
        This method does not return a window object, since some contexts must perform
        this allocation asynchronously.  Instead, allocates the Tkinter child components
        and stores them in the previously allocated ``:class:Window`` object ``window``.
        Hence the ``Window`` object can request allocation and then block until it is
        complete.
        
        :param window: The window to store the allocated Tkinter components
        :type window:  ``Window``
        
        :param x: initial x coordinate
        :type x: ``int`` >= 0
        
        :param y: initial y coordinate
        :type y: ``int`` >= 0
        
        :param width: initial window width
        :type width: ``int`` > 0
        
        :param height: initial window height
        :type height: ``int`` > 0
        """
        if not self._bkgd:
            self._bkgd = _TK_Thread(self)
        
        with self._lock:
            self._create.append((obj,x,y,width,height))
        
        while not obj._active:
            pass
    
    def dealloc(self,obj):
        """
        Deallocates a window object.
        
        This method does not guarantee that the window is disposed of immediately.  Instead
        it queues up a request to dispose the window via its ``_tk_dispose()`` method,
        ensuring that this method is called in the proper Tk thread.
        
        :param window: The window to deallocate
        :type window:  ``Window``
        """
        with self._lock:
            self._delete.append(obj._tkkey)
    
    def refresh(self):
        """
        Forces a refresh of the graphics state.
        
        This method is unused for the asynchronous context, and exists only for
        compatibility reasons.
        """
        pass
    
    def dispose(self):
        """
        Disposes this application context.
        
        As this class is a singleton, this method should never be called before
        Python exits.
        """
        with self._lock:
            self._window.clear()
            self._create.clear()
            self._delete.clear()
            self._bkgd.dispose()
            self._bkgd = None
            self._root = None

    def isasync(self):
        """
        :return: True if this is an asynchronous context; otherwise False
        :rtype:  ``bool``
        """
        return True

    def _tk_update(self):
        with self._lock:
            for key in self._window:
                self._window[key]._tk_update()
            for key in self._delete:
                self._window[key]._tk_dispose()
                del self._window[key]
            self._delete.clear()
            for item in self._create:
                self._pack(*item)
                self._window[item[0]._tkkey] = item[0]
            self._create.clear()
            if len(self._window) == 0 and self._bkgd:
                self._bkgd.dispose()
                self._bkgd = None
                self._root = None
    
    def _pack(self,window,x,y,width,height):
        """
        Asynchronously allocates a new window object with the given dimensions.
        
        This method is the callback to an allocation request.  It executes in the 
        Tkinter thread.
        
        :param window: The window to store the allocated Tkinter components
        :type window:  ``Window``
        
        :param x: initial x coordinate
        :type x: ``int`` >= 0
        
        :param y: initial y coordinate
        :type y: ``int`` >= 0
        
        :param width: initial window width
        :type width: ``int`` > 0
        
        :param height: initial window height
        :type height: ``int`` > 0
        """
        import tkinter as tk
        toplev = tk.Toplevel(self._root)
        toplev.title(window._title)
        toplev.protocol("WM_DELETE_WINDOW",window.dispose)
        outer  = tk.Frame(toplev, padx=self._PADDING, pady=self._PADDING,highlightthickness=0)
        inner  = tk.Frame(outer,  borderwidth=self._BORDER, relief=tk.SUNKEN,highlightthickness=0)
        canvas = tk.Canvas(inner, width=width, height=height, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=tk.YES)
        inner.pack(fill=tk.BOTH,  expand=tk.YES)
        outer.pack(fill=tk.BOTH,  expand=tk.YES)
        
        toplev.geometry( '+%d+%d' % (x,y))
        self._root.update()
        
        # We need some extra state to handle resizing weirdness
        canvas._dw = toplev.winfo_width()-canvas.winfo_width()
        canvas._dh = toplev.winfo_height()-canvas.winfo_height()
        canvas._lastw = canvas.winfo_width()
        canvas._lasth = canvas.winfo_height()
        canvas._currw = canvas._lastw
        canvas._currh = canvas._lasth
        
        outer.bind("<Configure>", window._tk_resize)
        window._window = toplev
        window._panels = outer
        window._canvas = canvas
        window._active = True
        self._window[window._tkkey] = window


class _SyncContext(object):
    """
    An instance is a synchronized Tkinter application context for MacOS.
    
    An application context is used to allocate all Tkinter objects, ensuring that they
    are in the proper thread. It is also used to force refreshes of the graphics
    state.
    
    Since there can only be one Tkinter application at a timem this is a singleton
    class.  The only and only object should be accessed through the ``instance()``
    classmethod.
    
    Synchronized contexts are processed all in the main thread, because MacOS always 
    has an implicit event loop for the window objects.  However, the context still
    presents itself as an asychronous event queue for abstraction purposes.
    """
    
    # The singleton instance
    _INSTANCE = None
    
    # The size of the bevel border
    _BORDER  = 3
    # The size of the pre-bevel padding
    _PADDING = 7
    
    @classmethod
    def Instance(cls):
        """
        Returns the single instance, allocating the instance if necessary.
        
        :return: The singleton context instance
        :rtype:  ``_SyncContext``
        """
        if not cls._INSTANCE:
            cls._INSTANCE = cls()
        return cls._INSTANCE
    
    def __init__(self):
        """
        Creates a new Tkinter application context.
        
        This context will allocate the Tkinter ojects in the main thread.
        """
        import tkinter as tk
        self._root = None
        self._bkgd = None
        self._window = {}
        self._create = []
        self._delete = []
        
        # The root window is not useful (other than being active).  Hide it
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW",self.dispose)
        label = tk.Label(root,text='Root App')
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (1, 1, w, h))
        self._root = root
    
    def alloc(self,window,x,y,width,height):
        """
        Allocates a new window object with the given dimensions.
        
        This method does not return a window object, since some contexts must perform
        this allocation asynchronously.  Instead, allocates the Tkinter child components
        and stores them in the previously allocated ``:class:Window`` object ``window``.
        Hence the ``Window`` object can request allocation and then block until it is
        complete.
        
        :param window: The window to store the allocated Tkinter components
        :type window:  ``Window``
        
        :param x: initial x coordinate
        :type x: ``int`` >= 0
        
        :param y: initial y coordinate
        :type y: ``int`` >= 0
        
        :param width: initial window width
        :type width: ``int`` > 0
        
        :param height: initial window height
        :type height: ``int`` > 0
        """
        import tkinter as tk
        toplev = tk.Toplevel(self._root)
        toplev.title(window._title)
        toplev.protocol("WM_DELETE_WINDOW",window.dispose)
        outer  = tk.Frame(toplev, padx=self._PADDING, pady=self._PADDING,highlightthickness=0)
        inner  = tk.Frame(outer,  borderwidth=self._BORDER, relief=tk.SUNKEN,highlightthickness=0)
        canvas = tk.Canvas(inner, width=width, height=height, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=tk.YES)
        inner.pack(fill=tk.BOTH,  expand=tk.YES)
        outer.pack(fill=tk.BOTH,  expand=tk.YES)
        
        toplev.geometry( '+%d+%d' % (x,y))
        self.refresh()
        
        # We need some extra state to handle resizing weirdness
        canvas._dw = toplev.winfo_width()-canvas.winfo_width()
        canvas._dh = toplev.winfo_height()-canvas.winfo_height()
        canvas._lastw = canvas.winfo_width()
        canvas._lasth = canvas.winfo_height()
        canvas._currw = canvas._lastw
        canvas._currh = canvas._lasth
        
        #canvas.bind("<Configure>", window._tk_resize)
        outer.bind("<Configure>", window._tk_resize)
        window._window = toplev
        window._panels = outer
        window._canvas = canvas
        window._active = True
        self._window[window._tkkey] = window
    
    def dealloc(self,window):
        """
        Deallocates a window object.
        
        This method does not guarantee that the window is disposed of immediately.  Instead
        it queues up a request to dispose the window via its ``_tk_dispose()`` method,
        ensuring that this method is called in the proper Tk thread.
        
        :param window: The window to deallocate
        :type window:  ``Window``
        """
        try:
            del self._window[window._tkkey]
            window._tk_dispose()
        except:
            pass
    
    def refresh(self):
        """
        Forces a refresh of the graphics state.
        
        This method is unused for the asynchronous context, and exists only for
        compatibility reasons.
        """
        for key in self._window:
            self._window[key]._tk_update()
        self._root.update()
    
    def dispose(self):
        """
        Disposes this application context.
        
        As this class is a singleton, this method should never be called before
        Python exits.
        """
        self._root.destroy()

    def isasync(self):
        """
        :return: True if this is an asynchronous context; otherwise False
        :rtype:  ``bool``
        """
        return False



# Produce the correct context
if hasattr(os,'uname') and os.uname().sysname=='Darwin':
    _Context = _SyncContext
else:
    _Context = _AsyncContext

