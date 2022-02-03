from matplotlib_exact import Alignment


for i, (nrows, ncols) in enumerate(zip([1, 2, 3], [3, 2, 1])):
	
	ali = Alignment(nrows, ncols)
	
	for a in ali.flatten():
		a.set_spacing(every=0.05)
		a.set_left(0.1)
		a.set_right(0.15)
	
	for a in ali.flatten():
		a.set_height(1.0)
		a.set_width(0.5)

	for a in ali.flatten():
		ax = a.matplotlib()
		ax.set_xticks([])
		ax.set_yticks([])
		a.annotate_rect(center=True, every=False)
		a.annotate_text(center=True, every=False)

	fig = ali.figure()
	fig.savefig(f'test_{i:03}.png', dpi=300)
	