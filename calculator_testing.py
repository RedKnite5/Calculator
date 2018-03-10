# -*- coding: utf-8 -*-

'''
Tests for re_calc.

calculator_testing.py
'''

import unittest
import os
import math

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
		self.assertEqual(c.separate("2,4,5,6"), ("2","4","5","6"))
		
	def test_split_parentheses(self):
		self.assertEqual(
		c.separate("3, 4, (5,6), 3"), ("3", " 4", " (5,6)", " 3"))
		
	def test_split_nested_parentheses(self):	
		self.assertEqual(
		c.separate("1, (2, 3, (4, 5), 6), 7, (8), (9, 10)"),
		("1", " (2, 3, (4, 5), 6)", " 7", " (8)", " (9, 10)"))


class test_constant_function(unittest.TestCase):
	
	def test_all_the_constants(self):
		self.assertEqual(c.constant_function("pi"), math.pi)
		self.assertEqual(c.constant_function("e"), math.e)
		self.assertEqual(c.constant_function("phi"), (1 + 5 ** 0.5) / 2)
		self.assertEqual(c.constant_function("π"), math.pi)
		self.assertEqual(c.constant_function("ans"), c.ans)
		self.assertEqual(c.constant_function("answer"), c.ans)
		self.assertEqual(c.constant_function("tau"), math.tau)
		self.assertEqual(c.constant_function("τ"), math.tau)
		self.assertEqual(c.constant_function("φ"), (1 + 5 ** 0.5) / 2)


class test_solving_equations(unittest.TestCase):

	def test_solve_with_no_equals_or_variable(self):
		self.assertEqual(c.solve_equations("x-5"), 5)

	def test_solve_with_no_equals(self):
		self.assertEqual(c.solve_equations("t-5 for t"), 5)

	def test_solve_with_no_variable(self):
		self.assertEqual(c.solve_equations("2*x = 4"), 2)

	def test_solve_with_everything(self):
		self.assertEqual(c.solve_equations("2*t = 4 for t"), 2)


class test_evaluation_function(unittest.TestCase):
	
	def test_eval_without_variable(self):
		self.assertEqual(c.evaluate_function("x", "5"), "5.0")
		
	def test_eval_with_variable(self):
		self.assertEqual(c.evaluate_function("t", "5", var = "t"), "5.0")
		
	def test_double_eval_function(self):
		self.assertEqual(
			c.evaluate_function("eval t at x for t", "4"), "4.0")


class test_find_derivative(unittest.TestCase):
	
	def test_find_basic_derivative(self):
		self.assertAlmostEqual(
			float(c.find_derivative("x^2", "3")), 6.0)

	def test_find_derivative_with_variable(self):
		self.assertAlmostEqual(
			float(c.find_derivative("t^2", "3", var = "t")), 6.0)

	def test_double_derivative(self):
		self.assertAlmostEqual(
			float(c.find_derivative("x * derivative of t^2 at 3", "1")),
			6.0)


class test_integrate_function(unittest.TestCase):
	
	def test_basic_integral(self):
		self.assertEqual(c.integrate_function("2*x", "x", "0", "3"), "9.0")

	def test_other_variables(self):
		self.assertEqual(c.integrate_function("2*r", "r", "0", "3"), "9.0")
		self.assertEqual(c.integrate_function("2*w", "w", "0", "3"), "9.0")
		self.assertEqual(c.integrate_function("2*l", "l", "0", "3"), "9.0")
		self.assertEqual(c.integrate_function("2*o", "o", "0", "3"), "9.0")

	def test_integrate_at_expression(self):
		self.assertEqual(
			c.integrate_function("2*x", "x", "0", "1+2"), "9.0")
			

class test_combinations_and_permutations(unittest.TestCase):
	
	def test_basic_combination_choose_notation(self):
		self.assertEqual(
			c.combinations_and_permutations("choose", "C", "5", "2"),
			"10.0")
		
	def test_basic_permutaion_choose_notation(self):
		self.assertEqual(
		c.combinations_and_permutations("choose", "P", "5", "2"),
		"20.0")

	def test_basic_combination_func_notation(self):
		self.assertEqual(
		c.combinations_and_permutations("func", "C", "(5,2)"),
		"10.0")

	def test_basic_permutaion_func_notation(self):
		self.assertEqual(
		c.combinations_and_permutations("func", "P", "(5,2)"),
		"20.0")

	def test_nested_combinations(self):
		self.assertEqual(
			c.combinations_and_permutations("func", "C", "(5,C(2,1))"),
			"10.0")

	def test_nested_permutations(self):
		self.assertEqual(
			c.combinations_and_permutations("func", "P", "(5,P(2,1))"),
			"20.0")

	def test_nested_mixed(self):
		self.assertEqual(
			c.combinations_and_permutations("func", "P", "(C(5,1),P(2,1))"),
			"20.0")

	def test_nested_mixed2(self):
		self.assertEqual(
			c.combinations_and_permutations("func", "C", "(C(5,1),P(2,1))"),
			"10.0")
			
	def test_choose_notation_needs_four_arguments(self):
		with self.assertRaises(TypeError):
			c.combinations_and_permutations("choose", "C", "(5,2)")

	def test_function_notation_needs_only_three_arguments(self):
		with self.assertRaises(TypeError):
			c.combinations_and_permutations("func", "C", "5", m = "2")

	def test_raises_value_errors_for_not_c_or_p_choose_notaion(self):
		with self.assertRaises(ValueError):
			c.combinations_and_permutations("choose", "R", "5", "2")
			
	def test_raises_value_errors_for_not_c_or_p_func_notaion(self):
		with self.assertRaises(ValueError):
			c.combinations_and_permutations("func", "R", "(5, 2)")


