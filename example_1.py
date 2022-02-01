from matplotlib_exact import Alignment

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