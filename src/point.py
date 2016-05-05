class Point(object):
    def __init__(self,x,y,mark=[]):
        self.x = x
        self.y = y
        self.mark = mark

    #implement magic method to add points (x,y)'s
    def __add__(self,other):
        return Point(self.x + other.x,self.y + other.y)
    def __radd__(self,other):
        return Point(self.x + other, self.y + other)
    def __sub__(self, other):                            #implements self - other
        return Point(self.x - other.x,self.y - other.y)
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __neq__(self,other):
        return self.x != other.x or self.y != other.y

    def patched_coincident(self,point2):
        point1 = (self.x,self.y)

        return utils.check_coincident(point1,point2)

    def patched_shift(self,x_shift,y_shift):
        point = (self.x,self.y)
        self.x,self.y = utils.shift_point(point,x_shift,y_shift)

    #Add an attribute to your Point class that returns an array [x,y]
    def return_array(self):
        arrayy = [self.x,self.y]
        return arrayy


from . import utils