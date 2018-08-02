#   matrix_prototype.py

import tkinter as tk
import numpy as np

class Matrix(object):

	def __init__(self):
		'''Create a matrix window.'''
		
		self.root = tk.Toplevel()
		
		display_text = tk.StringVar()
		display_text.set("Matrix A")
		
		display = tk.Message(self.root, textvariable=display_text)
		display.grid(row=0, column=0)
		
		by_mess = tk.Message(self.root, text="by")
		by_mess.grid(row=0, column=2)
		
		self.xvar = tk.StringVar()
		self.yvar = tk.StringVar()
		
		self.xdim = tk.Entry(self.root, textvariable=self.xvar)
		self.xdim.grid(row=0, column=1)
		
		self.ydim = tk.Entry(self.root, textvariable=self.yvar)
		self.ydim.grid(row=0, column=3)
		
		self.go_button = tk.Button(self.root, text="enter", command=self.get_matrix)
		self.go_button.grid(row=0, column=4)
		
		self.xdim.insert(tk.END, "1")
		self.ydim.insert(tk.END, "4")
		
		self.minputs = None
		
		self.resize()
		
		self.xvar.trace("w", self.resize)
		self.yvar.trace("w", self.resize)
		
		self.root.mainloop()

	def resize(self, *args):
		
		if self.minputs is None:
			self.minputs = []
			row = []
			self.x = int(self.xdim.get())
			self.y = int(self.ydim.get())
			for i in range(self.y):
				for k in range(self.x):
					row.append(tk.Entry(self.root))
					row[-1].grid(row=i + 1, column=k)
				self.minputs.append(row)
				row = []
			self.minputs = np.array(self.minputs)
		else:
			newx = self.xdim.get()
			newy = self.ydim.get()
			if "" in (newx, newy):
				return
			
			newx, newy = int(newx), int(newy)
			
			if newx <= self.x:
				for i in range(self.x - newx):
					for d in self.minputs[:, newx - 0]:
						d.grid_forget()
						d.destroy()
					self.minputs = np.delete(self.minputs, newx - 0, 1)
				self.x = newx
			else:
				for i in range(self.x, newx):
					column = []
					for k in range(self.y):
						column.append(tk.Entry(self.root))
						column[-1].grid(row=k + 1, column=i)
					self.minputs = np.append(
						self.minputs,
						np.array(column).reshape(self.y, 1),
						axis=1)
				
				self.x = newx
				
				
			if newy <= self.y:
				for i in range(self.y - newy):
					for d in self.minputs[newy, :]:
						d.grid_forget()
						d.destroy()
					self.minputs = np.delete(self.minputs, newy, 0)
				self.y = newy
			else:
				for k in range(self.y, newy):
					row = []
					print(self.x)
					for i in range(self.x):
						row.append(tk.Entry(self.root))
						row[-1].grid(row=k + 1, column=i)
					self.minputs = np.append(
						self.minputs,
						np.array(row).reshape(1, self.x),
						axis=0)
				
				self.y = newy
			
	
	def get_matrix(self):
		self.matrix = np.matrix(np.vectorize(lambda a: int(a.get()))(self.minputs.copy()))
		print(self.matrix)


if __name__ == "__main__":
	x = Matrix()

