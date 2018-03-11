# -*- coding: utf-8 -*-

'''
Written by: Max Friedman
Licensed under GPLv3

re_calc.py

This is a graphing calculator written in python 3.6.
It has defined:
addition, subtraction, multiplication, division, exponents,
logarithms, trig functions, inverse trig functions, hyperbolic
functions, inverse hyperbolic functions, the ceiling function,
the floor function, the gauss error function, modulus, absolute value,
factorials, the gamma function, combinations, permutations, max, min,
mean, median, mode, sample standard deviation, definite integrals,
derivatives at a point, evaluating a function at a point, graphing
functions in Cartesian and polar, and solving equations.

It has a GUI made with tkinter that it will default to using if tkinter
is installed. It defines graphing and polar graphing classes. It remembers
every input it is given.

'''

import math
import statistics as stats
import sys
import os

import numpy as np
from PIL import Image
from PIL import ImageTk
from warnings import warn, simplefilter
from pickle import load, dump
from re import compile, sub
from decimal import Context
from sympy import symbols, integrate, sympify
from sympy.solvers import solve

try:
	import tkinter as tk
	from _tkinter import TclError
except ModuleNotFoundError:
	simplefilter('default', ImportWarning)
	warn("Tkinter can not be imported. Using command line interface",
		category = ImportWarning)


'''  Completed
2) Make average functions deal with non-number arguments
3) Stdev
4) deal with commas
5) tkinter interface
8) min max functions
9) make tkinter windows close
12) two graphs at once
14) eval non-number arguments
15) multi argument functions cant have commas in the second argument
16) absolute value with pipes
17) use division sign
19) pickle degree mode
20) graph closes only when user dictates
28) improve tkinter interface
29) cut off trailing zeros
31) polar graphs
33) show request
'''

'''  To Do
1) Deal with floating point errors
6) complex numbers
7) higher order derivatives
10) graph non-functions
11) improper integrals
13) integrals can have non-number bounds
14) derivatives non-number arguments
18) set y bounds on graphs
21) matrices
22) unit conversions
23) indefinite integrals
24) derivatives of functions
25) summation notation
26) big pi notation
27) series
30) two expressions adjacent means multiplication
32) 3d graphs
34) make icon of tkinter window when run on Fedora
35) make compatible with other operating systems
36) fix subtraction problem
37) other weird trig functions
38) setup and wheel files
39) make tests for all parts of the program
40) doc strings for at least some of the tests
41) user defined functions
42) user defined variables
43)
'''


# os handling
if os.name == "nt":
	user_path = os.environ["USERPROFILE"]
elif os.name == "posix":
	user_path = os.environ["HOME"]

up_hist = 0
ctx = Context()

# changeable variables
use_gui = True
graph_w = 400
graph_h = 400
graph_colors = ("black", "red", "blue", "green", "orange", "purple")
ctx.prec = 15

# multi session variables
calc_path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(calc_path, "re_calc_info.txt"), "rb") as file:
	calc_info = load(file)
history = calc_info[0]
ans = calc_info[1]
options = calc_info[2]
degree_mode = options[0]  # in degree mode 0 = off 2 = on
polar_mode = options[1]
der_approx = options[2]  # default = .0001
hist_len = options[3]
win_bound = calc_info[3]

#                 enter up down           enter  up  down
key_binds = {"nt": (13, 38, 40), "posix": (104, 111, 116)}
g_bound_names = ("x min", "x max", "y min", "y max", "theta min",
	"theta max")
one_arg_funcs = {
	#   name                 function                angles
	"hacovercosin": (lambda x: .5 + math.sin(x) / 2, "in"),
	"hacoversin": (lambda x: .5 - math.sin(x) / 2, "in"),
	"havercosin": (lambda x: .5 + math.cos(x) / 2, "in"),
	"haversin": (lambda x: .5 - math.cos(x) / 2, "in"),
	"covercosin": (lambda x: 1 + math.sin(x), "in"),
	"coversin": (lambda x: 1 - math.sin(x), "in"),
	"vercosin": (lambda x: 1 + math.cos(x), "in"),
	"versin": (lambda x: 1 - math.cos(x), "in"),
	"exsec": (lambda x: 1 / math.cos(x) - 1, "in"),
	"excsc": (lambda x: 1 / math.sin(x) - 1, "in"),
	
	"asinh": (math.asinh, "out"),
	"acosh": (math.acosh, "out"),
	"atanh": (math.atanh, "out"),
	"asech": (lambda x: math.acosh(1 / x), "out"),
	"acsch": (lambda x: math.asinh(1 / x), "out"),
	"acoth": (lambda x: math.atanh(1 / x), "out"),
	
	"arcsinh": (math.asinh, "out"),
	"arccosh": (math.acosh, "out"),
	"arctanh": (math.atanh, "out"),
	"arcsech": (lambda x: math.acosh(1 / x), "out"),
	"arccsch": (lambda x: math.asinh(1 / x), "out"),
	"arccoth": (lambda x: math.atanh(1 / x), "out"),

	"sinh": (math.sinh, "in"),
	"cosh": (math.cosh, "in"),
	"tanh": (math.tanh, "in"),
	"sech": (lambda x: 1 / math.cosh(x), "in"),
	"csch": (lambda x: 1 / math.sinh(x), "in"),
	"coth": (lambda x: 1 / math.tanh(x), "in"),

	"asin": (math.asin, "out"),
	"acos": (math.acos, "out"),
	"atan": (math.atan, "out"),
	"asec": (lambda x: math.acos(1 / x), "out"),
	"acsc": (lambda x: math.asin(1 / x), "out"),
	"acot": (lambda x: math.atan(1 / x), "out"),
	
	"arcsin": (math.asin, "out"),
	"arccos": (math.acos, "out"),
	"arctan": (math.atan, "out"),
	"arcsec": (lambda x: math.acos(1 / x), "out"),
	"arccsc": (lambda x: math.asin(1 / x), "out"),
	"arccot": (lambda x: math.atan(1 / x), "out"),

	"sin": (math.sin, "in"),
	"cos": (math.cos, "in"),
	"tan": (math.tan, "in"),
	"sec": (lambda x: 1 / math.cos(x), "in"),
	"csc": (lambda x: 1 / math.sin(x), "in"),
	"cot": (lambda x: 1 / math.tan(x), "in"),

	"abs": (math.fabs, ""),
	"ceil": (math.ceil, ""),
	"floor": (math.floor, ""),
	"erf": (math.erf, ""),
	"erfc": (math.erfc, "")
}


