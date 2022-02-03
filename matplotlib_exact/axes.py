import numpy
from mpl_toolkits.axes_grid1 import Divider, Size
from matplotlib.patches import Rectangle
from .spacing import Spacing

class Axes:

	def __init__(self, alignment=None, width=None, height=None, aspect=None):

		self.set_alignment(alignment or Alignment(1, 1))
		self.set_aspect(aspect or None)
		self.set_width(width or 0.0)
		self.set_height(height or 0.0)
		self._spacing = Spacing(0.0, 0.0, 0.0, 0.0)
		self._matplotlib = None

	def set_alignment(self, alignment):
		self._alignment = alignment

	def alignment(self):
		return self._alignment

	def index(self):
		index = numpy.where(self.alignment().array() == self)
		return index

	def set_aspect(self, aspect):
		self._aspect = aspect

	def aspect(self):
		return self._aspect

	def set_width(self, width):
		self._width = width
		if self.aspect():
			self._height = width / self.aspect()

	def width(self):
		return self._width

	def total_width(self):
		return self.left() + self.width() + self.right()

	def set_height(self, height):
		self._height = height
		if self.aspect():
			self._width = height * self.aspect()

	def height(self):
		return self._height

	def spacing_width(self):
		return self.left() + self.right()

	def spacing_height(self):
		return self.top() + self.bottom()

	def total_height(self):
		return self.top() + self.height() + self.bottom()

	def set_size(self, width=None, height=None):
		if width:
			self.set_width(width)
		if height:
			self.set_height(height)

	def total_size(self):
		return (self.total_width(), self.total_height())

	def set_spacing(self, left=None, right=None, top=None, bottom=None, every=None):
		if every:
			self._spacing = Spacing(every, every, every, every)
		if left:
			self.set_left(left)
		if right:
			self.set_right(right)
		if top:
			self.set_top(top)
		if bottom:
			self.set_bottom(bottom)

	def spacing(self):
		return self._spacing

	def set_left(self, left):
		self.spacing().set_left(left)

	def left(self):
		return self.spacing().left()

	def set_right(self, right):
		self.spacing().set_right(right)

	def right(self):
		return self.spacing().right()

	def set_bottom(self, bottom):
		self.spacing().set_bottom(bottom)

	def bottom(self):
		return self.spacing().bottom()

	def set_top(self, top):
		self.spacing().set_top(top)

	def top(self):
		return self.spacing().top()

	def matplotlib(self):
		if self._matplotlib == None:
			if self.width() and self.height():
				self._matplotlib = self._convert_to_matplotlib()
		return self._matplotlib

	def _convert_to_matplotlib(self):

		# Verify figure size.
		a = self.alignment()
		a_size = a.figure_size()
		f = a.figure()
		f_size = f.get_size_inches()
		f_size = (f_size[0], f_size[1])
		if f_size != a_size:
			f.set_size_inches(a_size)

		# Index.
		index = self.index()
		row = int(index[0])
		col = int(index[1])

		# Calculate left.
		left = 0.0
		for c in a.array()[row][:col]:
			left += c.total_width()
		left += self.left()
		width = self.width()

		# Calculate bottom.
		bottom = 0.0
		for r in a.array()[row + 1:][::1]:
			row_h = 0.0
			for c in r:
				h = c.total_height()
				if h > row_h: 
					row_h = h
			bottom += row_h
		bottom += self.bottom()
		height = self.height()
		
		h = [Size.Fixed(left), Size.Fixed(width)]
		v = [Size.Fixed(bottom), Size.Fixed(height)]
		divider = Divider(f, (0, 0, 1, 1), h, v, aspect=False)
		ax = f.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))

		return ax

	def annotate_text(self, center=False, left=False, right=False, top=False, bottom=False, every=False, fontsize='xx-small'):

		ax = self.matplotlib()

		if ax:

			if center or every:
				ax.text(
					0.5,
					0.5,
					f'w: {self.width():.3f}"\nh: {self.height():.3f}"',
					ha = 'center',
					va = 'center',
					fontsize=fontsize,
				)

			if left or every:
				width = self.left()/self.width()
				height = self.height()/self.height()
				x = 0.0 - width
				y = 0.0
				ax.text(
					0.0 - width/2,
					0.5,
					f'{self.left():.3f}"',
					ha = 'center',
					va = 'center',
					fontsize=fontsize,
					rotation=90
				)

			if right or every:
				width = self.right()/self.width()
				height = self.height()/self.height()
				x = 1.0
				y = 0.0
				ax.text(
					1.0 + width/2,
					0.5,
					f'{self.right():.3f}"',
					ha = 'center',
					va = 'center',
					fontsize=fontsize,
					rotation=90
				)

			if top or every:
				width = self.width()/self.width()
				height = self.top()/self.height()
				x = 0.0
				y = 1.0
				ax.text(
					0.5,
					1.0 + height/2,
					f'{self.top():.3f}"',
					ha = 'center',
					va = 'center',
					fontsize=fontsize
				)

			if bottom or every:
				width = self.width()/self.width()
				height = self.bottom()/self.height()
				x = 0.0
				y = 0.0 - height
				ax.text(
					0.5,
					0.0 - height/2,
					f'{self.bottom():.3f}"',
					ha = 'center',
					va = 'center',
					fontsize=fontsize
				)

	def annotate_rect(self, center=False, left=False, right=False, top=False, bottom=False, every=False):

		ax = self.matplotlib()

		if ax:

			if center or every:
				ax.axhline(sum(ax.get_ylim())/2, ls='-', alpha=0.5)
				ax.axvline(sum(ax.get_xlim())/2, ls='-', alpha=0.5)

			if left or every:
				width = self.left()/self.width()
				height = self.height()/self.height()
				x = 0.0 - width
				y = 0.0
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color='#F16A70',
					alpha=0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
				)
				ax.add_patch(rect)

			if right or every:
				width = self.right()/self.width()
				height = self.height()/self.height()
				x = 1.0
				y = 0.0
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color='#B1D877',
					alpha=0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
				)
				ax.add_patch(rect)

			if top or every:
				width = self.width()/self.width()
				height = self.top()/self.height()
				x = 0.0
				y = 1.0
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color='#8CDCDA',
					alpha=0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
				)
				ax.add_patch(rect)

			if bottom or every:
				width = self.width()/self.width()
				height = self.bottom()/self.height()
				x = 0.0
				y = 0.0 - height
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color='#4D4D4D',
					alpha=0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
				)
				ax.add_patch(rect)


	def __repr__(self):
		return f'Axes(width={self.width()}, height={self.height()}, aspect={self.aspect()}, spacing={self.spacing()}'