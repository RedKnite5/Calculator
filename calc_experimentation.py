# calc_experimentation.py


	# intentianly not using compile_ignore_case so that you can
	# differentiate between capital and lowercase units
	conv_comp = re.compile(
		"[Cc][Oo][Nn][Vv][Ee][Rr][Tt] (.+?)(?="
		+ "|".join(units) + ")(?:" + "|".join(units) + ")[Tt][Oo] ("
		+ "|".join(units) + ")"),