# regular expressions
if True:
	# regex for a number
	reg_num = "(-?[0-9]+\.?[0-9]*|-?[0-9]*\.?[0-9]+)"

	# regex for commands
	# ^$ is for an empty string
	command_reg = ("([Hh]istory)|([Qq]uit|[Ee]xit|^$)|"
		"([Dd]egree [Mm]ode)|([Rr]adian [Mm]ode)")
	command_comp = compile(command_reg)

	# regex for constants
	const_reg = ("(pi|π|(?<![a-z0-9])e(?![a-z0-9])|"
	"ans(?:wer)?|tau|τ|phi|φ)")
	const_comp = compile(const_reg)

	# regex for graphing
	graph_reg = "[Gg]raph (.+)"
	graph_comp = compile(graph_reg)

	# regex for equation solving
	alg_reg = "[Ss]olve(.+)"
	alg_comp = compile(alg_reg)

	# regex for evaluating functions
	eval_reg = ("[Ee]val(?:uate)? (.+) (?:for|at) (.+)")
	eval_comp = compile(eval_reg)

	# regex for derivatives (must be at a number)
	der_reg = ("[Dd]erivative of (.+) at (.+?)"
	"( with respect to [a-z])?")
	der_comp = compile(der_reg)

	# regex for integrals (bounds must be numbers)
	int_reg = ("(?:[Ii]ntegra(?:te ?|l ?)|∫)(.+)d([a-z])"
	" (?:from )?"+reg_num+" to "+reg_num)
	int_comp = compile(int_reg)

	# regex for combinations and permutations
	# parentheses is to differentiate it from choose notation
	comb_reg = "(C|P)(\(.+)"
	comb_comp = compile(comb_reg)

	# regex for statistics functions
	ave_reg = ("([Aa]verage|[Aa]ve|[Mm]ean|[Mm]edian|[Mm]ode|"
	"[Mm]ax|[Mm]in|[Ss]tdev)(.+)")
	ave_comp = compile(ave_reg)

	# regex for one argument functions
	# the order does matter because if trig functions come
	# before hyperbolic functions the "h" is interpreted as
	# part of the argument for the function
	trig_reg = ("("
	"hacovercosin|hacoversin|havercosin|haversin|"
	"covercosin|coversin|vercosin|versin|"
	"exsec|excsc|"
	"sinh|cosh|tanh|asinh|acosh|atanh|"
	"arcsinh|arccosh|arctanh|"
	"sech|csch|coth|asech|acsch|acoth|"
	"arcsech|arccsch|arccoth|"
	"sin|cos|tan|sec|csc|cot|"
	"asin|arcsin|acos|arccos|atan|arctan|"
	"asec|acsc|acot|arcsec|arccsc|arccot|"
	"abs|ceil|floor|erf"
	")(.+)")
	
	# trig_reg = "(" + "|".join(key for key in one_arg_funcs) + ")(.+)"
	trig_comp = compile(trig_reg)

	# regex for gamma function
	gamma_reg = "(?:[Gg]amma|Γ)(.+)"
	gamma_comp = compile(gamma_reg)

	# regex for logarithms
	log_reg = "[Ll]og(.+)|ln(.+)"
	log_comp = compile(log_reg)

	# regex for modulus
	mod2_reg = "[Mm]od(.+)"
	mod2_comp = compile(mod2_reg)

	# regex for detecting absolute value
	abs_reg = "(.*\|.*)"
	abs_comp = compile(abs_reg)

	# regex for parentheses
	# [^()] makes it only find the inner most parentheses
	paren_reg = "\(([^()]+)\)"
	paren_comp = compile(paren_reg)

	# regex for choose notation (not recursive)
	# in the form of "nCm" or "nPm"
	choos_reg = reg_num+"(C|P)"+reg_num
	choos_comp = compile(choos_reg)

	# ignores commas in the middle of numbers
	# could be problematic if two floats ever
	# end up next to each other
	comma_comp = compile(reg_num+","+reg_num)

	# regex for exponents (not recursive)
	exp_reg = reg_num+" ?(\*\*|\^) ?"+reg_num
	exp_comp = compile(exp_reg)

	# regex for factorials (not recursive)
	fact_reg = reg_num+"\!"
	fact_comp = compile(fact_reg)

	# regex in the form x%y (not recursive)
	mod_reg = reg_num+" ?% ?"+reg_num
	mod_comp = compile(mod_reg)

	# regex for percentages (should probably be done without regex)
	per_reg = "%"
	per_comp = compile(per_reg)

	# regex for multiplication (not recursive)
	mult_reg = reg_num + " ?([*/÷]) ?" + reg_num
	mult_comp = compile(mult_reg)

	# regex for addition (not recursive)
	add_reg = reg_num+" ?([+-]) ?"+reg_num
	add_comp = compile(add_reg)

# list of compiled regular expressions in order
operations = [command_comp, const_comp, graph_comp,
	alg_comp, eval_comp, der_comp, int_comp,
	comb_comp, ave_comp, trig_comp, gamma_comp, log_comp, mod2_comp,
	abs_comp, paren_comp,
	# here is where the order of operations starts to matter
	# it goes: choose notation(nCm), exponents, factorial,
	# modulus, multiplication, addition
	comma_comp, choos_comp,
	exp_comp, fact_comp, mod_comp, per_comp, mult_comp, add_comp]

#######################################################
# regular expressions not used on the immediate input #
#######################################################

# check for bounds on graph
graph_rang_reg = "(.+(?=from))(from "+reg_num+" to "+reg_num+")"
graph_rang_comp = compile(graph_rang_reg)

# check for equals sign when solving equations
eq_sides_reg = "(.+)=(.+)|(.+)"
eq_sides_comp = compile(eq_sides_reg)

# checks for specified variable when solving equations
alg_var_reg = "(.+) for ([a-z])"
alg_var_comp = compile(alg_var_reg)


def float_to_str(f):
	'''Convert the given float to a string,
	without resorting to scientific notation.
	
	>>> float_to_str(3.0030)
	'3.003'
	'''
	
	d1 = ctx.create_decimal(repr(float(f)))
	return format(d1, 'f')


def check_if_float(x):
	'''Test if a object can be made a float.
	
	>>> check_if_float("4.5")
	True
	
	>>> check_if_float("this")
	False
	'''

	try:
		float(x)
		return(True)
	except (ValueError, TypeError):
		return(False)


def save_info():
	'''Save options, history and other stuff to a file.'''

	global calc_info

	calc_info = [history, ans, options, win_bound]

	with open(os.path.join(calc_path, "re_calc_info.txt"), "wb") as file:
		dump(calc_info, file)


def switch_degree_mode(mode):
	'''Switch between degree mode and radian mode.'''

	global degree_mode

	if mode == "degree":
		degree_mode = 2
	elif mode == "radian":
		degree_mode = 0
	elif mode in (0, 2):
		degree_mode = mode
	else:
		raise CalculatorError("Can not set degree_mode to " + str(mode))

	options[0] = degree_mode
	save_info()


def switch_polar_mode(mode):
	'''Switch between polar and Cartesian graphing.'''

	global polar_mode

	if mode == "polar":
		polar_mode = True
	elif mode == "Cartesian":
		polar_mode = False
	elif mode in (True, False):
		polar_mode = mode
	else:
		raise CalculatorError("Can not set polar_mode to " + str(mode))

	options[1] = polar_mode
	save_info()


