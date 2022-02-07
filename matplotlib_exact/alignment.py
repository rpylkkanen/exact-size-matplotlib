import matplotlib.pyplot
import numpy
from .axes import Axes
from matplotlib.lines import Line2D


class Alignment:

  def __init__(self, nrows, ncols, size=None, spacings=None, width=None, height=None, left=None, right=None, top=None, bottom=None, every=None):

    self._figure = matplotlib.pyplot.figure(dpi=200)
    self._nrows = None
    self._ncols = None
    self._left, self._right, self._top, self._bottom = None, None, None, None
    self._array = None
    self.text_annotation = None
    self.rect_annotation = None
    self.post_update_functions = []
    self.reset(nrows, ncols, size=size, spacings=spacings, width=width, height=height, left=left, right=right, top=top, bottom=bottom, every=every)

  def reset(self, nrows, ncols, size=None, spacings=None, width=None, height=None, left=None, right=None, top=None, bottom=None, every=None):

    self.figure().clear()

    if size is not None:
      width, height = size[0], size[1]

    if spacings is not None:
      if hasattr(spacings, '__iter__'):
        left, right, top, bottom = spacings[0], spacings[1], spacings[2], spacings[3]
      else:
        every = spacings

    self._nrows = nrows
    self._ncols = ncols
    self._left, self._right, self._top, self._bottom = [], [], [], []
    self._array = numpy.empty(shape=(nrows, ncols), dtype=object)
    self.calculate_edges()
    self.clear_annotations()
    self.set_sizes(width=width, height=height)
    self.set_spacings(left=left, right=right, top=top, bottom=bottom, every=every)
    self.update()

  def calculate_edges(self):

    self._left, self._right, self._top, self._bottom = [], [], [], []

    for row_idx, row in enumerate(self.array()):

      for col_idx, value in (enumerate(row)):

        if value is None:
          value = Axes(self)
        self.array()[row_idx][col_idx] = value

        if row_idx in [0]:
          self._top.append(value)

        if row_idx == (self.nrows() - 1):
          self._bottom.append(value)

        if col_idx in [0]:
          self._left.append(value)

        if col_idx == (len(row) - 1):
          self._right.append(value)

  def reshape(self, nrows, ncols):
    self._array = numpy.reshape(self.array(), (nrows, ncols))
    self._nrows = nrows
    self._ncols = ncols
    self.calculate_edges()
    self.update()

  def nrows(self):
    return self._nrows

  def ncols(self):
    return self._ncols

  def figure(self):
    return self._figure

  def array(self):
    return self._array

  def left(self):
    return self._left

  def right(self):
    return self._right
  
  def top(self):
    return self._top
  
  def bottom(self):
    return self._bottom

  def array(self):
    return self._array

  def spacing_width(self):
    fig_w = 0.0
    for r, row in enumerate(self):
      row_w = 0.0
      for c, ax in enumerate(row):
        w = ax.spacing_width()
        row_w += w
        if row_w > fig_w:
          fig_w = row_w
    return fig_w

  def spacing_height(self):
    fig_h = 0.0
    for r, row in enumerate(self):
      row_h = 0.0
      for c, ax in enumerate(row):
        h = ax.spacing_height()
        if h > row_h:
          row_h = h
      fig_h += row_h
    return fig_h

  def spacing_size(self):
    return self.spacing_width(), self.spacing_height()

  def figure_width(self):
    fig_w = 0.0
    for r, row in enumerate(self):
      row_w = 0.0
      for c, ax in enumerate(row):
        w = ax.total_width()
        row_w += w
        if row_w > fig_w:
          fig_w = row_w
    return fig_w

  def figure_height(self):
    fig_h = 0.0
    for r, row in enumerate(self):
      row_h = 0.0
      for c, ax in enumerate(row):
        h = ax.total_height()
        if h > row_h:
          row_h = h
      fig_h += row_h
    return fig_h

  def figure_size(self):
    return self.figure_width(), self.figure_height()

  def annotate(self):
    x = 0.75
    if self.nrows() > 1:
      x = (self.nrows() - 1)/self.nrows()
    y = 1 - x
    self.annotate_rect(x=x, y=y)
    self.annotate_text(x=x, y=y)
    for a in self.flatten():
      a.annotate()

  def clear_annotations(self):
    self.clear_text_annotations()
    self.clear_rect_annotations()
    for a in self.flatten():
      a.clear_annotations()

  def clear_rect_annotations(self):
    fig = self.figure()
    if fig and self.rect_annotation:
      for line in self.rect_annotation:
        if line in fig.artists:
          fig.artists.remove(line)
      self.rect_annotation = None

  def clear_text_annotations(self):
    fig = self.figure()
    if fig and self.text_annotation:
      if self.text_annotation in fig.texts:
        fig.texts.remove(self.text_annotation)
      self.text_annotation = None

  def annotate_rect(self, x=0.5, y=0.5, ls=':', lw=1, color='k', alpha=0.5):
    fig = self.figure()
    self.clear_rect_annotations()
    line1 = fig.add_artist(Line2D(
      [x, x], 
      [0.0, 1.0], 
      ls=ls, 
      lw=lw, 
      color=color,
      alpha=alpha,
    ))
    line2 = fig.add_artist(Line2D(
      [0.0, 1.0], 
      [y, y], 
      ls=ls, 
      lw=lw, 
      color=color, 
      alpha=alpha)
    )
    self.rect_annotation = [line1, line2]

  def annotate_text(self, x=0.5, y=0.5, fontsize='xx-small', bgcolor='white', bgalpha=0.5):
    fig = self.figure()
    self.clear_text_annotations()
    fig_w, fig_h = fig.get_size_inches()
    text = f'Figure:\n{fig_w:.2f}x{fig_h:.2f}"'
    text = fig.text(
      x,
      y, 
      text,
      ha='center', 
      va='center', 
      fontsize=fontsize, 
      bbox=dict(
        fc=bgcolor,
        alpha=bgalpha)
      )
    self.text_annotation = text

  def set_leftmost_spacings(self, left=None, right=None, top=None, bottom=None, every=None):
    for a in self.left():
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)

  def set_rightmost_spacings(self, left=None, right=None, top=None, bottom=None, every=None):
    for a in self.right():
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)

  def set_topmost_spacings(self, left=None, right=None, top=None, bottom=None, every=None):
    for a in self.top():
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)

  def set_bottommost_spacings(self, left=None, right=None, top=None, bottom=None, every=None):
    for a in self.bottom():
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)

  def set_spacings(self, left=None, right=None, top=None, bottom=None, every=None):
    for a in self.flatten():
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)

  def set_leftmost_sizes(self, width=None, height=None):
    for a in self.left():
      a.set_size(width=width, height=height)

  def set_rightmost_sizes(self, width=None, height=None):
    for a in self.right():
      a.set_size(width=width, height=height)

  def set_topmost_sizes(self, width=None, height=None):
    for a in self.top():
      a.set_size(width=width, height=height)

  def set_bottommost_sizes(self, width=None, height=None):
    for a in self.bottom():
      a.set_size(width=width, height=height)

  def set_sizes(self, width=None, height=None):
    for a in self.flatten():
      a.set_size(width=width, height=height)

  def set_dpi(self, dpi):
    self.figure().set_dpi(dpi)

  def update(self):
    axes = []
    for a in self.flatten():
      ax = a.matplotlib()
      axes.append(ax)
    if self.text_annotation is not None and self.rect_annotation is not None:
      self.annotate()
    for f in self.post_update_functions:
      f()
    return axes

  def add_rows(self, nrows, size=None, spacings=None, width=None, height=None, left=None, right=None, top=None, bottom=None, every=None):
    rows = self.nrows()
    array = numpy.empty(shape=(nrows, self.ncols()), dtype=object)
    self._array = numpy.concatenate((self.array(), array))
    self._nrows = self.nrows() + nrows
    self.calculate_edges()
    self.update()
    axes = self.array()[rows:]

    if size is not None:
      width, height = size[0], size[1]

    if spacings is not None:
      if hasattr(spacings, '__iter__'):
        left, right, top, bottom = spacings[0], spacings[1], spacings[2], spacings[3]
      else:
        every = spacings

    for a in axes.flatten():
      a.set_size(width=width, height=height)
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)
    return axes

  def add_columns(self, ncols, size=None, spacings=None, width=None, height=None, left=None, right=None, top=None, bottom=None, every=None):
    cols = self.ncols()
    array = numpy.empty(shape=(self.nrows(), ncols), dtype=object)
    self._array = numpy.concatenate((self.array(), array), axis=1)
    self._ncols = self.ncols() + ncols
    self.calculate_edges()
    self.update()
    axes = self.array()[:, cols:]
    if size is not None:
      width, height = size[0], size[1]

    if spacings is not None:
      if hasattr(spacings, '__iter__'):
        left, right, top, bottom = spacings[0], spacings[1], spacings[2], spacings[3]
      else:
        every = spacings

    for a in axes.flatten():
      a.set_size(width=width, height=height)
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)
    return axes

    if size is not None:
      width, height = size[0], size[1]

    if spacings is not None:
      if hasattr(spacings, '__iter__'):
        left, right, top, bottom = spacings[0], spacings[1], spacings[2], spacings[3]
      else:
        every = spacings

    for a in axes.flatten():
      a.set_size(width=width, height=height)
      a.set_spacing(left=left, right=right, top=top, bottom=bottom, every=every)
    return axes

  def __repr__(self):
    return f'Alignment({self.array()})'

  def __len__(self):
    return self.array().__len__()

  def __getitem__(self, idx):
    return self.array().__getitem__(idx)

  def __iter__(self):
    return self.array().__iter__()

  def flatten(self):
    arr = self.array()
    if arr is not None:
      return self.array().flatten()
    else:
      return []