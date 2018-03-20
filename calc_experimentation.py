# calc_experimentation.py



def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def check_if_float(x):
	'''
	Test if a object can be made a float.

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


def check_if_words(text):
	try:
		text2int(text)
		return(True)
	except:
		return(False)


class Number(object):
	'''
	A class that stores exact values of numbers.
	'''

	def __init__(self, num):
		if isinstance(num, str):
			if num.isdigit():
				self.num = int(num)
				self.mode = "int"
			elif check_if_float(num):
				self.num = float(num).as_integer_ratio()
				self.mode = "frac"
			elif check_if_words(num):
				self.num = text2int(num)
				self.mode = "int"
				
			





print(string)