def change_hist_len(entry_box, root):
	'''Change the length of the history print back.'''

	global hist_len

	# get user input
	input = entry_box.get()

	# if the input is a digit set that to be the
	# history print back length save and close the window
	if input.isdigit() and int(input) > 0:
		hist_len = int(input)
		options[3] = hist_len
		save_info()

		root.destroy()
	else:
		pass


def change_hist_len_win():
	'''Create a popup to change the length of the
	history print back.
	'''

	root = tk.Toplevel()

	# create window text
	disp = tk.Message(root,
	text = "Current History print back length: "
	+ str(hist_len))
	disp.grid(row = 0, column = 0)

	# create the input box
	entry_box = tk.Entry(root)
	entry_box.grid(row = 1, column = 0)

	# bind enter to setting the input to be the history length
	root.bind("<Return>",
	lambda event: change_hist_len(entry_box, root))

	root.mainloop()


def change_der_approx(entry_box, root):
	'''Change the length of the history print back.'''

	global der_approx

	# get user input
	input = entry_box.get()

	# if the input is a positive float set that to be the
	# der_approx value save and close the window
	if check_if_float(input) and "-" not in input:
		der_approx = float(input)
		options[2] = der_approx
		save_info()

		root.destroy()
	else:
		pass


def change_der_approx_win():
	'''Create a popup to change the lenght of the
	history print back.
	'''

	root = tk.Toplevel()

	# create window text
	disp = tk.Message(root, text = "Current der approx: "
	+ str(der_approx))
	disp.grid(row = 0, column = 0)

	# create the input box
	entry_box = tk.Entry(root)
	entry_box.grid(row = 1, column = 0)

	# bind enter to setting the input to be the history length
	root.bind("<Return>",
	lambda event: change_der_approx(entry_box, root))

	root.mainloop()


def change_graph_win_set():
	'''Change the graphing window bounds.'''

	global win_bound, g_bound_entry, g_bound_string

	g_bound_input = {}
	for i in g_bound_names:
		g_bound_input[i] = g_bound_entry[i].get()

	for i in g_bound_names:
		if check_if_float(g_bound_input[i]):
			win_bound[i] = float(g_bound_input[i])

	save_info()

	for i in g_bound_names:
		g_bound_string[i].set(i + " = " + str(win_bound[i]))


def find_match(s):
	'''Find matching parentheses.
	
	>>> find_match("(4, (5), 3) + 2")
	('(4, (5), 3)', ' + 2')
	'''

	x = 0
	if not s.startswith("("):
		raise CalculatorError(
			"error '" + str(s) + "' is an invalid input.")
				
	for i in range(len(s)):

		# count the parentheses
		if s[i] == "(":
			x += 1
		elif s[i] == ")":
			x -= 1

		if x == 0:

			# left is all the excess characters after
			# the matched parentheses
			# an is the matched parentheses and everything in them
			an = s[:i+1]
			left = s[i+1:]

			break

		elif x < 0:
			raise CalculatorError(
				"error '" + str(s) + "' is an invalid input.")

	try:
		return(an, left)
	except UnboundLocalError:
		raise CalculatorError("error '" + str(s) + "' is an invalid input.")


def brackets(s):
	'''Inform separate whether parentheses match.
	
	>>> brackets("())")
	False
	
	>>> brackets("(()())")
	True
	
	>>> brackets("w(h)(a()t)")
	True
	'''

	x = 0
	for i in s:
		if i == "(":
			x += 1
		elif i == ")":
			x -= 1
		if x < 0:
			return(False)
	return(not x)


def separate(s):
	'''Split up arguments of a function with commas
	like mod(x, y) or log(x, y) based on where commas that aren't in
	parentheses.
	
	>>> separate("5, 6 , (4, 7)")
	('5', ' 6 ', ' (4, 7)')
	'''
	
	terms = s.split(",")
	
	new_terms = []
	middle = False
	term = ""
	for i in terms:
		if middle:
			term = term + "," + i
		else:
			term = i
		x = brackets(term)
		if x:
			new_terms.append(term)
			middle = False
		else:
			middle = True
	return(tuple(new_terms))


class CalculatorError(Exception):
	pass


class graph(object):
	'''Cartesian Graphing window class.'''

	def __init__(self,
	xmin = -5, xmax = 5, ymin = -5, ymax = 5,
	wide = 400, high = 400):  # all the arguments you pass the object
		'''Initialize the graphing window.'''

		self.root = tk.Toplevel()

		self.root.title("Calculator")

		# sets bounds
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax

		self.xrang = self.xmax - self.xmin
		self.yrang = self.ymax - self.ymin

		# dimensions of the window
		self.wide = wide
		self.high = high
		
		self.data = np.zeros((self.high, self.wide, 3), dtype = np.uint8)
		self.data.fill(255)

		# create the canvas
		self.screen = tk.Canvas(self.root,
		width = self.wide, height = self.high)
		self.screen.pack()
		
		# create the image
		self.pic = ImageTk.PhotoImage(Image.fromarray(self.data, "RGB"))
		self.screen.create_image(
			self.wide / 2, self.high / 2, image = self.pic)

		# button that close the window and program immediately
		self.close = tk.Button(self.root, text = "Close",
		command = self.root.destroy)
		self.close.pack()

		print(sys.getrefcount(self.pic))
		# draws the axes
		self.axes()

	# draw the axes
	def axes(self):
		'''Draw the axis.'''

		xrang = self.xmax - self.xmin
		yrang = self.ymax - self.ymin

		# adjusted y coordinate of x-axis
		b = self.high + (self.ymin * self.high / yrang)

		# adjusted x coordinate of y-axis
		a = -1 * self.xmin * self.wide / xrang
		
		self.data[int(round(b, 0)), :, :] = 0
		self.data[:, int(round(a, 0)), :] = 0
		self.data.fill(0)
		self.pic = ImageTk.PhotoImage(Image.fromarray(self.data, "RGB"))
		self.screen.create_image(
			self.wide / 2, self.high / 2, image = self.pic)

		try:
			# draw x-axis
			#self.screen.create_line(0, b, self.wide, b, fill = "gray")

			# draw y-axis
			#self.screen.create_line(a, self.high, a, 0, fill = "gray")

			self.root.update()
		except TclError as e:
			pass

	def draw(self, func, color = "black"):
		'''Draw a Cartesian function.'''

		density = 1000
		x = self.xmin

		while x < self.xmax:

			# move the x coordinate a little
			x += self.xrang / density
			try:
				# eval the function at x and set that to y
				y = float(evaluate_function(func, str(x)))

				# check if the graph goes off the screen
				if y > self.ymax or y < self.ymin and density > 2000:
					denstiy = 2000
				else:
					# find the slope at the point using the derivative
					# function of simplify
					try:
						slope = float(find_derivative(func, str(x)))
					except (ValueError) as e:
						slope = 10

					# calculate how dense the points need to be
					# this function is somewhat arbitrary
					density = int((3000 * math.fabs(slope))
					/ self.yrang + 500)

				# adjust coordinate for the screen (this is the
				# hard part)
				a = (x-self.xmin) * self.wide / self.xrang
				b = self.high - ((y - self.ymin) * self.high
				/ self.yrang)

				# draw the point
				self.screen.create_line(a, b, a + 1, b, fill = color)
			except (ValueError, TclError) as e:
				pass

			# update the screen
			try:
				self.root.update()
			except TclError as e:
				x = self.xmax + 1


