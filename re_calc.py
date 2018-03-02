# -*- coding: utf-8 -*-


#   Calculator\re_calc.py

import math
import statistics as stats
import sys
import os

from pickle import load, dump
from re import compile, sub
from sympy import symbols, integrate, sympify
from sympy.solvers import solve


try:
	import tkinter as tk
except ModuleNotFoundError:
	pass


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
25) summation
26) big pi notation
27) series
29) cut off trailing zeros
30) two expressions adjacent means multiplication
32) 3d graphs
34) make icon of tkinter window when run on Fedora
35) make compatible with other operating systems
36) fix polar graphing of cardioid
37) fix 2-2*sin(6)
38) 
'''


'''  Test inputs
log(mean(ln(e^2),ln(e**2),mode(4),4*sin(arccos(-1)/2))+C(5C1,1),2!) = 3
graph x/2 -1 from -10 to 2
solve(2*r+4=r) for r  = -4
'''

# os handling
if os.name == "nt":
    user_path = os.environ["USERPROFILE"]
elif os.name == "posix":
    user_path = os.environ["HOME"]

# changeable variables
use_gui = True
graph_w = 400
graph_h = 400
graph_colors = ("black", "red", "blue", "green", "orange", "purple")

# variables used in multiple functions
x_min_str, x_max_str, y_min_str, y_max_str = (None, None, None, None)
x_min_entry, x_max_entry, y_min_entry, y_max_entry = (None,
	None, None, None)
theta_min_str, theta_max_str = (None, None)
theta_min_entry, theta_max_entry = (None, None)
input_widget = None
equals_button = None
back_button = None
menubar = None
up_hist = 0
digit_button = []
trig_func_buttons = []
hyperbolic_func_buttons = []
misc_func_buttons = []
stats_func_buttons = []

# multi session variables
calc_path = os.path.abspath(os.path.dirname(__file__))
calc_info = load(open(
	os.path.join(calc_path, "re_calc_info.txt"), "rb"))
history = calc_info[0]
ans = calc_info[1]
options = calc_info[2]
degree_mode = options[0]  # in degree mode 0 = off 2 = on
polar_mode = options[1]
der_approx = options[2]  # default = .0001
hist_len = options[3]
win_bound = calc_info[3]

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
	"ans(?:wer)?|tau|τ)")
	const_comp = compile(const_reg)

	# regex for graphing
	graph_reg = "[Gg]raph (.+)"
	graph_comp = compile(graph_reg)

	# regex for equation solving
	alg_reg = "[Ss]olve(.+)"
	alg_comp = compile(alg_reg)

	# regex for evaluating functions
	eval_reg = "[Ee]val(?:uate)? (.+?) (?:for|at) (.+)"
	eval_comp = compile(eval_reg)

	# regex for derivatives (must be at a number)
	der_reg = "[Dd]erivative of (.+) at "+reg_num
	der_comp = compile(der_reg)

	# regex for integrals (bounds must be numbers)
	int_reg = ("(?:[Ii]ntegra(?:te|l)|∫) (.+)d([a-z])"
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
	# the order does matter because of trig functions come
	# before hyperbolic functions the "h" is interpreted as
	# part of the argument for the function
	trig_reg = ("("
	"sinh|cosh|tanh|asinh|acosh|atanh|"
	"arcsinh|arccosh|arctanh|"
	"sech|csch|coth|asech|acsch|acoth|"
	"arcsech|arccsch|arccoth|"
	"sin|cos|tan|sec|csc|cot|"
	"asin|arcsin|acos|arccos|atan|arctan|"
	"asec|acsc|acot|arcsec|arccsc|arccot|"
	"abs|ceil|floor|erf"
	")(.+)")
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


def check_if_float(x):
	"""Test if a object can be made a float."""

	try:
		float(x)
		return(True)
	except (ValueError, TypeError):
		return(False)


def save_info():
	"""Save options, history and other stuff to a file."""

	global calc_info

	calc_info = [history, ans, options, win_bound]

	dump(calc_info, open(os.path.join(calc_path,
	"re_calc_info.txt"), "wb"))


def switch_degree_mode(mode):
	"""Switch between degree mode and radian mode."""

	global degree_mode

	if mode == "degree":
		mode = 2
	elif mode == "radian":
		mode = 0

	degree_mode = mode
	options[0] = degree_mode
	save_info()


def switch_polar_mode(mode):
	"""Switch between polar and Cartesian graphing."""

	global polar_mode

	if mode == "polar":
		mode = True
	if mode == "Cartesian":
		mode = False

	polar_mode = mode
	options[1] = polar_mode
	save_info()


def change_hist_len(entry_box, root):
	"""Change the length of the hisstory print back."""

	global hist_len

	# get user input
	input = entry_box.get()

	# if the input is a digit set that to be the
	# history print back length save and close the window
	if input.isdigit():
		hist_len = int(input)
		options[3] = hist_len
		save_info()

		root.destroy()
	else:
		pass


def change_hist_len_win():
	"""Create a popup to change the length of the
	history print back.
	"""

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
	"""Change the length of the history print back."""

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
	"""Create a popup to change the lenght of the
	history print back.
	"""

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
	"""Change the graphing window bounds."""

	global win_bound
	global x_min_str, x_max_str, y_min_str, y_max_str
	global x_min_entry, x_max_entry, y_min_entry, y_max_entry
	global theta_min_str, theta_max_str
	global theta_min_entry, theta_max_entry

	xmin_in = x_min_entry.get()
	xmax_in = x_max_entry.get()
	ymin_in = y_min_entry.get()
	ymax_in = y_max_entry.get()
	theta_min_in = theta_min_entry.get()
	theta_max_in = theta_max_entry.get()

	if check_if_float(xmin_in):
		win_bound["xmin"] = float(xmin_in)
	if check_if_float(xmax_in):
		win_bound["xmax"] = float(xmax_in)
	if check_if_float(ymin_in):
		win_bound["ymin"] = float(ymin_in)
	if check_if_float(ymax_in):
		win_bound["ymax"] = float(ymax_in)
	if check_if_float(theta_min_in):
		win_bound["theta_max"] = float(theta_max_in)
	if check_if_float(theta_max_in):
		win_bound["theta_max"] = float(theta_max_in)

	save_info()

	x_min_str.set("x min = " + str(win_bound["xmin"]))
	x_max_str.set("x max = " + str(win_bound["xmax"]))
	y_min_str.set("y min = " + str(win_bound["ymin"]))
	y_max_str.set("y max = " + str(win_bound["ymax"]))
	theta_min_str.set("theta min = " + str(win_bound["theta_min"]))
	theta_max_str.set("theta max = " + str(win_bound["theta_max"]))
	


def find_match(s):
	"""Find matching parentheses."""

	x = 0
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

	try:
		return(an, left)
	except Exception:
		print("error ", s, " is an invalid input.")
		raise ValueError


def brackets(s):
	"""Inform separate whether parentheses match."""

	x = 0
	for i in s:
		if i == "(":
			x += 1
		elif i == ")":
			x -= 1
	return(x)


def separate(s):
	"""Split up arguments of a function with commas
	like mod(x, y) or log(x, y) based on where commas that are only
	in one set of parentheses.
	"""

	# separate based on all commas
	terms = s.split(",")

	new_terms = []
	middle = False

	# iterate of over the groups separated by commas
	for i in range(len(terms)):

		# check if it is in the middle of a group of parentheses
		if middle is False:
			next_term = terms[i]

		# reevaluate if its in the middle of parentheses
		x = brackets(next_term)

		# if its not in the middle add the curren term to final list
		if x == 0:
			new_terms.append(terms[i])
			continue

		# if it is in the middle of a group
		if x > 0:

			# add the current term to the string of previous terms
			next_term = next_term + "," + terms[i + 1]

			# check if that was the end of the group
			if brackets(next_term) == 0:
				new_terms.append(next_term)
				middle = False
			else:
				middle = True

	return(new_terms)


class graph(object):
	"""Cartesian Graphing window class."""

	def __init__(self,
	xmin = -5, xmax = 5, ymin = -5, ymax = 5,
	wide = 400, high = 400):  # all the arguments you pass the object
		"""Initialize the graphing window."""

		self.root = tk.Toplevel()

		self.root.title("Calculator")

		# sets bounds
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax

		# dimensions of the window
		self.wide = wide
		self.high = high

		# create the canvas
		self.screen = tk.Canvas(self.root,
		width = wide, height = high)
		self.screen.pack()

		# button that close the window and program immediately
		self.close = tk.Button(self.root, text = "Close",
		command = self.root.destroy)
		self.close.pack()

		# draws the axes
		self.axes()

	# draw the axes
	def axes(self):
		"""Draw the axis on a Cartesian graph."""

		xrang = self.xmax - self.xmin
		yrang = self.ymax - self.ymin

		# adjusted y coordinate of x-axis
		b = self.high + (self.ymin * self.high / yrang)

		# draw x-axis
		self.screen.create_line(0, b, self.wide, b, fill = "gray")

		# adjusted x coordinate of y-axis
		a = -1 * self.xmin * self.wide / xrang

		# draw y-axis
		self.screen.create_line(a, self.high, a, 0, fill = "gray")

		self.root.update()

	def draw(self, func, color = "black"):
		"""Draw a Cartesian function."""

		density = 1000
		x = self.xmin
		xrang = self.xmax - self.xmin
		yrang = self.ymax - self.ymin

		while x < self.xmax:

			# move the x coordinate a little
			x += xrang / density
			try:
				# eval the function at x and set that to y
				y = float(evaluate_function(
					eval_comp.search("eval " + func + " at " + str(x))))

				# check if the graph goes off the screen
				if y > self.ymax or y < self.ymin and density > 2000:
					denstiy = 2000
				else:
					# find the slope at the point using the derivative
					# function of simplify
					try:
						slope = float(find_derivative(
							der_comp.search("derivative of "
							+ func + " at " + str(x))))
					except:
						slope = 10

					# calculate how dense the points need to be
					# this function is somewhat arbitrary
					density = int((3000 * math.fabs(slope)) / yrang + 500)

				# adjust coordinate for the screen (this is the
				# hard part)
				a = (x-self.xmin) * self.wide / xrang
				b = self.high - ((y - self.ymin) * self.high / yrang)

				# draw the point
				self.screen.create_line(a, b, a + 1, b, fill = color)
			except:
				pass

			# update the screen
			try:
				self.root.update()
			except:
				x = self.xmax + 1


class polar_graph(graph):
	"""Polar graphing window class."""

	def __init__(self,
	xmin = -5, xmax = 5, ymin = -5, ymax = 5,
	theta_min = 0, theta_max = 10,
	wide = 400, high = 400):  # all the arguments you pass the object
		"""Initialize polar graphing window."""

		self.root = tk.Toplevel()

		self.root.title("Calculator")

		# sets bounds
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.theta_min = theta_min
		self.theta_max = theta_max

		# dimensions of the window
		self.wide = wide
		self.high = high

		# create the canvas
		self.screen = tk.Canvas(self.root,
		width = wide, height = high)
		self.screen.pack()

		# button that close the window and program immediately
		self.close = tk.Button(self.root, text = "Close",
		command = self.root.destroy)
		self.close.pack()

		# draw axes
		self.axes()

	def draw(self, func, color = "black"):
		"""Draw a polar function."""

		density = 1000
		theta = self.theta_min
		theta_rang = self.theta_max - self.theta_min
		xrang = self.xmax - self.xmin
		yrang = self.ymax - self.ymin

		while theta < self.theta_max:

			# move theta a little
			theta += theta_rang / density
			try:
				# eval the function at theta and set that to r
				r = float(evaluate_function(
					eval_comp.search("eval "
					+ func + " at " + str(theta))))

				# find the slope at the point using find_derivative
				slope = float(find_derivative(
					der_comp.search("derivative of " + func + " at "
					+ str(theta))))

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
				a = (x - self.xmin) * self.wide / xrang
				b = self.high - ((y - self.ymin) * self.high / yrang)

				# draw the point
				self.screen.create_line(a, b, a + 1, b, fill = color)
			except:
				pass

			# update the screen
			try:
				self.root.update()
			except:
				theta = self.theta_max + 1


#####################
# List of Functions #
#####################

def constant_function(m):
	"""Evaluate mathematical constants."""

	# pi
	if m.group(1) in ("pi", "π"):
		return(math.pi)

	# e
	elif m.group(1) == "e":
		return(math.e)

	# the output of the previous query
	elif m.group(1) in ("ans", "answer"):
		return(ans)

	# tau (equivalent to 2*pi)
	elif m.group(1) in ("tau", "τ"):
		return(math.tau)

	# should never happen debugging use only
	else:
		print("Unknown constant: ", m.group(0))
		raise ValueError


def graph_function(m):
	"""Graph the given function."""

	# looks for x bounds on the graph
	range_m = graph_rang_comp.search(m.group(1))
	if range_m is not None:
		m = range_m

	# checks to see if tkinter is installed to graph things at all
	if "tkinter" in sys.modules:

		# finds multiple functions to graph
		funcs_to_graph = m.group(1).split(" and ")

		# sets bounds to bounds given
		if range_m is None:
			temp_graph_xmin = win_bound["xmin"]
			temp_graph_xmax = win_bound["xmax"]
		else:
			temp_graph_xmin = float(m.group(3))
			temp_graph_xmax = float(m.group(4))

		# creates graph object
		if polar_mode is False:
			made_graph = graph(
				xmin = temp_graph_xmin, xmax = temp_graph_xmax,
				ymin = win_bound["ymin"], ymax = win_bound["ymax"],
				wide = graph_w, high = graph_h)
		else:
			made_graph = polar_graph(
				xmin = temp_graph_xmin, xmax = temp_graph_xmax,
				ymin = win_bound["ymin"], ymax = win_bound["ymax"],
				theta_min = win_bound["theta_min"],
				theta_max = win_bound["theta_max"],
				wide = graph_w, high = graph_h)

		# works out how many times it needs to
		# loop the colors its using
		color_loops = math.ceil(len(funcs_to_graph)
		/ len(graph_colors))

		# passes functions to be graphed and the color to do so with
		for f, c in zip(funcs_to_graph, graph_colors * color_loops):
			made_graph.draw(f, color = c)

	# informs the user of reason for failure
	else:
		print("Could not graph. Tkinter is not installed")


def solve_equations(m):
	"""Solve equations using sympy. If there is no equals
	sign it is assumed the expression equals zero.
	"""

	# find if there is a specified variable
	varm = alg_var_comp.search(m.group(1))

	# find the variable its solving for. defaults to "x"
	if varm is None:
		x = symbols("x")
		eq = m.group(1)
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


def evaluate_function(m):
	"""Evaluate the function by substituting x for the number you
	want to evaluate at.
	"""

	# substituting the point for x in the function and evaluating
	# that recursively
	return(simplify(sub("(?<![a-z])x",
	m.group(2), m.group(1))))


def find_derivative(m):
	"""Calculate the derivative by evaluating the slope
	between two points on either side of the point you are
	finding the derivative of.
	"""

	# find the point on either side of the desired point
	x_one = float(m.group(2)) + der_approx
	x_two = float(m.group(2)) - der_approx

	# find the change in y value between the two points
	delta_y = float(simplify("eval " + m.group(1) + " for "
	+ str(x_one))) - float(simplify("eval " + m.group(1) + " for "
	+ str(x_two)))

	# divide by the length of the interval to find the slope
	return(delta_y / (2 * der_approx))


def integrate_function(m):
	"""Integrate with sympy."""

	# Integrals must be in a form that sympy can integrate
	# The bounds must be numbers not expressions
	# The integral must have a "dx" or whatever variable you are using

	# using sympy to integrate
	return(integrate(m.group(1),
	(m.group(2), m.group(3), m.group(4))))


def combinations_and_permutations(m, i):
	"""Solve combinations and permutations."""

	# combinations and permutations written
	# both as C(5, 2) and 5C2 evaluated as: 5 choose 2
	# if written as mCn it will only take numbers not expressions
	# unless parentheses are used. In order of operations nCm comes
	# first.
	# Combinations and permutations both used the gamma function
	# in place of factorials and as a result will take
	# non-integer arguments

	if i == choos_comp:  # if written as nCm

		# turn the arguments into floats and give them more
		# descriptive names
		inner_n = float(m.group(1))
		inner_m = float(m.group(3))

		# find permutations
		temp_result = math.gamma(1 + inner_n) \
			/ math.gamma(1 + inner_n - inner_m)

		# if combinations also divide by m!
		if m.group(2) == "C":
			temp_result = temp_result / math.gamma(1 + inner_m)

		return(temp_result)

	else:  # if written as C(5, 2)

		# find the arguments of the function and cut off
		# everything else
		# sin(C(5, 2)) ← the last parenthesis
		proto_inner = find_match(m.group(2))

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
		if m.group(1) == "C":
			temp_result = temp_result / math.gamma(1 + inner_m)

		# add on anything that was was cut off the end when finding
		# the arguments
		# sin(C(5, 2)) ← the last parenthesis
		return(str(temp_result) + proto_inner[1])


def statistics_functions(m):
	"""Perform general statistics functions."""

	# this may in the future include any function that
	# can have an arbitrarily large number of arguments

	# find the arguments of the function and cut off
	# everything else
	# sin(mean(4, 2)) ← the last parenthesis
	proto_inner = find_match(m.group(2))

	# separate the arguments based on commas that are not
	# within more than one set of parentheses
	ave_args = separate(proto_inner[0][1:-1])

	# evaluate all the arguments
	list_ave = list(map((lambda x: float(simplify(x))), ave_args))

	# perform the different functions
	if m.group(1).lower() in ("ave", "average", "mean"):
		result = stats.mean(list_ave)
	if m.group(1).lower() == "median":
		result = stats.median(list_ave)
	if m.group(1).lower() == "mode":
		result = stats.mode(list_ave)
	if m.group(1).lower() == "max":
		result = max(list_ave)
	if m.group(1).lower() == "min":
		result = min(list_ave)
	if m.group(1).lower() in ("stdev"):
		result = stats.stdev(list_ave)

	# add on anything that was was cut off the end when finding
	# the arguments
	# sin(mean(4, 2)) ← the last parenthesis
	return(str(result) + proto_inner[1])


def single_argument(m):
	"""Evaluate trig functions and other unary operators."""

	global degree_mode

	# find the arguments of the function and cut off
	# everything else
	# tan(sin(π)) ← the last parenthesis when
	# evaluating sin
	proto_inner = find_match(m.group(2))

	# looks for the degree symbol in the argument
	# if the program finds it degree mode is set to true
	# for the particular operation
	if "°" in proto_inner[0] and degree_mode == 0:
		degree_mode = 1
		proto_inner[0] = sub("[°]", "", proto_inner[0])

	# evaluate the argument into a form that math.log
	# can accept
	inner = float(simplify(proto_inner[0]))

	# check if in degree mode and if its doing an
	# operation that takes an angle as an argument
	if degree_mode > 0:
		if m.group(1) in ("sin", "sec",
		"cos", "csc", "tan", "cot",
		"sinh", "cosh", "tanh"):
			inner = math.pi * inner / 180

	# trig functions and inverse trig functions
	if m.group(1) == "sin":
		result = math.sin(inner)
	if m.group(1) == "cos":
		result = math.cos(inner)
	if m.group(1) == "tan":
		result = math.tan(inner)
	if m.group(1) == "sec":
		result = 1/math.cos(inner)
	if m.group(1) == "csc":
		result = 1/math.sin(inner)
	if m.group(1) == "cot":
		result = 1/math.tan(inner)
	if m.group(1) in ("asin", "arcsin"):
		result = math.asin(inner)
	if m.group(1) in ("acos", "arccos"):
		result = math.acos(inner)
	if m.group(1) in ("atan", "arctan"):
		result = math.atan(inner)
	if m.group(1) in ("asec", "arcsec"):
		result = math.acos(1 / inner)
	if m.group(1) in ("acsc", "arccsc"):
		result = math.asin(1 / inner)
	if m.group(1) in ("acot", "arccot"):
		result = math.atan(1 / inner)

	# hyperbolic functions and inverse hyperbolic functions
	if m.group(1) == "sinh":
		result = math.sinh(inner)
	if m.group(1) == "cosh":
		result = math.cosh(inner)
	if m.group(1) == "tanh":
		result = math.tanh(inner)
	if m.group(1) == "sech":
		result = 1/math.cosh(inner)
	if m.group(1) == "csch":
		result = 1/math.sinh(inner)
	if m.group(1) == "coth":
		result = 1/math.tanh(inner)
	if m.group(1) in ("asinh", "arcsinh"):
		result = math.asinh(inner)
	if m.group(1) in ("acosh", "arccosh"):
		result = math.acosh(inner)
	if m.group(1) in ("atanh", "arctanh"):
		result = math.atanh(inner)
	if m.group(1) in ("asech", "arcsech"):
		result = math.acosh(1 / inner)
	if m.group(1) in ("acsch", "arccsch"):
		result = math.asinh(1 / inner)
	if m.group(1) in ("acoth", "arccoth"):
		result = math.atanh(1 / inner)

	# other single argument functions
	if m.group(1) == "abs":
		result = math.fabs(inner)
	if m.group(1) == "ceil":
		result = math.ceil(inner)
	if m.group(1) == "floor":
		result = math.floor(inner)
	if m.group(1) == "erf":
		result = math.erf(inner)

	# checks if its in degree mode (not because of
	# degree symbols in the argument) and if so
	# converts the answer to degrees for functions that
	# output an angle
	if m.group(1) in ("asin",
	"arcsin", "acos", "arccos", "atan", "arctan",
	"asinh", "arcsinh", "acosh", "arccosh",
	"atanh", "arctanh") and degree_mode == 2:
		result = result * 180 / math.pi

	# resets the degree mode for the session
	if degree_mode == 1:
		degree_mode = 0

	# this is a janky fix for the output being in
	# scientific notation and the program mistaking the
	# e for the constant e
	try:
		result = "{:.16f}".format(float(result))
	except (ValueError, TypeError):
		pass

	# add back anything that was cut off when finding the
	# argument of the inner function
	# tan(sin(π)) ← the last parenthesis when
	# evaluating sin
	return(str(result) + proto_inner[1])


def gamma_function(m):
	"""Use the gamma function."""

	# find the arguments of the function and cut off
	# everything else
	# sin(gamma(5)) ← the last parenthesis
	proto_inner = find_match(m.group(1))

	# evaluating the argument
	inner = float(simplify(proto_inner[0]))

	# doing the calculation
	result = math.gamma(inner)

	# add back anything that was cut off when finding the
	# argument of the inner function
	# sin(gamma(5)) ← the last parenthesis
	return(str(result) + proto_inner[1])


def factorial_function(m):
	"""Evaluate factorials."""

	# interprets x! mathematically as gamma(x + 1)
	# if written with an "!" will only take numbers as an argument.
	# In order of operations factorials come after exponents,
	# but before modulus

	# doing the calculation
	return(math.gamma(float(m.group(1)) + 1))


def logarithm(m):
	"""Solve logarithms."""

	# logarithms written as log(x, y) where y
	# is the base and written as ln(x)

	if m.group(1) is not None:  # if written as log(x, y)

		# find the arguments of the function and cut off
		# everything else
		# sin(log(4, 2)) ← the last parenthesis
		proto_inner = find_match(m.group(1))

		# separate the arguments based on commas that are not
		# within more than one set of parentheses
		log_args = separate(proto_inner[0][1:-1])

		# evaluate the arguments individually into a form
		# that math.log can accept
		argument = float(simplify(log_args[0]))
		base = float(simplify(log_args[1]))

		# perform the logarithm
		return(str(math.log(argument, base)) + proto_inner[1])

	elif m.group(2) is not None:  # if written as ln(x)

		# find the argument of the function and cut off
		# everything else
		# sin(ln(e)) ← the last parenthesis
		proto_inner = find_match(m.group(2))

		# perform the logarithm
		result = math.log(float(simplify(proto_inner[0])))

		# add on anything that was was cut off the end when finding
		# the arguments
		# sin(log(4, 2)) ← the last parenthesis
	return(str(result) + proto_inner[1])


def modulus_function(m):
	"""Find the modulus of the input."""

	# find the arguments of the function and cut off
	# everything else
	# sin(mod(5, 2)) ← the last parenthesis
	proto_inner = find_match(m.group(1))

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
	"""Break up a expression based on where pipes are and return the
	the absolute value of what is in them.
	"""

	parts = input.split("|")

	for i in range(len(parts)):
		if parts[i].startswith(("+", "*", "^", "/")) or\
		parts[i].endswith(("+", "*", "^", "/", "-")) or not parts[i]:
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
	"""Simplify an expression."""

	global degree_mode

	original = s

	# iterates over all the operations
	for i in operations:

		# janky solution to scientific notation being mistaken
		# for the constant e
		if i == const_comp:
			try:
				s = "{:.16f}".format(float(s))
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

				return(None)

			elif i == const_comp:

				result = constant_function(m)

			elif i == graph_comp:

				graph_function(m)
				return(None)

			elif i == alg_comp:

				result = solve_equations(m)

			elif i == eval_comp:

				result = evaluate_function(m)

			elif i == der_comp:

				result = find_derivative(m)

			elif i == int_comp:

				result = integrate_function(m)

			elif i in (comb_comp, choos_comp):

				result = combinations_and_permutations(m, i)

			elif i == ave_comp:

				result = statistics_functions(m)

			elif i == trig_comp:

				result = single_argument(m)

			elif i in (gamma_comp, fact_comp):

				# the user inputed the gamma function
				if i == gamma_comp:
					result = gamma_function(m)

				elif i == fact_comp:  # the user inputed a factorial
					result = factorial_function(m)

			elif i == log_comp:

				result = logarithm(m)

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

				# modulus written as both mod(x, y) and x%y
				# where x is the dividend and y is the divisor
				# if written as x%y it will only take numbers
				# for arguments. In order of operations modulus comes
				# after exponents and factorials, but before
				# multiplication and division

				if i == mod2_comp:

					result = modulus_function(m)

				else:

					# the x % y format
					result = math.fmod(float(m.group(1)),
					float(m.group(2)))

			elif i == per_comp:

				# percentage signs act just like dividing by 100

				result = "/100"

			elif i == mult_comp:

				# multiplication and division

				if m.group(2) == "*":

					result = float(m.group(1)) * float(m.group(3))

				elif m.group(2) in ("/", "÷"):

					result = float(m.group(1)) / float(m.group(3))

			elif i == add_comp:

				# addition and subtraction

				if m.group(2) == "+":

					result = math.fsum((float(m.group(1)),
					float(m.group(3))))

				elif m.group(2) == "-":

					result = float(m.group(1)) - float(m.group(3))

			if i not in (command_comp, const_comp,
			alg_comp, eval_comp, der_comp):

				# this is a janky fix for python returning
				# answers in scientific notation which since
				# it has e it mistakes the constant e

				try:
					result = "{:.16f}".format(result)
				except (ValueError, TypeError):
					pass

			# replace the text matched by i: the regular expression
			# with the result of the mathematical expression
			s = sub(i, str(result), s, count = 1)
			
			# print("result", "".join(m.groups()), " = ", result)
			# print("sub",s)
			
			m = i.search(s)
	try:
		s = "{:.16f}".format(s)
	except (ValueError, TypeError):
		pass
	return(s)


# pre and post processing for console
def ask(s = None):
	"""Ask the user what expression they want to simplify
	and do pre and post processing.
	"""

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
	"""Handle keys pressed in the gui."""

	global up_hist

	try:
		code = event.keycode
	except AttributeError:
		code = event

	key_binds = {"nt":(13, 38, 40), "posix":(104, 111, 116)}

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
	"""Delete the last character in the entry widget."""

	global input_widget

	# delete the last character in the input widget
	a = input_widget.get()
	input_widget.delete(0, "end")
	input_widget.insert(0, a[:-1])


def get_input():
	"""Get user input from the entry widget."""

	global ans, mess

	s = input_widget.get()

	# add the user input to the history
	history.append(s)

	# save history to file
	save_info()
	
	if s == "":
		if os.name == "posix":
			print("exit")
			exit()
		elif os.name == "nt":
			sys.exit()

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
	"""Use grid on the trig function buttons."""

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

	# sin cos tan
	trig_func_buttons[0].grid(row = 3, column = 8)
	trig_func_buttons[1].grid(row = 3, column = 9)
	trig_func_buttons[2].grid(row = 3, column = 10)

	# sec csc cot
	trig_func_buttons[3].grid(row = 4, column = 8)
	trig_func_buttons[4].grid(row = 4, column = 9)
	trig_func_buttons[5].grid(row = 4, column = 10)

	# arcsin arccos arctan
	trig_func_buttons[6].grid(row = 5, column = 8)
	trig_func_buttons[7].grid(row = 5, column = 9)
	trig_func_buttons[8].grid(row = 5, column = 10)

	# arcsec arccsc arccot
	trig_func_buttons[9].grid(row = 6, column = 8)
	trig_func_buttons[10].grid(row = 6, column = 9)
	trig_func_buttons[11].grid(row = 6, column = 10)


def switch_hyperbolic():
	"""Use grid on the trig function buttons."""

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

	# sinh cosh tanh
	hyperbolic_func_buttons[0].grid(row = 3, column = 8)
	hyperbolic_func_buttons[1].grid(row = 3, column = 9)
	hyperbolic_func_buttons[2].grid(row = 3, column = 10)

	# sech csch coth
	hyperbolic_func_buttons[3].grid(row = 4, column = 8)
	hyperbolic_func_buttons[4].grid(row = 4, column = 9)
	hyperbolic_func_buttons[5].grid(row = 4, column = 10)

	# arcsinh arccosh arctanh
	hyperbolic_func_buttons[6].grid(row = 5, column = 8)
	hyperbolic_func_buttons[7].grid(row = 5, column = 9)
	hyperbolic_func_buttons[8].grid(row = 5, column = 10)

	# arcsech arccsch arccoth
	hyperbolic_func_buttons[9].grid(row = 6, column = 8)
	hyperbolic_func_buttons[10].grid(row = 6, column = 9)
	hyperbolic_func_buttons[11].grid(row = 6, column = 10)


def switch_misc():
	"""Use grid on miscellaneous functions."""

	# remove the buttons for the trig functions, hyperbolic functions,
	# and stats functions
	for i in range(12):
		trig_func_buttons[i].grid_forget()
		hyperbolic_func_buttons[i].grid_forget()
		try:
			stats_func_buttons[i].grid_forget()
		except IndexError:
			pass

	# log ln gamma
	misc_func_buttons[0].grid(row = 3, column = 8)
	misc_func_buttons[1].grid(row = 3, column = 9)
	misc_func_buttons[2].grid(row = 3, column = 10)

	# abs ceil floor
	misc_func_buttons[3].grid(row = 4, column = 8)
	misc_func_buttons[4].grid(row = 4, column = 9)
	misc_func_buttons[5].grid(row = 4, column = 10)

	# erf mod C
	misc_func_buttons[6].grid(row = 5, column = 8)
	misc_func_buttons[7].grid(row = 5, column = 9)
	misc_func_buttons[8].grid(row = 5, column = 10)

	# P
	misc_func_buttons[9].grid(row = 6, column = 8)
	# misc_func_buttons[10].grid(row = 3, column = 9)
	# misc_func_buttons[11].grid(row = 3, column = 10)
	pass


def switch_stats():
	"""Use grid on statistics functions."""

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
	stats_func_buttons[0].grid(row = 3, column = 8)
	stats_func_buttons[1].grid(row = 3, column = 9)
	stats_func_buttons[2].grid(row = 3, column = 10)

	# stdev max min
	stats_func_buttons[3].grid(row = 4, column = 8)
	stats_func_buttons[4].grid(row = 4, column = 9)
	stats_func_buttons[5].grid(row = 4, column = 10)

	# stats_func_buttons[6].grid(row = 5, column=8)
	# stats_func_buttons[7].grid(row = 5, column=9)
	# stats_func_buttons[8].grid(row = 5, column=10)

	# stats_func_buttons[9].grid(row = 6, column = 8)
	# misc_func_buttons[10].grid(row = 6, column = 9)
	# misc_func_buttons[11].grid(row = 6, column = 10)
	pass


def format_default_screen():
	"""Use grid to put in place the buttons"""

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
	"""Create window for dealing with matrices."""

	pass


def edit_graph_window():
	"""Change the graph window options."""

	global x_min_str, x_max_str, y_min_str, y_max_str
	global x_min_entry, x_max_entry, y_min_entry, y_max_entry
	global theta_min_str, theta_max_str
	global theta_min_entry, theta_max_entry

	root = tk.Toplevel()

	x_min_entry = tk.Entry(root)
	x_max_entry = tk.Entry(root)
	y_min_entry = tk.Entry(root)
	y_max_entry = tk.Entry(root)
	theta_min_entry = tk.Entry(root)
	theta_max_entry = tk.Entry(root)

	x_min_str = tk.StringVar()
	x_min_str.set("x min = " + str(win_bound["xmin"]))

	x_max_str = tk.StringVar()
	x_max_str.set("x max = " + str(win_bound["xmax"]))

	y_min_str = tk.StringVar()
	y_min_str.set("y min = " + str(win_bound["ymin"]))

	y_max_str = tk.StringVar()
	y_max_str.set("y max = " + str(win_bound["ymax"]))
	
	theta_min_str = tk.StringVar()
	theta_min_str.set("theta min = " + str(win_bound["theta_min"]))
	
	theta_max_str = tk.StringVar()
	theta_max_str.set("theta max = " + str(win_bound["theta_max"]))

	x_min_disp = tk.Message(root, textvariable = x_min_str,
	width = 100)
	x_max_disp = tk.Message(root, textvariable = x_max_str,
	width = 100)
	y_min_disp = tk.Message(root, textvariable = y_min_str,
	width = 100)
	y_max_disp = tk.Message(root, textvariable = y_max_str,
	width = 100)
	theta_min_disp = tk.Message(root, textvariable = theta_min_str,
	width = 100)
	theta_max_disp = tk.Message(root, textvariable = theta_max_str,
	width = 100)

	x_min_disp.grid(row = 0, column = 0)
	x_max_disp.grid(row = 1, column = 0)
	y_min_disp.grid(row = 2, column = 0)
	y_max_disp.grid(row = 3, column = 0)
	theta_min_disp.grid(row = 4, column = 0)
	theta_max_disp.grid(row = 5, column = 0)

	x_min_entry.grid(row = 0, column = 1)
	x_max_entry.grid(row = 1, column = 1)
	y_min_entry.grid(row = 2, column = 1)
	y_max_entry.grid(row = 3, column = 1)
	theta_min_entry.grid(row = 4, column = 1)
	theta_max_entry.grid(row = 5, column = 1)

	root.bind("<Return>", lambda a: change_graph_win_set())

	root.mainloop()


def tkask(s = None):
	"""Make a GUI for the program."""

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

	root.mainloop()


# default startup
if len(sys.argv) == 1:
	if "tkinter" in sys.modules and use_gui:
		tkask()
	else:
		while True:
			ask()

else:  # handling command line arguments and startup
	history.append(" ".join(sys.argv[1:]))

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
