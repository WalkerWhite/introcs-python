"""
Unit test for turtle package

It is impossible to have automated tests for this package.  But we can at least draw
on the screen for the user to prevent issues like we had with release 2.0.

:author:  Walker M. White (wmw2)
:version: August 20, 2019
"""
import unittest
import numpy
from introcs.turtle import *


class TurtleTest(unittest.TestCase):
    """
    Unit test for the turtle package
    """
    
    def setUp(self):
        """
        Initializes a unit test (UNUSED)
        """
        self.window = Window()
        self.turtle = Turtle(self.window)
        self.turtle.speed = 4
        self.turtle.color = "red"
    
    def tearDown(self):
        """
        Completes a unit test (UNUSED)
        """
        self.window.clear()
        self.window.dispose()
    
    def test01_spiral(self):
        """
        Tests the urlread function.
        """
        self.turtle.clear()
        
        ang = 100
        side = 10
        for x in range(20):
            self.turtle.forward((x+1)*side)
            self.turtle.left(ang)
            if x % 3 == 0:
                self.turtle.color = "blue"
            if x % 3 == 1:
                self.turtle.color = "red"
            if x % 3 == 2:
                self.turtle.color = "green"


if __name__=='__main__':
  unittest.main( )
