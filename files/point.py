from . import utils



class Point(object):
  
  def __init__(self, x, y, mark={}):
      self.x = x
      self.y = y
      self.mark = mark
      
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __ne__(self, other):
    return self.x != other.x or self.y != other.y
	
  def __str__(self):
    return ("({0}, {1}").format(self.x, self.y)

  def array(self):
    return [self.x, self.y]
    
  def point_check_coincident(self, test):
    return utils.check_coincident((self.x, self.y), test)
  
  def point_shift_point(self, x_shift, y_shift):
      test = utils.shift_point((self.x, self.y), x_shift, y_shift)
      self.x = utils.getx(test)
      self.y = utils.gety(test)
      
