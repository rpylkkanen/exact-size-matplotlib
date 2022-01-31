from alignment import Alignment
import numpy
import random

# Initialize the alignment.
nrows, ncols = 3, 3
alignment = Alignment(nrows, ncols)

# Configure axes spacing.
for a in alignment.flatten():
	a.set_spacing(every=0.05)

# Specify figure size.
figure_width, figure_height = 3, 3

# Calculate size consumed by spacing (figure doesnt containe else).
spacing_width, spacing_height = alignment.figure_size()

# Calculate available space for each axes.
ncols = alignment.ncols()
nrows = alignment.nrows()
axes_width = (figure_width - spacing_width)/ncols
axes_height = (figure_height - spacing_height)/nrows

# Configure axes sizes.
for a in alignment.flatten():
	a.set_size(width=axes_width, height=axes_height)

# Plot some data.
for i, a in enumerate(alignment.flatten()):
	ax = a.matplotlib()
	n = 100
	x = numpy.linspace(0, n, num=n)
	y = numpy.random.randn(n)
	color = "#%06x" % random.randint(0, 0xFFFFFF)
	ax.plot(
		x, 
		y,
		color=color
	)
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_ylim(-nrows*ncols, nrows*ncols)

# Save figure.
fig = alignment.figure()
fig.savefig('examples/example_2.png', dpi=100)