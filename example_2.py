from alignment import Alignment
import numpy

numpy.random.seed(123)

# Initialize the alignment (1x1 grid)
nrows, ncols = 3, 3
alignment = Alignment(nrows, ncols)

# Configure spacing (in inches).
for a in alignment.flatten():
	a.set_spacing(every=0.05)
	a.set_size(width=1.0, height=1.0)

# Initialize the matplotlib Axes-object and plot data.
for a in alignment.flatten():
	ax = a.matplotlib()
	n = 10
	ax.plot(numpy.linspace(0, 10, num=n), numpy.random.randn(n))
	ax.set_xticks([])
	ax.set_xticks([])

fig = alignment.figure()
fig.savefig('examples/example_2.png', dpi=100)