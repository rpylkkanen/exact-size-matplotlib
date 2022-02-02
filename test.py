from matplotlib_exact import Alignment

for nrows, ncols in zip([1, 2, 3], [3, 2, 1]):
	ali = Alignment(nrows, ncols)
	
	for a in ali.flatten():
		a.set_spacing(every=0.05)
		a.set_left(0.1)
		a.set_right(0.15)
	print(ali.figure_size(), ali.spacing_width(), ali.spacing_height())
	
	for a in ali.flatten():
		a.set_height(1.0)
		a.set_width(0.5)
	print(ali.figure_size(), ali.figure_width(), ali.figure_height())

	