class polar_graph(graph):
	'''Polar graphing window class.'''

	def __init__(self,
	xmin = -5, xmax = 5, ymin = -5, ymax = 5,
	theta_min = 0, theta_max = 10,
	wide = 400, high = 400):  # all the arguments you pass the object
		'''Initialize polar graphing window.'''

		super(polar_graph, self).__init__(
			xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax,
			wide = wide, high = high)

		self.theta_min = theta_min
		self.theta_max = theta_max

		self.theta_rang = self.theta_max - self.theta_min

	def draw(self, func, color = "black"):
		'''Draw a polar function.'''

		density = 1000
		theta = self.theta_min

		while theta < self.theta_max:

			# move theta a little
			theta += self.theta_rang / density
			try:
				# eval the function at theta and set that to r
				r = float(evaluate_function(func, str(theta)))

				# find the slope at the point using find_derivative
				slope = float(find_derivative(func, str(theta)))

				x = r * math.cos(theta)
				y = r * math.sin(theta)

				# calculate how dense the points need to be
				# this function is somewhat arbitrary
				density = int((400 * math.fabs(slope)) + 500)

				# check if the graph goes off the screen
				if y > self.ymax or y < self.ymin or \
					x > self.xmax or x < self.xmin:
					denstiy = 2000

				# adjust coordinate for the
				# screen (this is the hard part)
				a = (x - self.xmin) * self.wide / self.xrang
				b = self.high - ((y - self.ymin) * self.high
				/ self.yrang)

				# draw the point
				self.screen.create_line(a, b, a + 1, b, fill = color)
			except (ValueError, TclError) as e:
				pass

			# update the screen
			try:
				self.root.update()
			except TclError as e:
				theta = self.theta_max + 1


#####################
# List of Functions #
#####################

def constant_function(constant):
	'''Evaluate mathematical constants.
	
	>>> constant_function("pi")
	3.141592653589793
	
	>>> constant_function("phi")
	1.618033988749895
	'''

	constant_dict = {"pi": math.pi, "π": math.pi, "e": math.e,
	"ans": ans, "answer": ans, "tau": math.tau, "τ": math.tau,
	"phi": (1 + 5 ** 0.5) / 2, "φ": (1 + 5 ** 0.5) / 2}

	if constant in constant_dict:
		return(constant_dict[constant])
	else:
		raise CalculatorError("'%s' is not a recognized constant." % constant)


def graph_function(func_arg):
	'''Graph the given function.'''

	# looks for x bounds on the graph
	range_m = graph_rang_comp.search(func_arg)
	if range_m is not None:
		func_arg = range_m

	# checks to see if tkinter is installed to graph things at all
	if "tkinter" in sys.modules:

		# finds multiple functions to graph
		if range_m is None:
			funcs_to_graph = func_arg.split(" and ")
		else:
			funcs_to_graph = func_arg.group(1).split(" and ")

		# sets bounds to bounds given
		if range_m is None:
			temp_graph_xmin = win_bound["x min"]
			temp_graph_xmax = win_bound["x max"]
		else:
			temp_graph_xmin = float(func_arg.group(3))
			temp_graph_xmax = float(func_arg.group(4))

		# creates graph object
		if polar_mode is False:
			made_graph = graph(
				xmin = temp_graph_xmin, xmax = temp_graph_xmax,
				ymin = win_bound["y min"], ymax = win_bound["y max"],
				wide = graph_w, high = graph_h)
		else:
			made_graph = polar_graph(
				xmin = temp_graph_xmin, xmax = temp_graph_xmax,
				ymin = win_bound["y min"], ymax = win_bound["y max"],
				theta_min = win_bound["theta min"],
				theta_max = win_bound["theta max"],
				wide = graph_w, high = graph_h)
		print(sys.getrefcount(made_graph.pic))

		# works out how many times it needs to
		# loop the colors its using
		color_loops = math.ceil(len(funcs_to_graph)
		/ len(graph_colors))

		# passes functions to be graphed and the color to do so with
		for f, c in zip(funcs_to_graph, graph_colors * color_loops):
			made_graph.draw(f, color = c)

		return(made_graph)

	# informs the user of reason for failure
	else:
		print("Could not graph. Tkinter is not installed")


def solve_equations(equation):
	'''Solve equations using sympy. If there is no equals
	sign it is assumed the expression equals zero. If there is more
	than one answer it will return a list of the answers.
	
	>>> solve_equations("x^2 = 4")
	[-2, 2]
	
	>>> solve_equations("x-7 = 13")
	20
	'''

	# find if there is a specified variable
	varm = alg_var_comp.search(equation)

	# find the variable its solving for. defaults to "x"
	if varm is None:
		x = symbols("x")
		eq = equation
	else:
		# used to be symbols(varm.group(2)[-1]) don't know why
		# may have been important
		x = symbols(varm.group(2))
		eq = varm.group(1)

	# if there is an equals sign solve for zero and use sympy
	# to solve it
	em = eq_sides_comp.search(eq)
	if em.group(3) is None:
		sym_zero = sympify(em.group(1) + "-(" + em.group(2) + ")")
		temp_result = solve(sym_zero, x)

		# if there is only one result make it the result
		# otherwise return the list
		if len(temp_result) == 1:
			return(temp_result[0])
		else:
			return(temp_result)

	# if there isn't an equals sign use sympy to solve
	else:
		temp_result = solve(em.group(3), x)

		# if there is only one result make it the result
		# otherwise return the list
		if len(temp_result) == 1:
			return(temp_result[0])
		else:
			return(temp_result)


def evaluate_function(expression, point, var = "x"):
	'''Evaluate the function by substituting var for the number you
	want to evaluate at.
	
	>>> evaluate_function("r^2", 5, var = "r")
	'25.0'
	
	>>> evaluate_function("3*b", "2", "b")
	'6.0'
	'''

	# substituting the point for x in the function and evaluating
	# that recursively
	return(simplify(sub("(?<![a-z])" + var + "(?![a-z])",
	str(point), expression)))


def find_derivative(expression, point, var = "x"):
	'''Calculate the derivative by evaluating the slope
	between two points on either side of the point you are
	finding the derivative of.
	'''

	# find the point on either side of the desired point
	p = float(simplify(point))
	x_one = p + der_approx
	x_two = p - der_approx

	# find the change in y value between the two points
	delta_y = (float(evaluate_function(expression, str(x_one), var = var))
	- float(evaluate_function(expression, str(x_two), var = var)))

	# divide by the length of the interval to find the slope
	return(delta_y / (2 * der_approx))


