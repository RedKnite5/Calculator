#   calculator_testing.py

import unittest
import os
import tkinter as tk

import re_calc as c


class test_check_if_float(unittest.TestCase):

	def test_float(self):
		self.assertTrue(c.check_if_float(3.4))

	def test_int_type(self):
		self.assertTrue(c.check_if_float(4))

	def test_string_type(self):
		self.assertTrue(c.check_if_float("3.4"))

	def test_word(self):
		self.assertFalse(c.check_if_float("hello"))

	def test_int_string(self):
		self.assertTrue(c.check_if_float("2"))

	def test_mixed(self):
		self.assertFalse(c.check_if_float("sin(3.14)"))

	def test_parrentheses(self):
		self.assertFalse(c.check_if_float("(5)"))
		
	def test_list_type(self):
		self.assertFalse(c.check_if_float([2]))

class test_files(unittest.TestCase):
	
	def test_main_path(self):
		self.assertTrue(os.path.exists(c.calc_path))
		
	def test_picked_data(self):
		self.assertTrue(
		os.path.isfile(os.path.join(c.calc_path, "re_calc_info.txt")))
		
	def test_tkinter_icon(self):
		self.assertTrue(
		os.path.isfile(os.path.join(c.calc_path, "calc_pic.ico")))
		

class test_switch_degree_mode(unittest.TestCase):
	
	def setUp(self):
		self.original_degree_mode = c.degree_mode
	
	def test_set_degree_mode(self):
		c.switch_degree_mode(2)
		self.assertEqual(c.degree_mode, 2)
		self.assertEqual(c.options[0], 2)
		
	def test_set_radian_mode(self):
		c.switch_degree_mode(0)
		self.assertEqual(c.degree_mode, 0)
		self.assertEqual(c.options[0], 0)
		
	def test_set_degree_mode_string(self):
		c.switch_degree_mode("degree")
		self.assertEqual(c.degree_mode, 2)
		self.assertEqual(c.options[0], 2)
		
	def test_set_radian_mode_string(self):
		c.switch_degree_mode("radian")
		self.assertEqual(c.degree_mode, 0)
		self.assertEqual(c.options[0], 0)
		
	def test_set_not_option(self):
		with self.assertRaises(ValueError):
			c.switch_degree_mode(1)
			
	def test_set_to_random_word(self):
		with self.assertRaises(ValueError):
			c.switch_degree_mode("random")
		
	def tearDown(self):
		c.switch_degree_mode(self.original_degree_mode)


class test_switch_polar_cartesian(unittest.TestCase):
	
	def setUp(self):
		self.original_graphing_mode = c.polar_mode
		
	def test_set_polar(self):
		c.switch_polar_mode("polar")
		self.assertEqual(c.polar_mode, True)
		self.assertEqual(c.options[1], True)
		
	def test_set_cartesian(self):
		c.switch_polar_mode("Cartesian")
		self.assertEqual(c.polar_mode, False)
		self.assertEqual(c.options[1], False)
		
	def test_set_polar_boolean(self):
		c.switch_polar_mode(True)
		self.assertEqual(c.polar_mode, True)
		self.assertEqual(c.options[1], True)
		
	def test_set_cartesian_boolean(self):
		c.switch_polar_mode(False)
		self.assertEqual(c.polar_mode, False)
		self.assertEqual(c.options[1], False)
		
	def test_set_not_option(self):
		with self.assertRaises(ValueError):
			c.switch_polar_mode(4)
			
	def tearDown(self):
		c.switch_polar_mode(self.original_graphing_mode)
	

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
	

class test_find_match(unittest.TestCase):
	
	def test_basic_functionality(self):
		self.assertEqual(
		c.find_match("(inside)outside"), ('(inside)', 'outside'))
		
	def test_extra_parentheses(self):
		self.assertEqual(
		c.find_match("((inside)))"), ('((inside))', ')'))
		
	def test_mismatched_parentheses_left(self):
		with self.assertRaises(ValueError):
			c.find_match("(word")
			
	def test_mismatched_parentheses_right(self):
		with self.assertRaises(ValueError):
			c.find_match("word)")

class test_brackets_function(unittest.TestCase):
	
	def test_matched_brackets(self):
		self.assertTrue(c.brackets(""))
		self.assertTrue(c.brackets("()"))
		self.assertTrue(c.brackets("(())"))
		self.assertTrue(c.brackets("(()())"))
		self.assertTrue(c.brackets("((word)(other)word)"))
		
	def test_unmatched_brackets(self):
		self.assertFalse(c.brackets("("))
		self.assertFalse(c.brackets(")"))
		self.assertFalse(c.brackets(")("))
		self.assertFalse(c.brackets("(()words"))
		
class test_separate(unittest.TestCase):
	
	def test_split_no_parentheses(self):
		self.assertEqual(c.separate("(2, 4, 5, 6)"), ("2","4","5","6"))
		
	


















if __name__ == '__main__':
    unittest.main()
