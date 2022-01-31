from alignment import Alignment
import numpy

numpy.random.seed(123)

# Initialize the alignments (1x1 grid)

figwidth = 7
alignments = {
	'a': Alignment(1, 6),
	'b': Alignment(2, 3),	
	'c': Alignment(1, 6),	 	
	'd': Alignment(1, 1), 	
	'e': Alignment(2, 2),	
	'f': Alignment(2, 2),
}


# Configure spacings
small = 0.025
large = 0.2
for key, alignment in alignments.items():
	# Default
	for a in alignment.flatten():
		a.set_spacing(every=small)
	for a in alignment.left():
		a.set_left(large)
	for a in alignment.right():
		a.set_right(small)
	for a in alignment.top():
		a.set_top(large)
	for a in alignment.bottom():
		a.set_bottom(small)

# Panels a), b), c)
for key, aspect in zip(['a', 'b', 'c'], [1/1, 4/3, 1/1]):
	alignment = alignments.get(key)
	ncols = alignment.ncols()
	space, _ = alignment.figure_size()
	width = (figwidth - space)/ncols
	for a in alignment.flatten():
		a.set_aspect(aspect)
		a.set_width(width)	

# Use same size for f) and c)
alignment = alignments.get('f')
for a in alignment.flatten():
	a.set_aspect(1/1)
	a.set_width(width)

# Use same height for e) and f)
width_f, height = alignment.figure_size()
alignment = alignments.get('e')
_, space = alignment.figure_size()
height = (height - space)/alignment.ncols()
for a in alignment.flatten():
	a.set_aspect(4/3)
	a.set_height(height)

# Use remaining width and height for d)
width_e, height = alignment.figure_size()
width = figwidth - width_e - width_f
for a in alignments.get('d').flatten():
	a.set_width(width - a.spacing_width())
	a.set_height(height - a.spacing_height())

# Plot some data.
colors = {
	'a': "#f44336",
	'b': "#9c27b0",
	'c': "#3f51b5",
	'd': "#03a9f4",
	'e': "#009688",
	'f': "#8bc34a",
}
for (key, alignment), color in zip(alignments.items(), colors):
	for i, a in enumerate(alignment.flatten()):
		ax = a.matplotlib()
		n = 10
		ax.plot(
			numpy.linspace(0, 10, num=n), 
			numpy.random.randn(n),
			color=colors.get(key),
		)

		ax.set_xticks([])
		ax.set_yticks([])		

		if i == 0:
			ax.text(
				0.0, 
				1.0, 
				f'{key})', 
				ha='right', 
				va='bottom', 
				transform=ax.transAxes,
				weight='semibold'
			)

	fig = alignment.figure()
	fig.savefig(f'examples/example_3{key}.png', dpi=100)