def integrate_function(expression, var, a, b):
	'''Integrate with sympy.'''

	# Integrals must be in a form that sympy can integrate
	# The bounds must be numbers not expressions
	# The integral must have a "dx" or whatever variable you are using

	# using sympy to integrate
	return(str(float(integrate(expression, (var, a, b)))))


def combinations_and_permutations(form, letter, n, m = None):
	'''Solve combinations and permutations.

	n is either n or all arguments depending of the for they're
	written in

	combinations and permutations written
	both as C(5, 2) and 5C2 evaluated as: 5 choose 2
	if written as mCn it will only take numbers not expressions
	unless parentheses are used. In order of operations nCm comes
	first.
	Combinations and permutations both used the gamma function
	in place of factorials and as a result will take
	non-integer arguments
	'''

	if form == "choose":  # if written as nCm
	
		if m is None:
			raise CalculatorError(
				"combinations_and_permutations requires a fourth "
				"argument when using choose notation")

		# turn the arguments into floats and give them more
		# descriptive names
		inner_n = float(n)
		inner_m = float(m)

		# find permutations
		temp_result = math.gamma(1 + inner_n) \
			/ math.gamma(1 + inner_n - inner_m)

		# if combinations also divide by m!
		if letter == "C":
			temp_result = temp_result / math.gamma(1 + inner_m)
		elif letter == "P":
			pass
		else:
			raise CalculatorError("Second argument must be 'C' or 'P' for "
				"combinations or permutations not '%s'" % letter)

		return(str(temp_result))

	elif form == "func":  # if written as C(5, 2)
		if m:
			raise CalculatorError(
				"combinations_and_permutations can not take a fourth "
				"argument when using function notation")

		# find the arguments of the function and cut off
		# everything else
		# sin(C(5, 2)) ← the last parenthesis
		proto_inner = find_match(n)

		# remove outer parentheses
		x = proto_inner[0][1:-1]

		# separate the arguments
		comb_args = separate(x)

		# evaluate each of the arguments separately
		inner_n = float(simplify(comb_args[0]))
		inner_m = float(simplify(comb_args[1]))

		# find permutations
		temp_result = math.gamma(1 + inner_n) \
			/ math.gamma(1 + inner_n - inner_m)

		# if combinations also divide by m!
		if letter == "C":
			temp_result = temp_result / math.gamma(1 + inner_m)
		elif letter == "P":
			pass
		else:
			raise CalculatorError("Second argument must be 'C' or 'P' for "
				"combinations or permutations not '%s'" % letter)

		# add on anything that was was cut off the end when finding
		# the arguments
		# sin(C(5, 2)) ← the last parenthesis
		return(str(temp_result) + proto_inner[1])
	else:
		raise CalculatorError("First argument must be 'choose' or 'func' "
			"not '%s'" % form)


def statistics_functions(function, args):
	'''Perform general statistics functions.

	This may in the future include any function that
	can have an arbitrarily large number of arguments.
	'''

	# find the arguments of the function and cut off
	# everything else
	# sin(mean(4, 2)) ← the last parenthesis
	proto_inner = find_match(args)

	# separate the arguments based on commas that are not
	# within more than one set of parentheses
	ave_args = separate(proto_inner[0][1:-1])

	# evaluate all the arguments
	list_ave = list(map((lambda x: float(simplify(x))), ave_args))

	# perform the different functions
	if function.lower() in ("ave", "average", "mean"):
		result = stats.mean(list_ave)
	elif function.lower() == "median":
		result = stats.median(list_ave)
	elif function.lower() == "mode":
		result = stats.mode(list_ave)
	elif function.lower() == "max":
		result = max(list_ave)
	elif function.lower() == "min":
		result = min(list_ave)
	# this is the sample standard deviation
	elif function.lower() in ("stdev"):
		result = stats.stdev(list_ave)
	else:
		raise CalculatorError("%s is not a function that is defined in "
			"statistics_functions" % function)

	# add on anything that was was cut off the end when finding
	# the arguments
	# sin(mean(4, 2)) ← the last parenthesis
	return(float_to_str(result) + proto_inner[1])


def single_argument(func, args):
	'''Evaluate trig functions and other unary operators.'''

	global degree_mode

	# find the arguments of the function and cut off
	# everything else
	# tan(sin(π)) ← the last parenthesis when
	# evaluating sin
	proto_inner = list(find_match(args))

	# looks for the degree symbol in the argument
	# if the program finds it degree mode is set to true
	# for the particular operation
	if "°" in proto_inner[0]:
		if degree_mode == 0:
			degree_mode = 1
		proto_inner[0] = sub("[°]", "", proto_inner[0])

	# evaluate the argument into a form that math.log
	# can accept
	inner = float(simplify(proto_inner[0]))

	# check if in degree mode and if its doing an
	# operation that takes an angle as an argument
	if degree_mode > 0 and "in" in one_arg_funcs[func][1]:
		inner = math.pi * inner / 180
		
	result = one_arg_funcs[func][0](inner)

	# checks if its in degree mode (not because of
	# degree symbols in the argument) and if so
	# converts the answer to degrees for functions that
	# output an angle
	if degree_mode == 2 and "out" in one_arg_funcs[func][1]:
		result = result * 180 / math.pi

	# resets the degree mode for the session
	if degree_mode == 1:
		degree_mode = 0

	# this is a fix for the output being in
	# scientific notation and the program mistaking the
	# e for the constant e
	try:
		result = float_to_str(result)
	except (ValueError, TypeError):
		pass

	# add back anything that was cut off when finding the
	# argument of the inner function
	# tan(sin(π)) ← the last parenthesis when
	# evaluating sin
	return(float_to_str(str(result) + proto_inner[1]))


def gamma_function(arg):
	'''Use the gamma function.'''

	# find the arguments of the function and cut off
	# everything else
	# sin(gamma(5)) ← the last parenthesis
	proto_inner = find_match(arg)

	# evaluating the argument
	inner = float(simplify(proto_inner[0]))

	# doing the calculation
	result = math.gamma(inner)

	# add back anything that was cut off when finding the
	# argument of the inner function
	# sin(gamma(5)) ← the last parenthesis
	return(str(result) + proto_inner[1])


def factorial_function(arg):
	'''Evaluate factorials.

	Interprets x! mathematically as gamma(x + 1)
	if written with an "!" will only take numbers as an argument.
	In order of operations factorials come after exponents,
	but before modulus
	'''

	# doing the calculation
	return(math.gamma(float(arg) + 1))


