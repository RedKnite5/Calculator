# calc_experimentation.py


class Unit(object):
	'''
	A class that represents different units
	'''

	base_units = ("meters", "m", "kilograms", "kg", "seconds", "s")
	
	distance_units = (
		"kilometers", "km",
		"centimeters", "cm",
		"milimeters", "mm",
		"inches", "in",
		"feet", "ft",
		"yards", "yd",
		"miles", "mi",)
	mass_units = (
		"grams", "g",
		"pounds", "lbs",
	)
	time_units = (
		"minutes", "min",
		"hours", "h",
	)

	multipliers_distance = (
		0.001, 100, 1000, 39.370078740157, 3.2808398950131,
		1.0936132983377, 0.00062137119223733,
	)
	multipliers_mass = (
		0.001, 2.2046226218,
	)
	multipliers_time = (
		1/60, 1/3600, 
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

	def double_list(l):
		return([i for s in ((i, i) for i in l) for i in s])

	def flatten(l):
		return((i for s in l for i in s))

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

	del double_list
	del flatten

	def __init__(self, amount, type):
		self.type = type
		self.amount = amount

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


	


a = Unit(4, "meters")
print(a + 4)
a += 2
a -= 3
print(a)
print(5 - a)
a.convert_inplace("cm")
print(a)
b = Unit(1500, "mm")
print(a + b)
print(a - b)
print(a * 2)
