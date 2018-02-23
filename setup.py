#   setup.py

from setuptools import setup, find_packages
setup(
    name = "Calculator",
    version = "0.1",
    packages = find_packages(),
	scripts = ["re_calc.py"],
	
	install_requires = ["sympy>=1.1.1", "tkinter>=8.6"]
	
	package_data = {
	"": ["*.ico", "*.txt", "*.py"]
	},
	
	author = "Max Friedman",
	author_email = "mr.awesome10000@gmail.com",
	desciption = "This is a basic graphing calculator.",
	licencse = "GNU"
	
)