def logarithm(log_arg, ln_arg):
	'''Solve logarithms.
	
	Log must be written with two arguments. Ln only takes one argument
	and is evaluated separately from log.
	'''

	# logarithms written as log(x, y) where y
	# is the base and written as ln(x)
	if log_arg is not None:  # if written as log(x, y)

		# find the arguments of the function and cut off
		# everything else
		# sin(log(4, 2)) ← the last parenthesis
		proto_inner = find_match(log_arg)

		# separate the arguments based on commas that are not
		# within more than one set of parentheses
		log_args = separate(proto_inner[0][1:-1])

		# evaluate the arguments individually into a form
		# that math.log can accept
		argument = float(simplify(log_args[0]))
		base = float(simplify(log_args[1]))

		# perform the logarithm
		if base == 2:
			result = math.log2(argument)
		elif base == 10:
			result = math.log10(argument)
		else:
			result = math.log(argument, base)
		
		return(str(result) + proto_inner[1])

	elif ln_arg is not None:  # if written as ln(x)

		# find the argument of the function and cut off
		# everything else
		# sin(ln(e)) ← the last parenthesis
		proto_inner = find_match(ln_arg)

		# perform the logarithm
		result = math.log(float(simplify(proto_inner[0])))
	
	else:
		raise CalculatorError("log_arg or ln_arg must be something not None")

	# add on anything that was was cut off the end when finding
	# the arguments
	# sin(log(4, 2)) ← the last parenthesis
	return(str(result) + proto_inner[1])


def modulus_function(arg):
	'''Find the modulus of the input as a function not an operator.'''

	# find the arguments of the function and cut off
	# everything else
	# sin(mod(5, 2)) ← the last parenthesis
	proto_inner = find_match(arg)

	# separate the arguments based on commas that are not
	# within more than one set of parentheses
	mod_args = separate(proto_inner[0][1:-1])

	# evaluate the arguments individually into a form that fmod
	# can accept
	inner1 = float(simplify(mod_args[0]))
	inner2 = float(simplify(mod_args[1]))

	# do the actual modulation
	result = math.fmod(inner1, inner2)

	# add on anything that was was cut off the end when finding
	# the arguments
	# sin(mod(5, 2)) ← the last parenthesis
	return(str(result) + proto_inner[1])


def abs_value(input):
	'''Break up a expression based on where pipes are and return the
	the absolute value of what is in them.
	'''

	parts = input.split("|")

	for i in range(len(parts)):
		if parts[i].startswith(("+", "*", "^", "/")) or\
			parts[i].endswith(("+", "*", "^", "/", "-")) or\
			not parts[i]:
			pass

		else:
			result = math.fabs(float(simplify(parts[i])))
			last = ""
			iter_last = []
			next = ""
			iter_next = []

			if i > 0:
				last = parts[i - 1]
				if i > 1:
					iter_last = parts[:i - 1]

			if i < len(parts) - 1:
				next = parts[i + 1]
				if i < len(parts) - 2:
					iter_next = parts[i + 2:]

			result = last + str(result) + next
			result = "|".join(iter_last + [result] + iter_next)

			return(result)


# main func
def simplify(s):
	'''Simplify an expression.'''

	global degree_mode

	# iterates over all the operations
	for i in operations:

		# solution to scientific notation being mistaken
		# for the constant e
		if i == const_comp:
			try:
				s = float_to_str(s)
			except (ValueError, TypeError):
				pass

		# checks for the operation
		m = i.search(s)

		# continues until all instances of an
		# operation have been dealt with
		while m is not None:

			if i == command_comp:
				# non-math commands

				# display history
				if m.group(1) is not None:
					print(history[-1 * hist_len:])

				# exit the program
				elif m.group(2) is not None:
					sys.exit()

				# set degree mode on for the session
				elif m.group(3) is not None:
					switch_degree_mode(2)

				# set degree mode off for the session
				elif m.group(4) is not None:
					switch_degree_mode(0)
					
				else:
					raise CalculatorError("Command must be 'history',"
						" 'exit', 'quit', 'degree mode', or 'radian mode'")

				return(None)

			elif i == const_comp:

				result = constant_function(m.group(1))

			elif i == graph_comp:

				g = graph_function(m.group(1))
				return(None)

			elif i == alg_comp:

				result = solve_equations(m.group(1))

			elif i == eval_comp:

				result = evaluate_function(m.group(1), m.group(2))

			elif i == der_comp:

				if m.group(3) is not None:
					result = find_derivative(m.group(1), m.group(2),
					var = m.group(3)[-1])
				else:
					result = find_derivative(m.group(1), m.group(2))

			elif i == int_comp:

				result = integrate_function(m.group(1), m.group(2),
				m.group(3), m.group(4))

			elif i in (comb_comp, choos_comp):

				if i == comb_comp:
					result = combinations_and_permutations("func",
						m.group(1), m.group(2))
				elif i == choos_comp:
					result = combinations_and_permutations("choose",
						m.group(2), m.group(1), m.group(3))

			elif i == ave_comp:

				result = statistics_functions(m.group(1), m.group(2))

			elif i == trig_comp:

				result = single_argument(m.group(1), m.group(2))

			elif i in (gamma_comp, fact_comp):

				# the user inputed the gamma function
				if i == gamma_comp:
					result = gamma_function(m.group(1))

				elif i == fact_comp:  # the user inputed a factorial
					result = factorial_function(m.group(1))
				
				else:
					raise CalculatorError("How could this possibly happen?"
						" It just tested if i was 'gamma_comp' or "
						"'fact_comp'.")

			elif i == log_comp:

				result = logarithm(m.group(1), m.group(2))

			elif i == abs_comp:

				result = abs_value(s)

			elif i == paren_comp:

				# recursively evaluates the innermost parentheses
				result = simplify(m.group(1))

			elif i == comma_comp:

				# just concatenates whats on either side
				# of the parentheses unless its separating
				# arguments of a function

				result = float(m.group(1) + m.group(2))

			elif i == exp_comp:

				# exponents

				result = float(m.group(1)) ** float(m.group(3))

			elif i in (mod_comp, mod2_comp):

				# modulus written as both mod(x, y) and x % y
				# where x is the dividend and y is the divisor
				# if written as x % y it will only take numbers
				# for arguments. In order of operations modulus comes
				# after exponents and factorials, but before
				# multiplication and division

				if i == mod2_comp:

					result = modulus_function(m.group(1))

				elif i == mod_comp:

					# the x % y format
					result = math.fmod(float(m.group(1)),
					float(m.group(2)))
				
				else:
					raise CalculatorError("How could this possibly happen?"
						" It just tested if i was 'mod2_comp' or "
						"'mod_comp'.")

			elif i == per_comp:

				# percentage signs act just like dividing by 100

				result = "/100"

			elif i == mult_comp:

				# multiplication and division

				if m.group(2) == "*":

					result = float(m.group(1)) * float(m.group(3))

				elif m.group(2) in ("/", "÷"):

					result = float(m.group(1)) / float(m.group(3))
					
				else:
					raise CalculatorError("Mult_comp must match '*', '//', "
						"or '÷'.")

			elif i == add_comp:

				# addition and subtraction

				if m.group(2) == "+":

					result = math.fsum((float(m.group(1)),
					float(m.group(3))))

				elif m.group(2) == "-":

					result = float(m.group(1)) - float(m.group(3))
					
				else:
					raise CalculatorError("add_comp must match '+' or '-'.")
			
			else:
				print("function not implemented.", i)

			if i not in (command_comp, const_comp,
			alg_comp, eval_comp, der_comp):

				# this is a fix for python returning
				# answers in scientific notation which since
				# it has e it mistakes the constant e
				try:
					result = float_to_str(result)
				except (ValueError, TypeError):
					pass

			# replace the text matched by i (the regular expression)
			# with the result of the mathematical expression
			s = sub(i, str(result), s, count = 1)

			m = i.search(s)
	try:
		s = float_to_str(s)
	except (ValueError, TypeError):
		pass
	return(s)


