# -*- coding: utf-8 -*-

'''
Classes and functions for ReCalc
'''

import re
from decimal import Context

# import tkinter if installed
try:
	import tkinter as tk
	from tkinter import filedialog
	from _tkinter import TclError
	from PIL import ImageTk
except ModuleNotFoundError:
	pass


__all__ = ["Unit", "compile_ignore_case", "CalculatorError",
	"NonRepeatingList", "Graph", "check_if_ascii", "float_to_str",
	]

def double_list(l):
	return([i for s in ((i, i) for i in l) for i in s])

def flatten(l):
	return((i for s in l for i in s))

ctx = Context()
ctx.prec = 17

def compile_ignore_case(pattern):
	'''
	Call re.compile with the IGNORECASE flag.
	'''

	return(re.compile(pattern, flags = re.I))


def check_if_ascii(s):
	try:
		s.encode("ascii")
		return(True)
	except UnicodeEncodeError:
		return(False)


def float_to_str(f):
	'''
	Convert the given float to a string,
	without resorting to scientific notation.

	>>> float_to_str(3.0030)
	'3.003'
	'''

	d1 = ctx.create_decimal(repr(float(f)))
	string = format(d1, "f")
	if string[-2:] == ".0":
		return string[:-2]
	return string


class CalculatorError(Exception):
	pass


class Unit(object):
	'''
	A class that represents different quantities
	'''

	base_units = ("meters", "m", "kilograms", "kg", "seconds", "s")

	distance_units = (
		"kilometers", "km",
		"centimeters", "cm",
		"millimeters", "mm",
		"inches", "in",
		"feet", "ft",
		"yards", "yd",
		"miles", "mi",
		"mils", "mil",
		"rods", "poles",
		"nautical miles", "nmi",
	)
	mass_units = (
		"grams", "g",
		"pounds", "lbs",
		"milligrams", "mg",
		"ounces", "oz",
		"tons", "tons",
		"micrograms", "µg",
		"tonnes", "t",
	)
	time_units = (
		"minutes", "min",
		"hours", "hr",
		"days", "d",
		"weeks", "wk",
		"years", "yr",
		"millisecond", "ms",
		"nanosecond", "ns",
	)

	multipliers_distance = (
		0.001, 100, 1000, 39.370078740157, 3.2808398950131,
		1.0936132983377, 0.00062137119223733, .039370078740157,
		5.029, 0.000539957,
	)
	multipliers_mass = (
		1000, 2.2046226218, 1000000, 35.274, 0.00110231, 1000000000000,
		0.001,
	)
	multipliers_time = (
		1 / 60, 1 / 3600, 1 / 86400, 1 / 604800, 1 / 31557600,
		1000, 1000000000,
	)

	nonbase_units = {
		"distance": distance_units,
		"time": time_units,
		"mass": mass_units
	}
	multipliers = {
		"distance": multipliers_distance,
		"time": multipliers_time,
		"mass": multipliers_mass,
	}

	for i in multipliers:
		multipliers[i] = double_list(multipliers[i])

	from_base_funcs = {unit: lambda a: a for unit in base_units}
	for unit, mult in zip(
		flatten(nonbase_units.values()),
		flatten(multipliers.values())):

		from_base_funcs.update({unit: lambda a, c = mult: a * c})

	to_base_funcs = {}
	for unit, mult in zip(
		flatten(nonbase_units.values()),
		flatten(multipliers.values())):

		to_base_funcs.update({unit: lambda a, c = mult: a / c})

	def __init__(self, amount, type):
		self.type = type
		self.amount = float(amount)

	def __repr__(self):
		return("Unit({a} {u})".format(a = self.amount, u = self.type))

	def __str__(self):
		return("{a} {u}".format(a = self.amount, u = self.type))

	def convert_to(self, new):
		'''
		Change what unit the quantity is expressed as.
		'''

		if self.type in Unit.base_units:
			new_amount = Unit.from_base_funcs[new](self.amount)
		elif new in Unit.base_units:
			new_amount = Unit.to_base_funcs[self.type](self.amount)
		else:
			new_amount = Unit.from_base_funcs[new](
				Unit.to_base_funcs[self.type](self.amount))

		return(Unit(new_amount, new))

	def convert_inplace(self, new):
		q = self.convert_to(new)
		self.amount = q.amount
		self.type = q.type

	def __floor__(self):
		return(Unit(floor(self.amount), self.type))

	def __ceil__(self):
		return(Unit(ceil(self.amount), self.type))

	def __trunc__(self):
		return(trunc(self.amount))

	def __add__(self, other):
		if isinstance(other, Unit):
			q = other.convert_to(self.type)
			q.amount += self.amount
			return(q)
		return(Unit(self.amount + other, self.type))

	def __sub__(self, other):
		if isinstance(other, Unit):
			q = other.convert_to(self.type)
			q.amount = self.amount - q.amount
			return(q)
		return(Unit(self.amount - other, self.type))

	def __radd__(self, other):
		return(other - self.amount)

	def __rsub__(self, other):
		return(other - self.amount)

	def __float__(self):
		return(float(self.amount))

	def __neg__(self):
		return(Unit(-self.amount, self.type))

	def __pos__(self):
		return(Unit(self.amount, self.type))

	def __abs__(self):
		return(Unit(abs(self.amount), self.type))

	def __round__(self, ndigits = None):
		return(Unit(round(self.amount, ndigits), self.type))


