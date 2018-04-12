# calc_experimentation.py

def double_list(l):
	return([i for s in ((i, i) for i in l) for i in s])
def flatten(l):
	return((i for s in l for i in s))

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

	for i in multipliers:
		multipliers[i] = double_list(multipliers[i])

	from_base_funcs = {unit: lambda a: a for unit in base_units}
	for unit, mult in zip(flatten(nonbase_units.values()), flatten(multipliers.values())):
		from_base_funcs.update({unit: lambda a, c = mult: a * c})
	
	to_base_funcs = {}
	for unit, mult in zip(flatten(nonbase_units.values()), flatten(multipliers.values())):
		to_base_funcs.update({unit: lambda a, c = mult: a / c})

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
			self.amount = Unit.from_base_funcs[new](self.amount)
		elif new in Unit.base_units:
			self.amount = Unit.to_base_funcs[self.type](self.amount)
		else:
			self.amount = Unit.from_base_funcs[new](Unit.to_base_funcs[self.type](self.amount))

		self.type = new
		return(self)


a = Unit(4, "feet")
print(a.convert_to("inches"))
