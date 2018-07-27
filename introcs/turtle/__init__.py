"""
Python Turtle Graphics

Python 3 broke the Turtle.

The Python Turtle has always been a problematic tool. By trying to be so close to the
logo model, it uses a module as a stateful singleton. This is poor design. First of all,
there is no reason to force the Turtle to be singleton.  What if you want to display
the student Turtle next to an instructor solution?  Why should that require separate
Python processes?  Furthermore, some platforms do not allow Tkinter to be run in 
multiple processes, making this impossible.  Finally, I personally have problems with
stateful modules since the way modules interact with memory and the garbage collector
is far murkier than classes; it is far better to use a classmethod pattern if you want
a singleton.

In Python 2, you could get around this problem by allowing (careful) direct access to 
the underlying clases.  But the Turtle always used Tkinter in a way that Tkinter was never 
meant to be used.  It requires that the students to be able to type Python at the same
time that the Turtle draws in a window.  Most of the time, this can only be done by 
putting Tkinter in a separate thread:

https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop

However, this is not, and has never been possible on MacOS.  MacOS requires that Tkinter
run in the main loop.  The issue is the window handler.  In Windows and Linux, the 
Window handler is explicitly run by Python.  In MacOS it is run by the OS, but sends
event messages to Python.  The end result is that if you run Tkinter on Windows or Linux
with no mainloop() running, the program will freeze and crash whenver you touch the window.

And that is exactly what happens with the Turtle in Python 3.  After getting numerous
complaints from Windows-based students that the Turtle was freezing their computers and 
crashing, we decided it was time for a new Turtle.

The old Turtle got around this by calling the update() method manually as the Turtle
moves, but not blocking on a full loop.  But outside of MacOS this causes a problem if 
the window is moved while the Turtle is not moving.  Personally, I believe that the
MacOS version is correct, and that delegating top-levelwindow commands to Python (instead 
of the OS) is a poor design decision. But it is what it is.

The end result is that there is one solution (the old approach)  that works on MacOS 
and another that works on Windows and Linux.  This new version of the Turtle creates
a hybrid solution that works seamlessly on all platforms.

This code is a massive violation of everything that we teach at Cornell.  I violate the
spirit of the Tkinter specification everywhere, and depend heavily on what Tkinter does
instead of what it is supposed to do.  The result is a Turtle that can break at any
time Tkinter is upgraded. That is why it is not automatically imported in the top level
package.  But the Turtle is a great tool for assignments, and we needed to keep it 
going for a while.

:author:  Walker M. White (wmw2)
:version: July 24, 2018
"""
from .window import Window
from .turtle import Turtle
from .pentool import Pen