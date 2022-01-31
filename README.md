# exact-size-matplotlib

Provides a helper Alignment class to display complex [matplotlib](https://matplotlib.org/) plots with defined sizes in inches.
Alignment is based on a grid, where spacings (left, right, top, bottom), and size (width, height) are determined in inches for each axes. 

# Getting started

## Example 1

The simplest example is a single axes with defined spacing and size in inches. In this case, `alignment.flatten()` only converts the grid to a 1D list allowing us to iterate through all the axes. The same result could be obtained by specifying `a = alignment[0][0]`. This figure has a size of 3x3", or 300x300 px when rendered at 100 dpi.

```python
from alignment import Alignment

# Initialize the alignment.
nrows, ncols = 1, 1
alignment = Alignment(nrows, ncols)

# Configure axes spacing.
for a in alignment.flatten():
	a.set_spacing(
		left=0.5, 
		right=1.0, 
		top=1.25, 
		bottom=0.5
	)

# Configure axes size.
for a in alignment.flatten():
	a.set_size(
		width=1.5, 
		height=1.25
	)

# Plot some data.
for a in alignment.flatten():
	ax = a.matplotlib()
	ax.plot(
		[1, 2, 3], 
		[0.5, 0.25, 0.125]
	)

# Save the figure.
fig = alignment.figure()
fig.savefig('examples/example_1.png', dpi=100)
```

![Example 1](https://github.com/rpylkkanen/exact-size-matplotlib/blob/main/examples/example_1.png) ![Example 2](https://github.com/rpylkkanen/exact-size-matplotlib/blob/main/examples/example_1_decorations.png)


## Example 2

A more practical example may be a figure where we want to specify exact output size, and control only spacings. An example is illustrated below for code that generates a 3x3 grid with 0.05" spacing on each side of each axes. The resulting figure has a size of 3x3" or 300x300 px when saved at 100 dpi. 

```python
from alignment import Alignment
import numpy
import random

numpy.random.seed(123)

# Initialize the alignment.
nrows, ncols = 3, 3
alignment = Alignment(nrows, ncols)

# Configure axes spacing.
for a in alignment.flatten():
	a.set_spacing(every=0.05)

# Specify figure size.
figure_width, figure_height = 3, 3

# Calculate size consumed by spacing (figure contains only spacing).
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
for a in alignment.flatten():
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
	ax.set_ylim(-15, 15)

# Save the figure.
fig = alignment.figure()
fig.savefig('examples/example_2.png', dpi=100)
```

![Example 2](https://github.com/rpylkkanen/exact-size-matplotlib/blob/main/examples/example_2.png)


## Example 3

A more complex multi-panel example may be closer to a real-life situation, where the whole figure can have a maximum width of 5".

![Example 3](https://github.com/rpylkkanen/exact-size-matplotlib/blob/main/examples/example_3.png)

The easiest way to obtain this result is to treat each panel as its own alignment object, save the figures separately and combine them later for the final figure. This is relatively easy if you have control over all dimensions of the resulting panels. Below is the basic configuration, note we can use for example `alignment.left()` to adjust only the spacings of the leftmost axes. Using `if key == 'f'` we are able to easily reserve extra space for text in panel f).

```python
from alignment import Alignment
import numpy

numpy.random.seed(123)

# Initialize the alignments

figwidth = 5
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
text = 0.20
large = 0.20
for key, alignment in alignments.items():
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
	if key in 'f':
		a.set_top(text)
```

Below is the logic for calculating axes widths/heights. For a)-c), we want the figures to consume all available space. Height in this case will be determined by specifying aspect ratio, but alternatively we could set it manually. For f), we use same size as for c), but e) has different aspect ratio than f). Finally, d) will consume remaining space.

```python
# Panels a), b), c)
for key, aspect in zip('abc', [1/1, 4/3, 1/1]):
	alignment = alignments.get(key)
	# Alignment contains only spacing at this point.
	space, _ = alignment.figure_size()
	width = (figwidth - space)/alignment.ncols()
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
```

Now, the only thing left to do is plot some data and save the panels. The code for combining them using PIL is given in merge_example_3.py.

```python
for key, alignment in alignments.items():
			
	# Plot some data.
	for i, a in enumerate(alignment.flatten()):
		ax = a.matplotlib()
		n = 100
		x = numpy.linspace(0, n, num=n)
		y = numpy.random.randn(n)
		ax.plot(
			x, 
			y,
			color=colors[key],
		)
		ax.set_xticks([])
		ax.set_yticks([])
		ax.set_ylim(-15, 15)

		# Annotation
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

		if key == 'f':
			ax.set_title(f'text {i}', fontsize='small')

	fig = alignment.figure()
	fig.savefig(f'examples/example_3{key}.png', dpi=100)
```

