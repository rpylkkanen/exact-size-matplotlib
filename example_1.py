from alignment import Alignment

# Initialize the alignment (1x1 grid)
nrows, ncols = 1, 1
alignment = Alignment(nrows, ncols)

# Configure spacing (in inches).
a = alignment[0][0] # Custom Axes-object, we only have one.
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