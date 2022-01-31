# exact-size-matplotlib

Provides a helper Alignment class to display complex [matplotlib](https://matplotlib.org/) plots with defined sizes in inches. It is particularly useful for multi-panel figures for scientific publications, where figure specifications (for example maximum width) are given by the journal, and available space may be tight and exact alignment as opposed to relative (for example based on figure/axis fraction) are important.

Alignment is based on a grid, where spacings (left, right, top, bottom), and size (width, height) are determined in inches for each axis. 

# Getting started

## Example 1

The simplest example is a single axes with defined spacing and size in inches. 

In order to generate an image with specified dimensions, we can define the spacings and subtract them from the final figure size (3x3"). The resulting figure has a size of 300x300 px when saved at 100 dpi. The code to generate additional decorations is given in example_2.py. 

```python
from alignment import Alignment

# Initialize the alignment (1x1 grid)
nrows, ncols = 1, 1
alignment = Alignment(nrows, ncols)

# Configure spacing (in inches).
a = alignment[0][0] # Custom Axes-object, not to be confused with matplotlib.
a.set_spacing(left=0.5, right=1.0, top=1.25, bottom=0.5)

# Configure axis size (in inches, calculated from final figure size).
figure_width, figure_height = 3.0, 3.0
width = figure_width - a.spacing_width() 	# = 1.5
height = figure_height - a.spacing_height()	# = 1.25
a.set_size(width=width, height=height)

# Initialize the matplotlib Axes-object and plot data.
ax = a.matplotlib()
ax.plot([1, 2, 3], [0.5, 0.25, 0.125])

# Save the figure.
fig = alignment.figure()
fig.savefig('examples/example_1.png', dpi=100)
```

![Example 1](https://github.com/rpylkkanen/exact-size-matplotlib/blob/main/examples/example_1.png) ![Example 2](https://github.com/rpylkkanen/exact-size-matplotlib/blob/main/examples/example_1_decorations.png)


## Example 2

A more practical example may be a 3x3 grid, where each image is exactly 1x1" square with 0.05" spacing on every side. In this case the resulting figure has a width and height of 3 * 1" (for each axes) and 3 * 2 * 0.05" (for each spacing, on both sides of axes) for a total figure size of 3.3x3.3". The resulting figure has a size of 330x330 px when saved at 100 dpi.

```python
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
fig.savefig('examples/example_3.png', dpi=100)
```

![Example 3](https://github.com/rpylkkanen/exact-size-matplotlib/blob/main/examples/example_2.png)
