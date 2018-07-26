from .window import Window
from .turtle import Turtle
from .pentool import Pen
from ._context import _Context
import gc,sys

def test_turtle():
    w = Window()
    t = Turtle(w)
    t.speed = 3
    t.stroke = 3
    t.dash = (10,10)
    print(w.turtles)
    print(w.pens)
    input('Press return')
    t.forward(100)
    t.right(90)
    t.forward(100)
    input('Press return')
    t.color = 'blue'
    t.backward(200)
    input('Press return')
    t.clear()
    t.dash = None
    input('Press return')
    t.forward(200)
    input('Press return')
    w.clear()
    input('Press return')
    w.dispose()

def test_pen():
    w = Window()
    t = Pen(w)
    t.speed = 3
    t.stroke = 3
    t.dash = (10,10)
    print(w.turtles)
    print(w.pens)
    input('Press return')
    t.drawTo(100,100)
    t.solid = True
    input('Press return')
    t.drawLine(0,100)
    t.drawLine(100,0)
    t.drawLine(0,-100)
    input('Press return')
    t.fillcolor = 'green'
    input('Press return')
    t.move(-100,-100)
    t.drawOval(25,25)
    input('Press return')
    w.clear()
    input('Press return')
    w.dispose()


test_pen()
#test_turtle()