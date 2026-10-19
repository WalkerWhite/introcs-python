"""Headless checks for dash geometry and queued drawing groups."""
import math
import unittest
from introcs.turtle._dash import dash_runs, shape_path
from introcs.turtle.window import Window


class Canvas:
    def __init__(self, platform='win32'):
        self.tk = self
        self.platform = platform
        self.items = []

    def call(self,*args):
        return self.platform

    def create_line(self,*coords,**kw):
        self.items.append(('line',coords,kw))
        return len(self.items)

    def create_rectangle(self,*coords,**kw):
        self.items.append(('rectangle',coords,kw))
        return len(self.items)

    def delete(self,tag):
        self.items = [item for item in self.items if tag not in item[2].get('tags',())]


class DashTest(unittest.TestCase):
    def test_prefixes(self):
        for length,expected in ((30,[[0,0,30,0]]),(75,[[0,0,50,0]]),
                                (125,[[0,0,50,0],[100,0,125,0]]),
                                (200,[[0,0,50,0],[100,0,150,0]])):
            self.assertEqual(list(dash_runs([0,0,length,0],(50,50))),expected)

    def test_corner_and_zero_segment(self):
        self.assertEqual(list(dash_runs([0,0,0,0,30,0,30,40],(50,50))),
                         [[0,0,30,0,30,20]])

    def test_diagonal_and_odd_pattern(self):
        runs = list(dash_runs([0,0,120,160],(50,)))
        self.assertEqual(runs,[[0,0,30,40],[60,80,90,120]])
        self.assertEqual(list(dash_runs([0,0,100,0],(50,50),25)),
                         [[0,0,25,0],[75,0,100,0]])

    def test_arc_prefix_and_closure(self):
        opts = {'style':'arc','start':20,'extent':90}
        first = shape_path('arc',[0,0,200,100],opts)
        second = shape_path('arc',[0,0,200,100],dict(opts,extent=180))
        self.assertEqual(first[:-2],second[:len(first)-2])
        oval = shape_path('oval',[0,0,200,100],{})
        self.assertEqual(oval[:2],oval[-2:])

    def test_history_group(self):
        # Avoid constructing a Tk window or running Window.__del__.
        class Harness:
            _tk_internal_create_shape = Window._tk_internal_create_shape
        window = Harness()
        window._canvas = Canvas()
        tag = window._tk_internal_create_shape('line',[0,0,200,0],{'dash':(50,50)})
        self.assertEqual(len(window._canvas.items),2)
        self.assertTrue(all(tag in item[2]['tags'] for item in window._canvas.items))
        window._history = {'tool':[tag]}
        Window._tk_internal_delete_history(window,'tool',1)
        self.assertEqual(window._canvas.items,[])
        self.assertEqual(window._history['tool'],[])

    def test_fill_and_native_fallback(self):
        class Harness:
            _tk_internal_create_shape = Window._tk_internal_create_shape
        window = Harness()
        window._canvas = Canvas()
        tag = window._tk_internal_create_shape('rectangle',[0,0,200,100],
                  {'dash':(50,50),'fill':'blue','outline':'red'})
        self.assertEqual(window._canvas.items[0][2]['outline'],'')
        self.assertTrue(all(tag in item[2]['tags'] for item in window._canvas.items))
        window._canvas.delete(tag)
        self.assertEqual(window._canvas.items,[])
        window._canvas = Canvas('aqua')
        window._tk_internal_create_shape('line',[0,0,200,0],{'dash':(50,50)})
        self.assertEqual(window._canvas.items[0][2]['dash'],(50,50))


if __name__ == '__main__':
    unittest.main()
