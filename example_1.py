from alignment import Alignment
import matplotlib
import numpy

# Example 1

nrows, ncols = 1, 1
alignment = Alignment(nrows, ncols)

fig = alignment.figure()
axes = alignment.flatten()
a = axes[0]

# Spacing
left, right, top, bottom = 0.5, 1.0, 1.25, 0.5
a.set_spacing(
	left=left, 
	right=right,
	top=top, 
	bottom=bottom
)

# Axis width
figure_width, figure_height = 3.0, 3.0
width = figure_width - a.spacing_width()
height = figure_height - a.spacing_height()
a.set_size(width=width, height=height)

# Plotting
ax = a.matplotlib()
ax.plot([1, 2, 3], [0.5, 0.25, 0.125])

fig.savefig('examples/example_1.png', dpi=100)