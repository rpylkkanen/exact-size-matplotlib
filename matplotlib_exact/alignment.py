import matplotlib.pyplot
import numpy
from .axes import Axes
from matplotlib.lines import Line2D

class Alignment:

  def __init__(self, nrows, ncols):

    self._nrows = nrows
    self._ncols = ncols

    self._figure = matplotlib.pyplot.figure()

    self._left, self._right, self._top, self._bottom = [], [], [], []

    self._array = numpy.empty(shape=(nrows, ncols), dtype=object)
    
    for row_idx, row in enumerate(self.array()):
      for col_idx, value in (enumerate(row)):

        value = Axes(self)
        self.array()[row_idx][col_idx] = value
        
        if row_idx in [0]:            
          self._top.append(value)
        
        if row_idx == (nrows - 1):     
          self._bottom.append(value)
        
        if col_idx in [0]:            
          self._left.append(value)
        
        if col_idx == (len(row) - 1): 
          self._right.append(value)

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


  def annotate_rect(self, x=0.5, y=0.5, ls=':', lw=1, color='k', alpha=0.5):
    fig = self.figure()
    # | 
    fig.add_artist(Line2D(
      [x, x], 
      [0.0, 1.0], 
      ls=ls, 
      lw=lw, 
      color=color,
      alpha=alpha,
    ))
    fig.add_artist(Line2D(
      [0.0, 1.0], 
      [y, y], 
      ls=ls, 
      lw=lw, 
      color=color, 
      alpha=alpha)
    )

  def annotate_text(self, x=0.5, y=0.5, fontsize='xx-small', bgcolor='white', bgalpha=0.5):
    fig = self.figure()
    fig_w, fig_h = fig.get_size_inches()
    text = f'Figure:\n{fig_w:.1f}x{fig_h:.1f}"'
    fig.text(
      x,
      y, 
      text,
      ha='center', 
      va='center', 
      fontsize=fontsize, 
      bbox=dict(
        fc='white', 
        alpha=0.5)
      )  

  def __repr__(self):
    return f'Alignment({self.array()})'

  def __len__(self):
    return self.array().__len__()

  def __getitem__(self, idx):
    return self.array().__getitem__(idx)

  def __iter__(self):
    return self.array().__iter__()

  def flatten(self):
    return self.array().flatten()