class NonRepeatingList(object):
	'''
	A mutable list that doesn't have two of the same element in a row.

	>>> repr(NonRepeatingList(3, 3, 4))
	'NonRepeatingList(3, 4)'
	'''

	def __init__(self, *args):
		if len(args) > 0:
			self.items = [args[0]]
			for i in args:
				if i != self.items[-1]:
					self.items.append(i)
		else:
			self.items = []

	def __getitem__(self, index):
		return(self.items[index])

	def __delitem__(self, index):
		'''
		Delete the item in the given index. If that puts two equal
		items adjacent delete the for recent one.
		'''

		del self.items[index]
		if index != 0:
			if self.items[index] == self.items[index - 1]:
				del self.items[index]

	def __contains__(self, item):
		'''
		Check if an item is in the NonRepeatingList.
		'''

		return(item in self.items)

	def __len__(self):
		return(len(self.items))

	def __repr__(self):
		return("NonRepeatingList(" + repr(self.items)[1:-1] + ")")

	def __str__(self):
		return(str(self.items))

	def __eq__(self, other):
		if isinstance(other, NonRepeatingList):
			if self.items == other.items:
				return(True)
		return(False)

	def append(self, *args):
		'''
		Add all arguments to the list if one is not the equal to the
		previous item.
		'''

		for item in args:
			if len(self.items) > 0:
				if self.items[-1] != item:
					self.items.append(item)
			else:
				self.items.append(item)

	def clear(self):
		'''
		Delete all items in the list.
		'''

		self.items.clear()


class Graph(object):
	'''
	Base class for all graphs.
	'''

	color_dict = {
		"black": (0, 0, 0),
		"red": (255, 0, 0),
		"green": (0, 128, 0),
		"blue": (0, 0, 255),
		"orange": (255, 165, 0),
		"purple": (128, 0, 128),
		"magenta": (255, 0, 255),
	}

	def __init__(
		self,
		xmin = -5, xmax = 5, ymin = -5, ymax = 5,
		wide = 400, high = 400):
		'''
		Initialize the graphing window.
		'''

		self.root = tk.Toplevel()

		self.root.title("ReCalc")

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

		# create the canvas
		self.screen = tk.Canvas(
			self.root,
			width = self.wide, height = self.high)
		self.screen.pack()

		self.options = tk.Menu(self.root)
		self.file_options = tk.Menu(self.options, tearoff = 0)

		self.file_options.add_command(
			label = "Save",
			command = self.save_image)
		self.file_options.add_command(
			label = "Exit",
			command = self.root.destroy)

		self.options.add_cascade(
			label = "File",
			menu = self.file_options)

		self.root.config(menu = self.options)

	def axes(self):
		'''
		Draw the axis.
		'''

		# adjusted y coordinate of x-axis
		b = self.high + (self.ymin * self.high / self.yrang)

		# adjusted x coordinate of y-axis
		a = -1 * self.xmin * self.wide / self.xrang

		try:
			# draw x-axis
			self.screen.create_line(0, b, self.wide, b, fill = "gray")

			# draw y-axis
			self.screen.create_line(a, self.high, a, 0, fill = "gray")

			self.root.update()
		except TclError as e:
			pass

	def save_image(self):
		'''
		Save the image to a file.
		'''

		fout = filedialog.asksaveasfile()
		self.image.save(fout)
		print("Saved")
