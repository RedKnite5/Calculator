#   matrix_prototype.py
#import tkinter as tk

'''
def matrix():
	"""Create a matrix window."""
	
	root = tk.Toplevel()
	
	display_text = tk.StringVar()
	display_text.set("Matrix A")
	
	display = tk.Message(root,textvariable=display_text)
	display.grid(row=0, column=0)
	
	by_mess = tk.Message(root,text="by")
	by_mess.grid(row=0, column=2)
	
	xdim = tk.Entry(root)
	xdim.grid(row=0, column=1)
	
	ydim = tk.Entry(root)
	ydim.grid(row=0, column=3)
	
	
	
	root.mainloop()

x = matrix()
'''

def brackets(s):
	'''Inform separate whether parentheses match.'''

	x = 0
	for i in s:
		if i == "(":
			x += 1
		elif i == ")":
			x -= 1
		if x < 0:
			return(False)
	return(not not x)


def separate(s):
	'''Split up arguments of a function with commas
	like mod(x, y) or log(x, y) based on where commas that are only
	in one set of parentheses.
	'''

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

		# if its not in the middle add the current term to final list
		if x:
			new_terms.append(terms[i])
			continue

		# if it is in the middle of a group
		if x:

			# add the current term to the string of previous terms
			next_term = next_term + "," + terms[i + 1]

			# check if that was the end of the group
			if not brackets(next_term):
				new_terms.append(next_term)
				middle = False
			else:
				middle = True

	return(new_terms)
	








