class Spacing:

  def __init__(self, left=None, right=None, top=None, bottom=None):

    self.set_left(left or 0.0)
    self.set_right(right or 0.0)
    self.set_top(top or 0.0)
    self.set_bottom(bottom or 0.0)
  
  def set_left(self, left):
    self._left = left

  def left(self):
    return self._left
  
  def set_right(self, right):
    self._right = right

  def right(self):
    return self._right

  def set_top(self, top):
    self._top = top

  def top(self):
    return self._top

  def set_bottom(self, bottom):
    self._bottom = bottom  

  def bottom(self):
    return self._bottom

  def __repr__(self):
    return f'Spacing(left={self.left()}, right={self.right()}, top={self.top()}, bottom={self.bottom()})'