class test_statistics_functions(unittest.TestCase):
	
	def test_all_basic_statistics(self):
		self.assertEqual(
			c.statistics_functions("mean", "(4, 6, 39, 2, 11)"),
			"12.4")
		self.assertEqual(
			c.statistics_functions("ave", "(4, 6, 39, 2, 11)"),
			"12.4")
		self.assertEqual(
			c.statistics_functions("mean", "(4, 6, 39, 2, 11)"),
			"12.4")
		self.assertEqual(
			c.statistics_functions("median", "(1, 2, 3, 1, 7)"),
			"2.0")
		self.assertEqual(
			c.statistics_functions("mode", "(1, 2, 3, 1, 7)"),
			"1.0")
		self.assertEqual(
			c.statistics_functions("min", "(3, 6, 11, -7, -1, 55)"),
			"-7.0")
		self.assertEqual(
			c.statistics_functions("max", "(3, 6, 11, -7, -1, 55)"),
			"55.0")
		self.assertAlmostEqual(
			float(c.statistics_functions("stdev", "(3, 4, 4, 6, 8)")),
			2.0)
			
	def test_nested_stats_functions(self):
		self.assertEqual(
			c.statistics_functions("mean", "(1, 2, mean(1, 3, 5))"),
			"2.0")
			
	def test_not_defined_functions(self):
		with self.assertRaises(ValueError):
			c.statistics_functions("sin", "(pi)")

			
class test_single_argument_function(unittest.TestCase):
	
	def test_basic_trig_functions(self):
		self.assertAlmostEqual(
			float(c.single_argument("sin", "(pi/6)")),
			0.5)
		self.assertAlmostEqual(
			float(c.single_argument("cos", "(pi/3)")),
			0.5)
		self.assertAlmostEqual(
			float(c.single_argument("tan", "(pi/4)")),
			1.0)
		self.assertAlmostEqual(
			float(c.single_argument("sec", "(pi/3)")),
			2.0)
		self.assertAlmostEqual(
			float(c.single_argument("csc", "(pi/6)")),
			2.0)
		self.assertAlmostEqual(
			float(c.single_argument("cot", "(pi/4)")),
			1.0)
			
	def test_hyperbolic_trig_functions(self):
		self.assertAlmostEqual(
			float(c.single_argument("sinh", "(1)")),
			(math.e ** 2 - 1) / (2 * math.e))
		self.assertAlmostEqual(
			float(c.single_argument("cosh", "(1)")),
			(math.e ** 2 + 1) / (2 * math.e))
		self.assertAlmostEqual(
			float(c.single_argument("tanh", "(1)")),
			(math.e ** 2 - 1) / (math.e ** 2 + 1))
		self.assertAlmostEqual(
			float(c.single_argument("csch", "(1)")),
			(2 * math.e) / (math.e ** 2 - 1))
		self.assertAlmostEqual(
			float(c.single_argument("sech", "(1)")),
			(2 * math.e) / (math.e ** 2 + 1))
		self.assertAlmostEqual(
			float(c.single_argument("coth", "(1)")),
			(math.e ** 2 + 1) / (math.e ** 2 - 1))
		
	def test_arctrig_functions(self):
		self.assertAlmostEqual(
			float(c.single_argument("asin", "(.5)")),
			math.pi / 6)
		self.assertAlmostEqual(
			float(c.single_argument("acos", "(.5)")),
			math.pi / 3)
		self.assertAlmostEqual(
			float(c.single_argument("atan", "(3 ** .5)")),
			math.pi / 3)
		self.assertAlmostEqual(
			float(c.single_argument("asec", "(2)")),
			math.pi / 3)
		self.assertAlmostEqual(
			float(c.single_argument("acsc", "(2)")),
			math.pi / 6)
		self.assertAlmostEqual(
			float(c.single_argument("acot", "(3 ** .5)")),
			math.pi / 6)

	def test_inverse_hyperbolic_functions(self):
		self.assertAlmostEqual(
			float(c.single_argument("asinh",
				"(((e ** 2) - 1) / (2 * e))")),
			1)
		self.assertAlmostEqual(
			float(c.single_argument("acosh",
				"((e ** 2 + 1) / (2 * e))")),
			1)
		self.assertAlmostEqual(
			float(c.single_argument("atanh",
				"((e ** 2 - 1) / (e ** 2 + 1))")),
			1)
		self.assertAlmostEqual(
			float(c.single_argument("acsch",
				"((2 * e) / (e ** 2 - 1))")),
			1)
		self.assertAlmostEqual(
			float(c.single_argument("asech",
				"((2 * e) / (e ** 2 + 1))")),
			1)
		self.assertAlmostEqual(
			float(c.single_argument("acoth",
				"((e ** 2 + 1) / (e ** 2 - 1))")),
			1)

	def test_other_functions(self):
		self.assertEqual(
			c.single_argument("abs", "(-1)"),
			"1.0")
		self.assertEqual(
			c.single_argument("abs", "(3)"),
			"3.0")
		self.assertEqual(
			c.single_argument("ceil", "(.5)"),
			"1.0")
		self.assertEqual(
			c.single_argument("ceil", "(-1.5)"),
			"-1.0")
		self.assertEqual(
			c.single_argument("floor", "(4.8)"),
			"4.0")
		self.assertEqual(
			c.single_argument("floor", "(-4.8)"),
			"-5.0")
		self.assertAlmostEqual(
			float(c.single_argument("erf", "(e)")),
			0.9998790689599)
			
	def test_trig_functions_with_degree_symbol(self):
		self.assertAlmostEqual(
			float(c.single_argument("sin", "(30°)")),
			"0.5")






























if __name__ == '__main__':
    unittest.main()
