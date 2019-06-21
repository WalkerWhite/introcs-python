"""
A module to draw cool shapes with the introcs Turtle.

The module can be run as a script to show off the various functions. Unimplemented 
functions will do nothing.

Authors: Walker White (WMW2) and Lillian Lee (LJL2)
Date: Oct 10, 2018
"""
from introcs.turtle import Window, Turtle, Pen
import introcs  # For the RGB and HSV objects
import math     # For the math computations


################# Helpers for Precondition Verification #################

def is_number(x):
    """
    Returns: True if value x is a number; False otherwise.
    
    Parameter x: the value to check
    Precondition: NONE (x can be any value)
    """
    return type(x) in [float, int]


def is_window(w):
    """
    Returns: True if w is a cornell Window; False otherwise.
    
    Parameter w: the value to check
    Precondition: NONE (w can be any value)
    """
    return type(w) == Window


def is_valid_color(c):
    """
    Returns: True c is a valid turtle color; False otherwise
    
    Parameter c: the value to check
    Precondition: NONE (c can be any value)
    """
    return (type(c) == introcs.RGB or type(c) == introcs.HSV or
            (type(c) == str and (introcs.is_tkcolor(c) or introcs.is_webcolor(c))))


def is_valid_speed(sp):
    """
    Returns: True if sp is an int in range 0..10; False otherwise.
    
    Parameter sp: the value to check
    Precondition: NONE (sp can be any value)
    """
    return (type(sp) == int and 0 <= sp and sp <= 10)


def is_valid_length(side):
    """
    Returns: True if side is a number >= 0; False otherwise.
    
    Parameter side: the value to check
    Precondition: NONE (side can be any value)
    """
    return (is_number(side) and 0 <= side)


def is_valid_iteration(n):
    """
    Returns: True if n is an int >= 1; False otherwise.
    
    Parameter n: the value to check
    Precondition: NONE (n can be any value)
    """
    return (type(n) == int and 1 <= n)


def is_valid_depth(d):
    """
    Returns: True if d is an int >= 0; False otherwise.
    
    Parameter d: the value to check
    Precondition: NONE (d can be any value)
    """
    return (type(d) == int and d >= 0)


def is_valid_turtlemode(t):
    """
    Returns: True t is a Turtle with drawmode True; False otherwise.
    
    Parameter t: the value to check
    Precondition: NONE (t can be any value)
    """
    return (type(t) == Turtle and t.drawmode)


def is_valid_penmode(p):
    """
    Returns: True t is a Pen with solid False; False otherwise.
    
    Parameter p: the value to check
    Precondition: NONE (p can be any value)
    """
    return (type(p) == Pen and not p.solid)


def report_error(message, value):
    """
    Returns: An error message about the given value.
    
    This is a function for constructing error messages to be used in assert statements.  
    We find that students often introduce bugs into their assert statement messages, and 
    do not find them because they are in the habit of not writing tests that violate 
    preconditions.
    
    The purpose of this function is to give you an easy way of making error messages 
    without having to worry about introducing such bugs. Look at the function 
    draw_two_lines for the proper way to use it.
    
    Parameter message: The error message to display
    Precondition: message is a string
    
    Parameter value: The value that caused the error
    Precondition: NONE (value can be anything)
    """
    return message+': '+repr(value)



#################### DEMO: Two lines ####################


def draw_two_lines(w,sp):
    """
    Draws two lines on to window w.
    
    This function clears w of any previous drawings.  Then, in the middle of the window w, 
    this function draws a green line 100 pixels to the east, and then a blue line 200 
    pixels to the north.  It uses a new turtle that moves at speed sp, 0 <= sp <= 10, 
    with 1 being slowest and 10 fastest (and 0 being "instant").
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # Clear the window first!
    w.clear()
    
    # Create a turtle and draw
    t = Turtle(w)
    t.speed = sp
    t.color = 'green'
    t.forward(100) # draw a line 100 pixels in the current direction
    t.left(90)     # add 90 degrees to the angle
    t.color = 'blue'
    t.forward(200)
    
    # This is necessary if speed is 0!
    t.flush()




#################### TASK 1: Triangle ####################

def draw_triangle(t, s, c):
    """
    Draws an equilateral triangle of side s and color c at current position.
    
    The direction of the triangle depends on the current facing of the turtle.
    If the turtle is facing west, the triangle points up and the turtle starts
    and ends at the east end of the base line.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)
    
    Parameter c: The triangle color
    Precondition: c is a valid turtle color (see the helper function above)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)
    assert is_valid_color(c), report_error('Invalid color', c)
    
    # Hint: each angle in an equilateral triangle is 60 degrees.
    # Note: In this function, DO NOT save the turtle position and heading
    # in the beginning and then restore them at the end. The turtle moves
    # should be such that the turtle ends up where it started and facing
    # in the same direction, automatically.
    
    # Also, 3 lines have to be drawn. Does this suggest a for loop that
    # processes the range 0..2?
    oldDraw = t.drawmode
    oldColor = t.color
    oldheading = t.heading
    
    t.color = c
    for x in range(3):
        t.forward(s)
        t.right(120)
    
    #change back to initial values
    t.color = oldColor
    t.drawmode = oldDraw
    t.heading = oldheading
    
    # This is necessary if speed is 0!
    t.flush()