# pre and post processing for console
def ask(s = None):
	'''Ask the user what expression they want to simplify
	and do pre and post processing.
	'''

	global ans
	if s is None:

		# get input from the user
		s = input("input an expression: ")

		# add the user input to the history
		history.append(s)

		# save history to file
		save_info()

	# evaluate the expression
	out = simplify(s)

	# save output to be used by the user
	ans = out

	# display the output
	if out is not None:
		print(s + " = " + out)
	print("")

	# save answer to file to be used next session
	save_info()


def key_pressed(event):
	'''Handle keys pressed in the GUI.'''

	global up_hist

	try:
		code = event.keycode
	except AttributeError:
		code = event

	# print(code)

	# get the user input when enter is pressed
	if code == key_binds[os.name][0]:  # enter
		get_input()

	# go backwards in the history when the up arrow is pressed
	if code == key_binds[os.name][1]:  # up arrow
		up_hist += 1
		input_widget.delete(0, "end")
		input_widget.insert(0, history[-1 * up_hist])

	# go forwards in the history when the down arrow is pressed
	if code == key_binds[os.name][2]:  # down arrow
		if up_hist > 1:
			up_hist -= 1
			input_widget.delete(0, "end")
			input_widget.insert(0, history[-1 * up_hist])

	# if you are not navigating the history stop keeping
	# track of where you are
	if code not in (key_binds[os.name][1], key_binds[os.name][2]):
		up_hist = 0


def input_backspace():
	'''Delete the last character in the entry widget.'''

	global input_widget

	# delete the last character in the input widget
	a = input_widget.get()
	input_widget.delete(0, "end")
	input_widget.insert(0, a[:-1])


def get_input(s = None):
	'''Get user input from the entry widget.'''

	global ans, mess

	if s is None:
		pre_s = input_widget.get()
		if pre_s != "":
			s = pre_s

	if s == "":
		if os.name == "posix":
			exit()
		elif os.name == "nt":
			sys.exit()
	
	if s is not None:
		
		# add the user input to the history
		history.append(s)

		# save history to file
		save_info()

		out = simplify(s)

		# save output to be used by the user
		ans = out

		# display the output
		if out is not None:
			mess.set(s + " = " + out)

		# save answer to file to be used next session
		save_info()

		# clear the input box
		input_widget.delete(0, "end")


