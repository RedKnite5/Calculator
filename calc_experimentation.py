# calc_experimentation.py
import re

units = ("meters", "kilometers")

# intentianly not using compile_ignore_case so that you can
# differentiate between capital and lowercase units
conv_comp = re.compile(
	"[Cc][Oo][Nn][Vv][Ee][Rr][Tt] (.+?)(?="
	+ "|".join(units) + ")(" + "|".join(units) + ") ?[Tt][Oo] ("
	+ "|".join(units) + ")")
m = re.search(conv_comp, "convert 4 meters to kilometers")
print(m.groups())