#################### TASK 2: Hexagon ####################

def draw_hex(t, s):
    """
    Draws six triangles using the color 'cyan' to make a hexagon.
    
    The triangles are equilateral triangles, using draw_triangle as a helper.
    The drawing starts at the turtle's current position and heading. The
    middle of the hexagon is the turtle's starting position.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)

    # Note: Do not save any of the turtle's properties and then restore them
    # at the end. Just use 6 calls on procedures drawTriangle and t.left. Test
    # the procedure to make sure that t's final location and heading are the
    # same as t's initial location and heading (except for roundoff error).
    
    for x in range (6):
        draw_triangle(t,s,'cyan')
        t.left(60)
    
    # This is necessary if speed is 0!
    t.flush()




#################### Task 3A: Spirals ####################

def draw_spiral(w, side, ang, n, sp):
    """
    Draws a spiral using draw_spiral_helper(t, side, ang, n, sp)
    
    This function clears the window and makes a new turtle t.  This turtle
    starts in the middle of the canvas facing west (NOT the default east).
    It then calls draw_spiral_helper(t, side, ang, n, sp). When it is done,
    the turtle is left hidden (visible is False).
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.
    
    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number
    
    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_number(ang), report_error('ang is not a valid angle',ang)
    assert is_valid_iteration(n), report_error('n is not a valid number of iterations',side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # HINT: w.clear() clears window.
    # HINT: set the turtle's visible attribute to False at the end.
    w.clear()
    
    t = Turtle(w)
    t.color = 'green'
    t.right(180)
    draw_spiral_helper(t,side,ang,n,sp)
    t.visible = False
    
    # This is necessary if speed is 0!
    t.flush()


def draw_spiral_helper(t, side, ang, n, sp):
    """
    Draws a spiral of n lines at the current position and heading.
    
    The spiral begins at the current turtle position and heading, turning ang
    degrees to the left after each line.  Line 0 is side pixels long. Line 1
    is 2*side pixels long, and so on.  Hence each Line i is (i+1)*side pixels
    long. The lines alternate between green, blue, and red, in that order, with
    the first one green.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the function,
    you must change them back.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number
    
    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_number(ang), report_error('ang is not a valid angle',ang)
    assert is_valid_iteration(n), report_error('n is not a valid number of iterations',side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # NOTE: Since n lines must be drawn, use a for loop on a range of integers.
    oldDraw = t.drawmode
    oldVisible = t.visible
    oldspeed = t.speed
    t.speed = sp
    oldcolor = t.color
    
    for x in range(n):
        t.forward((x+1)*side)
        t.left(ang)
        if x % 3 == 0:
            t.color = "blue"
        if x % 3 == 1:
            t.color = "red"
        if x % 3 == 2:
            t.color = "green"
            
    #change to intial color, visibility,drawmode, and speed
    t.drawmode = oldDraw
    t.visible = oldVisible
    t.speed = oldspeed
    t.color = oldcolor


#################### TASK 3B: Polygons ####################


def multi_polygons(w, side, k, n, sp):
    """
    Draws polygons using multi_polygons_helper(t, side, k, n, sp)
    
    This function clears the window and makes a new turtle t.  This turtle starts in the 
    middle of the canvas facing north (NOT the default east). It then calls 
    multi_polygons_helper(t, side, k, n, sp). When it is done, the turtle is left 
    hidden (visible is False).
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.
    
    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1
    
    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 1
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert (type(k) == int and k >=1), report_error('k is an invalid # of polys',k)
    assert (type(n) == int and n >= 3), report_error('n is an invalid # of poly sides',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # HINT: w.clear() clears window.
    # HINT: set the turtle's visible attribute to False at the end.
    w.clear()
    
    t = Turtle(w)
    t.visible = True
    t.right(90)
    t.color = 'blue'
    multi_polygons_helper(t, side, k, n, sp)  
    t.visible = False
   
    # This is necessary if speed is 0!
    t.flush()


def multi_polygons_helper(t, side, k, n, sp):
    """
    Draws k n-sided polygons of side length s.
    
    The polygons are drawn by turtle t, starting at the current position. The turtles 
    alternate colors between blue and red. Each polygon is drawn starting at the same 
    place (within roundoff errors), but t turns left 360.0/k degrees after each polygon.
    
    At the end, ALL ATTRIBUTES of the turtle are the same as they were in the beginning 
    (within roundoff errors).  If you change any attributes of the turtle. then you must 
    restore them.  Look at the helper draw_polygon for more information.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1
    
    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 1
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert (type(k) == int and k >=1), report_error('k is an invalid # of polys',k)
    assert (type(n) == int and n >= 3), report_error('n is an invalid # of poly sides',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # HINT:  make sure that upon termination, t's color and speed are restored
    # HINT: since k polygons should be drawn, use a for-loop on a range.
    oldspeed = t.speed
    t.speed = sp
    oldcolor = t.color
    oldDraw = t.drawmode
    
    for x in range(k):
        draw_polygon(t, side, n, sp)
        t.left(360.0/k)
        if x % 2 == 0:
            t.color = 'red'
        if x % 2 == 1:
            t.color = 'blue'
    
    #restore intial values
    t.speed = oldspeed
    t.color = oldcolor
    t.drawmode = oldDraw


def draw_polygon(t, side, n, sp):
    """
    Draws an n-sided polygon using of side length side.
    
    The polygon is drawn with turtle t using speed sp.
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED: position 
    (x and y, within round-off errors), heading, color, speed, visible, and drawmode.  
    There is no need to restore these.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 1
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert type(n) == int and n >= 1, report_error('n is an invalid # of poly sides',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # Remember old speed
    oldspeed = t.speed
    t.speed = sp
    ang = 360.0/n # exterior angle between adjacent sides
    
    # t is in position and facing the direction to draw the next line.
    for _ in range(n):
        t.forward(side)
        t.left(ang)
    
    # Restore the speed
    t.speed = oldspeed


#################### TASK 3C: Radiating lines ####################

def radiate(w, side, n, sp):
    """
    Draws n straight radiating lines using radiate_helper(t, side, n, sp)
    
    This function clears the window and makes a new turtle t.  This turtle starts in the 
    middle of the canvas facing west (NOT the default east). It then calls 
    radiate_helper(t, side, n, sp). When it is done, the turtle is left hidden 
    (visible is False).
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.
    
    Parameter side: The length of each radial line
    Precondition: side is a valid side length (number >= 0)
    
    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert (type(n) == int and n >= 2), report_error('n is an invalid # of lines',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # HINT: w.clear() clears window.
    # HINT: set the turtle's visible attribute to False at the end.
    w.clear()
    
    t = Turtle(w, (0,0), 'red', 180, sp)
    t.stroke=4.0
    radiate_helper(t, side, n, sp)
    t.visible = False
    
    # This is necessary if speed is 0!
    t.flush()


def radiate_helper(t, side, n, sp):
    """
    Draws n straight radiating lines of length s at equal angles.
    
    This lines are drawn using turtle t with the turtle moving at speed sp.
    A line drawn at angle ang, 0 <= ang < 360 has HSV color (ang % 360.0, 1, 1).
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED: color, speed, 
    visible, and drawmode. However, the final position and heading may be different. If 
    you changed any of these four in the function, you must change them back.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each radial line
    Precondition: side is a valid side length (number >= 0)
    
    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2
    
    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert (type(n) == int and n >= 2), report_error('n is an invalid # of lines',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    # Preserve the color and speed
    oldcolor = t.color
    oldspeed = t.speed
    
    # Notes:
    # 1. Drawing n lines should be done with a loop that processes
    #    a certain range of integers.
    # 2. You should keep the heading of the turtle in the range
    #    0 <= heading < 360.
    # 3. (t.heading % 360.0, 1, 1) is an HSV representation of the color
    #    determined by turtle t's heading.
    # 4. You can use an HSV object for the turtle's color attribute,
    #    even though all the examples use strings with color names
    
    for i in range(n):
        t.color = introcs.HSV(t.heading % 360.0, 1.0, 1.0)
        t.forward(side)
        t.backward(side)
        t.left(360.0/n)
    
    # Restore the original values
    t.color = oldcolor
    t.speed = oldspeed




#################### TASK 4A: Cantor Stool ####################

def cantor(w, side, hght, d, sp):
    """
    Draws a Cantor Stool of dimensions side x hght, and depth d.
    
    This function clears the window and makes a new graphics pen p.  This
    pen starts in the middle of the canvas at (0,0). It draws by calling
    the function cantor_helper(p, 0, 0, side, hght, d). The pen is visible
    during drawing and should be set to hidden at the end.
    
    The pen should have a fill color of red and a line color of black.
    
    REMEMBER: You need to flush the pen if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a tkturtle Window object.
    
    Parameter side: The width of the Cantor stool
    Precondition: side is a valid side length (number >= 0)
    
    Parameter hght: The height of the Cantor stool
    Precondition: hght is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the stool
    Precondition: n is a valid depth (int >= 0)
    
    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_length(hght), report_error('hght is not a valid length',hght)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)
    
    w.clear()
    
    p = Pen(w, (0,0), 'black', 'red', sp)
    p.visible = True
    
    cantor_helper(p, 0, 0, side, hght, d)
    p.visible = False
    
    # This is necessary if speed is 0!
    p.flush()


def cantor_helper(p, x, y, side, hght, d):
    """
    Draws a stool of dimensions side x hght, and depth d centered at (x,y)
    
    The stool is draw with the current pen color and visibility attribute.
    Follow the instructions on the course website to recursively draw the
    Cantor stool.
    
    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.
    
    Parameter x: The x-coordinate of the stool center
    Precondition: x is a number
    
    Parameter y: The y-coordinate of the stool center
    Precondition: y is a number
    
    Parameter side: The width of the Cantor stool
    Precondition: side is a valid side length (number >= 0)
    
    Parameter hght: The height of the Cantor stool
    Precondition: hght is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the stool
    Precondition: n is a valid depth (int >= 0)
    """
    # Assert the preconditions
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('x is not a valid position',y)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_length(hght), report_error('hght is not a valid length',hght)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    
    if (d == 0):
        fill_rect(p,x,y,side,hght)
    elif (d > 0):
        cantor_helper(p,x-side/3.0,y-hght/4.0,side/3.0,hght/2.0,d-1)
        cantor_helper(p,x+side/3.0,y-hght/4.0,side/3.0,hght/2.0,d-1)
        fill_rect(p,x,y+hght/4.0,side,hght/2.0)


# DO NOT MODIFY
def fill_rect(p, x, y, side, hght):
    """
    Fills a rectangle of lengths side, hght with center (x, y) using pen p.
    
    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.
    
    Parameter x: The x-coordinate of the rectangle center
    Precondition: x is a number
    
    Parameter y: The y-coordinate of the rectangle center
    Precondition: y is a number
    
    Parameter side: The width of the rectangle
    Precondition: side is a valid side length (number >= 0)
    
    Parameter hght: The height of the rectangle
    Precondition: hght is a valid side length (number >= 0)
    """
    # Precondition assertions omitted
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('x is not a valid position',y)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_length(hght), report_error('hght is not a valid length',hght)
    
    # Move to the center and draw
    p.move(x - side/2.0, y - hght/2.0)
    p.solid = True
    p.drawLine(    0,  hght)
    p.drawLine( side,     0)
    p.drawLine(    0, -hght)
    p.drawLine(-side,     0)
    p.solid = False
    p.move(x - side/2.0, y - hght/2.0)




#################### TASK 4B: T-Square ####################

def tsquare(w, side, d, sp):
    """
    Draws a 'magenta' T-Square with side length and depth d
    
    This function clears the window and makes a new graphics pen p.  This
    pen starts in the middle of the canvas at (0,0). It draws by calling
    the function tsquare_helper(p, 0, 0, side, d). The pen is visible
    during drawing and should set to hidden at the end.
    
    The pen should have both a 'magenta' fill color and a 'magenta' line color.
    
    REMEMBER: You need to flush the pen if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a tkturtle Window object.
    
    Parameter side: The side length of the t-square
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the t-square
    Precondition: n is a valid depth (int >= 0)
    
    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    w.clear()
    
    p = Pen(w, (0,0), 'magenta', 'magenta', sp)
    p.visible = True
    tsquare_helper(p, 0, 0, side, d)
    p.visible = False
    
    # This is necessary if speed is 0!
    p.flush()


def tsquare_helper(p, x, y, side, d):
    """
    Draws a T-Square with side length and depth d centered at (x,y)
    
    The t-square is draw with the current pen color and visibility attribute.
    Follow the instructions on the course website to recursively draw the
    T-Square.
    
    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.
    
    Parameter x: The x-coordinate of the t-square center
    Precondition: x is a number
    
    Parameter y: The y-coordinate of the t-square center
    Precondition: y is a number
    
    Parameter side: The side-length of the t-square
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the t-square
    Precondition: n is a valid depth (int >= 0)
    """
    # Assert the preconditions
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('x is not a valid position',y)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    
    # HINT: Use fill_rect from Task 4A
    if (d != 0):
        h = side/2.0
        tsquare_helper(p,x-h,y-h,h,d-1)
        tsquare_helper(p,x-h,y+h,h,d-1)
        tsquare_helper(p,x+h,y+h,h,d-1)
        tsquare_helper(p,x+h,y-h,h,d-1)
    
    fill_rect(p, x, y, side, side)


#################### TASK 5:Koch Snowflake ####################

def snowflake(w, side, d, sp):
    """
    Draws a Koch snowflake with the given side length and depth d.
    
    This function clears the window and makes a new turtle T.  This turtle starts in 
    lower left corner of the equaliteral triangle centered at (0,0) with side length
    side.  It draws by calling the function snowflake_edge(t, side, d) three times, 
    rotating the turtle after each call, just as you did in draw_triangle.
    
    The turtle should be visible while drawing, but hidden at the end. The turtle color 
    is 'blue'.
    
    REMEMBER: You need to flush the turtle if the speed is 0.
    
    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.
    
    Parameter side: The side-length of the snowflake
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the snowflake
    Precondition: n is a valid depth (int >= 0)
    
    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is not a valid length',side)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    
    # HINT: Remember to make the Turtle visible while drawing
    w.clear()
    
    height = side/(math.sqrt(3)*2)
    width  = side/2
    
    t = Turtle(w, (-width, -height), 'blue', 60, sp)
    t.visible = True
    
    snowflake_edge(t, side, d)
    t.right(120)
    snowflake_edge(t, side, d)
    t.right(120)
    snowflake_edge(t, side, d)
    t.right(120)
    t.visible = False
    
    # This is necessary if speed is 0!
    t.flush()


def snowflake_edge(t, side, d):
    """
    Draws a single Koch edge with length side and depth d at the current position and angle.
    
    The edge is draw with the current turtle color.  You should make no assumptions of
    the current angle of the turtle (e.g. use left and right to turn; do not set the
    heading).
    
    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the function,
    you must change them back.
    
    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.
    
    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)
    
    Parameter d: The recursive depth of the edge
    Precondition: n is a valid depth (int >= 0)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is not a valid length',hght)
    assert is_valid_depth(d), report_error('d is not a valid depth',d)
    
    if d == 0:
        t.forward(side)
    else:
        # Split the side into 3 parts
        part = side/3
        snowflake_edge(t, part, d-1)
        t.left(60)
        snowflake_edge(t, part, d-1)
        t.right(120)
        snowflake_edge(t, part, d-1)
        t.left(60)
        snowflake_edge(t, part, d-1)



################ Test Functions #################

def prompt(func):
    """
    Returns: The answer to a yes or no question.
    
    If the answer is invalid, it is treated as no.
    
    Parameter func: The function to ask about
    Precondition: func is string
    """
    ans = input('Call '+func+'? [y/n]: ')
    return ans.strip().lower() == 'y'


def depth(func):
    """
    Returns: The answer to a (recursion) depth question.
    
    If the anwser is invalid, it is treated as -1.
    
    Parameter func: The function to ask about
    Precondition: func is string
    """
    ans = input('Function '+func+' depth? [-1 to skip]: ')
    try:
        return int(ans.strip())
    except:
        return -1


def main():
    """
    Runs each of the functions, allowing user to skip functions.
    """
    w = Window()
    
    # Change me to get different speeds
    speed = 0
    
    if prompt('draw_two_lines'):
        draw_two_lines(w,5)
    
    if prompt('draw_triangle'):
        w.clear()
        turt = Turtle(w)
        turt.speed = speed
        draw_triangle(turt,50,'orange')
    
    if prompt('draw_hex'):
        w.clear()
        turt = Turtle(w)
        turt.speed = speed
        draw_hex(turt,50)
    
    if prompt('draw_spiral'):
        draw_spiral(w, 1, 24, 64, speed)
    
    if prompt('multi_polygons'):
        multi_polygons(w, 100, 5, 6, speed)
    
    if prompt('radiate'):
        #radiate(w, 150, 45, speed)
        radiate(w, 150, 300, speed)
    
    d = depth('cantor')
    if d >= 0:
        cantor(w, 200, 200, d, speed)
    
    d = depth('t-square')
    if d >= 0:
        tsquare(w, 200, d, speed)
    
    d = depth('snowflake')
    if d >= 0:
        snowflake(w, 200, d, speed)
    
    # Pause for the final image
    input('Press <return>')


# Application code
if __name__ == '__main__':
    main()
