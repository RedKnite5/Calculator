# -*- coding: utf-8 -*-

'''
Tkinter tests for re_calc.

Calculator_tkinter_testing.py
'''

import unittest
import tkinter as tk

import re_calc as c


class test_history_length_changing(unittest.TestCase):
	
	def setUp(self):
		self.original_hist_len = c.hist_len		

	def test_change_hist_len(self):
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, "20")
		self.root.update()
		c.change_hist_len(self.entry, self.root)
		self.assertEqual(c.hist_len, 20)
		self.assertEqual(c.options[3], 20)
		
	def test_float_input(self):
		self.test_change_hist_len()
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, 49.5)
		self.root.update()

		pre_hist_len = c.hist_len
		c.change_hist_len(self.entry, self.root)
		self.assertEqual(c.hist_len, pre_hist_len)
		self.assertEqual(c.options[3], pre_hist_len)
		self.root.destroy()
		
	def test_other_string(self):
		self.test_change_hist_len()
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, "hello")
		self.root.update()

		pre_hist_len = c.hist_len
		c.change_hist_len(self.entry, self.root)
		self.assertEqual(c.hist_len, pre_hist_len)
		self.assertEqual(c.options[3], pre_hist_len)
		self.root.destroy()
		
	def test_string_int(self):
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, "50")
		self.root.update()
		c.change_hist_len(self.entry, self.root)
		self.assertEqual(c.hist_len, 50)
		self.assertEqual(c.options[3], 50)
		
	def tearDown(self):
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, self.original_hist_len)
		self.root.update()
		c.change_hist_len(self.entry, self.root)

		
class test_change_der_approx(unittest.TestCase):

	def setUp(self):
		self.original_der_approx = c.der_approx

	def test_change_der_approx_float(self):
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, ".002")
		self.root.update()
		
		c.change_der_approx(self.entry, self.root)
		self.assertEqual(c.der_approx, .002)
		self.assertEqual(c.options[2], .002)
		
	def test_der_approx_negative(self):
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, "-.01")
		self.root.update()
		pre_der_approx = c.der_approx
		
		c.change_der_approx(self.entry, self.root)
		self.assertEqual(c.der_approx, pre_der_approx)
		self.assertEqual(c.options[2], pre_der_approx)
		self.root.destroy()
		
	def test_der_approx_random_string(self):
		self.root = tk.Tk()
		self.entry = tk.Entry(self.root)
		self.root.update()
		self.entry.delete(0, "end")
		self.entry.insert(0, "word")
		self.root.update()
		pre_der_approx = c.der_approx

		c.change_der_approx(self.entry, self.root)
		self.assertEqual(c.der_approx, pre_der_approx)
		self.assertEqual(c.options[2], pre_der_approx)
		self.root.destroy()


class test_change_graph_win_set(unittest.TestCase):
	pass


class test_graph(unittest.TestCase):
	
	def test_create_graph(self):
		g = c.graph(xmin = -1, xmax = 1, ymin = 2, ymax = 3,
			wide = 40, high = 50)
		self.assertEqual(g.xmin, -1)
		self.assertEqual(g.xmax, 1)
		self.assertEqual(g.ymin, 2)
		self.assertEqual(g.ymax, 3)
		self.assertEqual(g.wide, 40)
		self.assertEqual(g.high, 50)
		g.root.destroy()
	
	def test_close_while_graphing(self):
		g = c.graph(xmin = -1, xmax = 1, ymin = 2, ymax = 3,
			wide = 40, high = 50)
		g.draw("1")
		g.root.destroy()
		
	def test_graph_partial_undefined(self):
		g = c.graph(xmin = -1, xmax = 1, ymin = 2, ymax = 3,
			wide = 40, high = 50)
		g.draw("x**.5")
		g.root.destroy()

		
class test_polar_graph(unittest.TestCase):
	
	def test_create_graph(self):
		g = c.polar_graph(xmin = -1, xmax = 1, ymin = 2, ymax = 3,
			theta_min = -2, theta_max = 6, wide = 40, high = 50)
		self.assertEqual(g.xmin, -1)
		self.assertEqual(g.xmax, 1)
		self.assertEqual(g.ymin, 2)
		self.assertEqual(g.ymax, 3)
		self.assertEqual(g.theta_min, -2)
		self.assertEqual(g.theta_max, 6)
		self.assertEqual(g.wide, 40)
		self.assertEqual(g.high, 50)
		g.root.destroy()
	
	def test_close_while_graphing(self):
		g = c.polar_graph(xmin = -1, xmax = 1, ymin = 2, ymax = 3,
			theta_min = -.5, theta_max = .5, wide = 40, high = 50)
		g.draw("1")
		g.root.destroy()
		
	def test_graph_partial_undefined(self):
		g = c.polar_graph(xmin = -1, xmax = 1, ymin = 2, ymax = 3,
			theta_min = -.5, theta_max = .5, wide = 40, high = 50)
		g.draw("x**.5")
		g.root.destroy()

		
class test_graph_function(unittest.TestCase):
	
	def setUp(self):
		self.mode = c.polar_mode
		c.switch_polar_mode(False)
		
	def test_basic_graph(self):
		g = c.graph_function("x")
		g.root.destroy()
		
	def test_graph_from(self):
		g = c.graph_function("x from 10 to 11")
		g.root.destroy()
		
	def test_multiple_graphs(self):
		g = c.graph_function("x and 2*x")
		g.root.destroy()
		
	def test_multiple_graphs_and_from(self):
		g = c.graph_function("x and 2*x from 10 to 11")
		g.root.destroy()

	def tearDown(self):
		c.switch_polar_mode(self.mode)


class test_graph_function_polar(unittest.TestCase):
	
	def setUp(self):
		self.mode = c.polar_mode
		c.switch_polar_mode(True)
		
	def test_basic_graph(self):
		g = c.graph_function("x")
		g.root.destroy()
		
	def test_graph_from(self):
		g = c.graph_function("x from 10 to 11")
		g.root.destroy()
		
	def test_multiple_graphs(self):
		g = c.graph_function("x and 2*x")
		g.root.destroy()
		
	def test_multiple_graphs_and_from(self):
		g = c.graph_function("x and 2*x from 10 to 11")
		g.root.destroy()

	def tearDown(self):
		c.switch_polar_mode(self.mode)
































if __name__ == '__main__':
    unittest.main()