def switch_trig():
	'''Put the trig function buttons on the GUI.'''

	# remove the buttons for the hyperbolic functions, misc functions,
	# and stats functions
	for i in range(12):
		hyperbolic_func_buttons[i].grid_forget()
		try:
			misc_func_buttons[i].grid_forget()
		except IndexError:
			pass
		try:
			stats_func_buttons[i].grid_forget()
		except IndexError:
			pass

	for i in range(12):
		trig_func_buttons[i].grid(row = i // 3 + 3, column = i % 3 + 8)


def switch_hyperbolic():
	'''Put the hyperbolic function buttons in the GUI.'''

	# remove the buttons for the trig functions, misc functions,
	# and stats functions
	for i in range(12):
		trig_func_buttons[i].grid_forget()
		try:
			misc_func_buttons[i].grid_forget()
		except IndexError:
			pass
		try:
			stats_func_buttons[i].grid_forget()
		except IndexError:
			pass

	for i in range(12):
		hyperbolic_func_buttons[i].grid(row = i // 3 + 3,
			column = i % 3 + 8)


def switch_misc():
	'''Put the miscellaneous function buttons on the GUI.'''

	# remove the buttons for the trig functions, hyperbolic functions,
	# and stats functions
	for i in range(12):
		trig_func_buttons[i].grid_forget()
		hyperbolic_func_buttons[i].grid_forget()
		try:
			stats_func_buttons[i].grid_forget()
		except IndexError:
			pass

	for i in range(10):
		misc_func_buttons[i].grid(row = i // 3 + 3, column = i % 3 + 8)


def switch_stats():
	'''Put the statistics function buttons in the GUI.'''

	# remove the buttons for the trig functions, misc functions,
	# and hyperbolic functions
	for i in range(12):
		trig_func_buttons[i].grid_forget()
		hyperbolic_func_buttons[i].grid_forget()
		try:
			misc_func_buttons[i].grid_forget()
		except IndexError:
			pass

	# mean median mode
	for i in range(6):
		stats_func_buttons[i].grid(row = i // 3 + 3,
			column = i % 3 + 8)


def format_default_screen():
	'''Put the buttons in place on the GUI'''

	# 7 8 9
	digit_button[7].grid(row = 3, column = 0)
	digit_button[8].grid(row = 3, column = 1)
	digit_button[9].grid(row = 3, column = 2)

	# 4 5 6
	digit_button[4].grid(row = 4, column = 0)
	digit_button[5].grid(row = 4, column = 1)
	digit_button[6].grid(row = 4, column = 2)

	# 1 2 3
	digit_button[1].grid(row = 5, column = 0)
	digit_button[2].grid(row = 5, column = 1)
	digit_button[3].grid(row = 5, column = 2)

	# 0 .
	digit_button[0].grid(row = 6, column = 0)
	digit_button[10].grid(row = 6, column = 1)  # .

	digit_button[11].grid(row = 3, column = 4)  # +
	digit_button[12].grid(row = 3, column = 5)  # -
	digit_button[13].grid(row = 4, column = 4)  # *
	digit_button[14].grid(row = 4, column = 5)  # ÷
	digit_button[15].grid(row = 5, column = 4)  # ^
	digit_button[16].grid(row = 5, column = 5)  # !
	digit_button[17].grid(row = 6, column = 4)  # π
	digit_button[18].grid(row = 6, column = 5)  # e
	digit_button[19].grid(row = 3, column = 6)  # (
	digit_button[20].grid(row = 3, column = 7)  # )
	digit_button[21].grid(row = 4, column = 6)  # |
	digit_button[22].grid(row = 4, column = 7)  # ,
	digit_button[23].grid(row = 5, column = 6)  # ∫
	digit_button[24].grid(row = 5, column = 7)  # x

	equals_button.grid(row = 6, column = 2)  # =
	back_button.grid(row = 3, column = 12)  # backspace

	# the functions menubutton
	menubar.grid(row = 3, column = 11)

	switch_trig()


def switch_matrices():
	'''Create window for dealing with matrices.'''

	pass


def graph_win_key_press(event, index):
	'''Deal with key presses while editing the graph window.'''

	global g_bound_entry

	try:
		code = event.keycode
	except AttributeError:
		code = event

	if code == key_binds[os.name][1] and index > 0:
		g_bound_entry[g_bound_names[index - 1]].focus()
	if code == key_binds[os.name][2] and\
		index < len(g_bound_names) - 1:
		g_bound_entry[g_bound_names[index + 1]].focus()


def edit_graph_window():
	'''Change the graph window options.'''

	global g_bound_entry, g_bound_string

	root = tk.Toplevel()

	g_bound_entry = {}
	g_bound_string = {}
	g_bound_disp = {}
	for index, val in enumerate(g_bound_names):
		g_bound_entry[val] = tk.Entry(root)

		g_bound_entry[val].grid(row = index, column = 1)

		g_bound_string[val] = tk.StringVar()
		g_bound_string[val].set(val + " = " + str(win_bound[val]))

		g_bound_disp[val] = tk.Message(root,
			textvariable = g_bound_string[val],
			width = 100)

		g_bound_disp[val].grid(row = index, column = 0)

		g_bound_entry[val].bind("<Key>",
			lambda event, i = index: graph_win_key_press(event, i))

	root.bind("<Return>", lambda a: change_graph_win_set())

	root.mainloop()


def tkask(s = None):
	'''Make a GUI for the program.'''

	global input_widget, mess
	global digit_button, equals_button, back_button, menubar
	global trig_func_buttons, inverse_trig_func_buttons
	global hyperbolic_func_buttons, inverse_hyperbolic_func_buttons
	global misc_func_buttons, stats_func_buttons

	root = tk.Tk()

	root.title("Calculator")

	if os.name == "nt":
		root.iconbitmap(default = os.path.join(calc_path,
		"calc_pic.ico"))

	mess = tk.StringVar()
	mess.set("Input an expression")

	# output text widget
	output_mess_widget = tk.Message(root, textvariable = mess,
	width = 200)
	output_mess_widget.grid(row = 0, column = 0, columnspan = 11)

	# input text widget
	input_widget = tk.Entry(root, width = 90)
	input_widget.grid(row = 1, column = 0, columnspan = 12)

	# list of basic buttons
	button_keys = list(range(10)) + [
		".", "+", "-", "*", "÷", "^", "!", "π", "e", "(", ")", "|",
		",", "∫", "x"]

	# creating of the basic buttons
	digit_button = list(tk.Button(root, text = str(i),
	command = lambda k = i: input_widget.insert("end", k),
	width = 5) for i in button_keys)

	# equals button
	equals_button = tk.Button(root, text = "=",
	command = get_input, width = 5, bg = "light blue")

	# backspace button
	back_button = tk.Button(root, text = "delete",
	command = input_backspace, width = 5)

	# list of trig functions
	trig_funcs = ("sin(", "cos(", "tan(", "sec(", "csc(", "cot(",
	"arcsin(", "arccos(", "arctan(", "arcsec(", "arccsc(", "arccot(")

	# creating of trig function buttons
	trig_func_buttons = list(tk.Button(root, text = i[:-1],
	command = lambda k = i: input_widget.insert("end", k),
	width = 5) for i in trig_funcs)

	# list of hyperbolic functions
	hyperbolic_funcs = ("sinh(", "cosh(", "tanh(", "sech(", "csch(",
	"coth(", "arcsinh(", "arccosh(", "arctanh(", "arcsech(",
	"arccsch(", "arccoth(")

	# creation of hyperbolic function buttons
	hyperbolic_func_buttons = list(tk.Button(root, text = i[:-1],
	command = lambda k = i: input_widget.insert("end", k),
	width = 5) for i in hyperbolic_funcs)

	# list of misc fuctions
	misc_funcs = ("log(", "ln(", "Γ(", "abs(", "ceil(", "floor(",
	"erf(", "mod(", "C(", "P(")

	# creation of misc function buttons
	misc_func_buttons = list(tk.Button(root, text = i[:-1],
	command = lambda k = i: input_widget.insert("end", k),
	width = 5) for i in misc_funcs)

	# list of stats functions
	stats_funcs = ("mean(", "median(", "mode(", "stdev(", "max(",
	"min(")

	# creation of stats buttons
	stats_func_buttons = list(tk.Button(root, text = i[:-1],
	command = lambda k = i: input_widget.insert("end", k),
	width = 5) for i in stats_funcs)

	# more functions button
	menubar = tk.Menubutton(root, text = "Functions",
	relief = "raised")
	dropdown = tk.Menu(menubar, tearoff = 0)
	dropdown.add_command(label = "Trig Functions",
	command = switch_trig)
	dropdown.add_command(label = "Hyperbolic Functions",
	command = switch_hyperbolic)
	dropdown.add_command(label = "Misc Functions",
	command = switch_misc)
	dropdown.add_command(label = "Stats Functions",
	command = switch_stats)

	menubar.config(menu = dropdown)

	# menu at top right of screen
	options_menu = tk.Menu(root)
	list_options = tk.Menu(options_menu, tearoff = 0)

	list_options.add_command(label = "Radian Mode",
	command = lambda: switch_degree_mode("radian"))

	list_options.add_command(label = "Degree Mode",
	command = lambda: switch_degree_mode("degree"))

	list_options.add_command(label = "Polar Mode",
	command = lambda: switch_polar_mode("polar"))

	list_options.add_command(label = "Cartesian Mode",
	command = lambda: switch_polar_mode("Cartesian"))

	list_options.add_command(label =
	"Change length of history print back",
	command = change_hist_len_win)

	list_options.add_command(label = "Change der approx",
	command = change_der_approx_win)

	options_menu.add_cascade(label = "Options", menu = list_options)

	# list of other things the calculator can do
	matrices_plus = tk.Menu(options_menu, tearoff = 0)
	matrices_plus.add_command(label = "Matrices",
	command = switch_matrices)
	matrices_plus.add_command(label = "Window",
	command = edit_graph_window)
	options_menu.add_cascade(label = "Things", menu = matrices_plus)

	root.config(menu = options_menu)

	format_default_screen()

	root.bind("<Key>", key_pressed)
	
	get_input(s = s)

	root.mainloop()


if __name__ == "__main__":
	# default startup
	if len(sys.argv) == 1:
		if "tkinter" in sys.modules and use_gui:
			tkask()
		else:
			while True:
				ask()

	else:  # handling command line arguments and startup
		if "tkinter" in sys.modules and use_gui:
			tkask(" ".join(sys.argv[1:]))
		else:
			ask(" ".join(sys.argv[1:]))

	# main loop if command line arguments passed
	if "tkinter" in sys.modules and use_gui:
		pass
	else:
		while True:
			ask()
