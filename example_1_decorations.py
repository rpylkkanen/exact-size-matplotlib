from alignment import Alignment
import matplotlib
import numpy

# Example 2

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
ax.set_xticks([])
ax.set_yticks([])

# Text
text = f'width={width:.2f}"\nheight={height:.2f}"'
ax.text(
	0.5, 
	0.5, 
	text,
	ha='center',
	va='center',
	transform=ax.transAxes
)

ls = '--'

# Left line
x = [0.0, a.left()/figure_width]
y = [0.5, 0.5]
line = matplotlib.lines.Line2D(x, y, ls=ls, transform=fig.transFigure)
fig.lines.append(line)

# Left text
ax.text(
	numpy.average(x), 
	numpy.average(y), 
	f'{a.left():.2f}"', 
	ha='center', 
	va='bottom', 
	transform=fig.transFigure
)

# Right line
x = [(a.left() + a.width())/figure_width, 1.0]
y = [0.5, 0.5]
line = matplotlib.lines.Line2D(x, y, ls=l, transform=fig.transFigure)
fig.lines.append(line)

# Right text
ax.text(
	numpy.average(x), 
	numpy.average(y), 
	f'{a.right():.2f}"', 
	ha='center', 
	va='bottom', 
	transform=fig.transFigure
)

# Top line
x = [0.5, 0.5]
y = [1.0, (figure_height - a.top())/figure_height]
line = matplotlib.lines.Line2D(x, y, ls=ls, transform=fig.transFigure)
fig.lines.append(line)

# Top text
ax.text(
	numpy.average(x), 
	numpy.average(y), 
	f'{a.top():.2f}"', 
	ha='right', 
	va='center',
	rotation=90, 
	transform=fig.transFigure
)

# Bottom line
x = [0.5, 0.5]
y = [(figure_height - a.top() - a.height())/figure_height, 0.0]
line = matplotlib.lines.Line2D(x, y, ls=ls, transform=fig.transFigure)
fig.lines.append(line)

# Bottom text
ax.text(
	numpy.average(x), 
	numpy.average(y), 
	f'{a.bottom():.2f}"', 
	ha='right', 
	va='center',
	rotation=90, 
	transform=fig.transFigure
)

fig.savefig('examples/example_1_decorations.png', dpi=100)