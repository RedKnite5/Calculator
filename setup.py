#   setup.py

from setuptools import setup, find_packages
setup(
    name = "Calculator",
    version = "0.1",
    packages = find_packages(),
	scripts = ["re_calc.py"],
	
	classifiers = [
	"Programming Language :: Python :: 3.6",
	"Environment :: X11 Applications :: Gnome",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	"Natural Language :: English",
	"Operating System :: Microsoft :: Windows :: Windows 10",
	"Operating System :: POSIX :: Linux".
	"Programming Language :: Python :: 3 :: Only",
	"Programming Language :: Python :: Implementation :: CPython",
	"Topic :: Scientific/Engineering :: Mathematics",
	]
	install_requires = ["sympy>=1.1.1", "tkinter>=8.6"]
	
	package_data = {
	"": ["*.ico", "*.txt", "*.py"]
	},
	
	url = "https://github.com/RedKnite5/Calculator.git"
	
	author = "Max Friedman",
	author_email = "mr.awesome10000@gmail.com",
	desciption = "This is a basic graphing calculator.",
	licencse = "GNU"
	
)





