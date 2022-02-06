import numpy
from mpl_toolkits.axes_grid1 import Divider, Size
from matplotlib.patches import Rectangle
from .spacing import Spacing
from matplotlib.lines import Line2D


class Axes:

	def __init__(self, alignment, width=None, height=None, aspect=None):

		self._alignment = alignment
		self._aspect = aspect or None
		self._width = width or 0.0
		self._height = height or 0.0
		self._spacing = Spacing(0.0, 0.0, 0.0, 0.0)
		self._matplotlib = None
		self.text_annotations = None
		self.rect_annotations = None
		self.line_annotations = None

	def set_alignment(self, alignment):
		self._alignment = alignment

	def alignment(self):
		return self._alignment

	def index(self):
		index = numpy.where(self.alignment().array() == self)
		return index

	def set_aspect(self, aspect):
		self._aspect = aspect
		self.alignment().update()

	def aspect(self):
		return self._aspect

	def set_width(self, width):
		self._width = width
		if self.aspect():
			self._height = width / self.aspect()
		self.alignment().update()

	def width(self):
		return self._width

	def total_width(self):
		return self.left() + self.width() + self.right()

	def set_height(self, height):
		self._height = height
		if self.aspect():
			self._width = height * self.aspect()
		self.alignment().update()

	def height(self):
		return self._height

	def spacing_width(self):
		return self.left() + self.right()

	def spacing_height(self):
		return self.top() + self.bottom()

	def total_height(self):
		return self.top() + self.height() + self.bottom()

	def set_size(self, width=None, height=None):
		if width is not None:
			self.set_width(width)
		if height is not None:
			self.set_height(height)

	def total_size(self):
		return self.total_width(), self.total_height()

	def set_spacing(self, left=None, right=None, top=None, bottom=None, every=None):
		if every is not None:
			self._spacing = Spacing(every, every, every, every)
		if left is not None:
			self.set_left(left)
		if right is not None:
			self.set_right(right)
		if top is not None:
			self.set_top(top)
		if bottom is not None:
			self.set_bottom(bottom)
		self.alignment().update()

	def spacing(self):
		return self._spacing

	def set_left(self, left):
		self.spacing().set_left(left)
		self.alignment().update()

	def left(self):
		return self.spacing().left()

	def set_right(self, right):
		self.spacing().set_right(right)
		self.alignment().update()

	def right(self):
		return self.spacing().right()

	def set_bottom(self, bottom):
		self.spacing().set_bottom(bottom)
		self.alignment().update()

	def bottom(self):
		return self.spacing().bottom()

	def set_top(self, top):
		self.spacing().set_top(top)
		self.alignment().update()

	def top(self):
		return self.spacing().top()

	def matplotlib(self):
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
			print(f'Resizing figure: ({a_size[0]:.2f}, {a_size[1]:.2f})')
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
		
		# Create ax. 
		if self._matplotlib is None:
			h = [Size.Fixed(left), Size.Fixed(width)]
			v = [Size.Fixed(bottom), Size.Fixed(height)]
			divider = Divider(f, (0, 0, 1, 1), h, v, aspect=False)
			ax = f.add_axes(
				divider.get_position(), 
				axes_locator=divider.new_locator(nx=1, ny=1)
			)
		else:
			ax = self._matplotlib
			h = [Size.Fixed(left), Size.Fixed(width)]
			v = [Size.Fixed(bottom), Size.Fixed(height)]
			divider = Divider(f, (0, 0, 1, 1), h, v, aspect=False)
			ax.set_position(divider.get_position())
			ax.set_axes_locator(divider.new_locator(nx=1, ny=1))

		if self.text_annotations:
			self.annotate_text()

		if self.rect_annotations:
			self.annotate_rect()

		return ax

	def annotate(self):
		self.annotate_text()
		self.annotate_rect()

	def annotate_text(self, center=False, left=False, right=False, top=False, bottom=False, fontsize='xx-small'):

		ax = self._matplotlib

		if ax is not None:

			if True in [left, right, top, bottom, center]:
				every = False
			else:
				every = True

			self.clear_text_annotations()

			texts = []

			if every or center:
				tc = ax.text(
					0.5,
					0.5,
					f'i: ({self.index()[0]}, {self.index()[1]})\nw: {self.width():.3f}"\nh: {self.height():.3f}"',
					ha='center',
					va='center',
					fontsize=fontsize,
					transform=ax.transAxes,
				)
				texts.append(tc)

			if (every or left) and self.width():
				width = self.left()/self.width()
				tl = ax.text(
					0.0 - width/2,
					0.5,
					f'{self.left():.3f}"',
					ha='center',
					va='center',
					fontsize=fontsize,
					rotation=90,
					transform=ax.transAxes,
				)
				texts.append(tl)

			if (every or right) and self.width():
				width = self.right()/self.width()
				tr = ax.text(
					1.0 + width/2,
					0.5,
					f'{self.right():.3f}"',
					ha='center',
					va='center',
					fontsize=fontsize,
					rotation=90,
					transform=ax.transAxes,
				)
				texts.append(tr)

			if (every or top) and self.height():
				height = self.top()/self.height()
				tt = ax.text(
					0.5,
					1.0 + height/2,
					f'{self.top():.3f}"',
					ha='center',
					va='center',
					fontsize=fontsize,
					transform=ax.transAxes,
				)
				texts.append(tt)

			if (every or bottom) and self.height():
				height = self.bottom()/self.height()
				tb = ax.text(
					0.5,
					0.0 - height/2,
					f'{self.bottom():.3f}"',
					ha='center',
					va='center',
					fontsize=fontsize,
					transform=ax.transAxes,
				)
				texts.append(tb)

			self.text_annotations = texts

	def clear_text_annotations(self):

		ax = self._matplotlib
		if ax and self.text_annotations:
			for text in self.text_annotations:
				if text in ax.texts:
					ax.texts.remove(text)
			self.text_annotations = None

	def clear_rect_annotations(self):

		ax = self._matplotlib
		if ax and self.rect_annotations:
			for patch in self.rect_annotations:
				if patch in ax.patches:
					ax.patches.remove(patch)
			self.rect_annotations = None

		if ax and self.line_annotations:
			for line in self.line_annotations:
				if line in ax._children:
					ax._children.remove(line)
			self.line_annotations = None

	def clear_annotations(self):
		self.clear_text_annotations()
		self.clear_rect_annotations()

	def annotate_rect(self, center=False, left=False, right=False, top=False, bottom=False, color=None, alpha=None):

		ax = self._matplotlib

		if ax is not None:

			if True in [left, right, top, bottom, center]:
				every = False
			else:
				every = True

			self.clear_rect_annotations()

			if every or center:
				lines = []
				line1 = ax.add_artist(Line2D(
					[0.5, 0.5],
					[0.0, 1.0],
					transform=ax.transAxes,
					color=color or None,
					alpha=alpha or 0.5,
				))
				lines.append(line1)
				line2 = ax.add_artist(Line2D(
					[0.0, 1.0],
					[0.5, 0.5],
					transform=ax.transAxes,
					color=color or None,
					alpha=alpha or 0.5)
				)
				lines.append(line2)
				self.line_annotations = lines

			patches = []

			if (every or left) and (self.width() and self.height()):
				width = self.left()/self.width()
				height = self.height()/self.height()
				x = 0.0 - width
				y = 0.0
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color=color or '#F16A70',
					alpha=alpha or 0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
					zorder=-5,
				)
				patch = ax.add_patch(rect)
				patches.append(patch)

			if (every or right) and (self.width() and self.height()):
				width = self.right()/self.width()
				height = self.height()/self.height()
				x = 1.0
				y = 0.0
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color=color or '#B1D877',
					alpha=alpha or 0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
					zorder=-5,
				)
				patch = ax.add_patch(rect)
				patches.append(patch)

			if (every or top) and (self.width() and self.height()):
				width = self.width()/self.width()
				height = self.top()/self.height()
				x = 0.0
				y = 1.0
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color=color or '#8CDCDA',
					alpha=alpha or 0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
					zorder=-5,
				)
				patch = ax.add_patch(rect)
				patches.append(patch)

			if (every or bottom) and (self.width() and self.height()):
				width = self.width()/self.width()
				height = self.bottom()/self.height()
				x = 0.0
				y = 0.0 - height
				rect = Rectangle(
					(x, y),
					width=width,
					height=height,
					color=color or '#4D4D4D',
					alpha=alpha or 0.95,
					transform=ax.transAxes,
					clip_on=False,
					linewidth=0.0,
					zorder=-5,
				)
				patch = ax.add_patch(rect)
				patches.append(patch)

			self.rect_annotations = patches

	def __repr__(self):
		return f'Axes(width={self.width()}, height={self.height()}, aspect={self.aspect()}, spacing={self.spacing()}'
