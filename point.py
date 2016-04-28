


class Point():

    def __init__(self,x,y,mark=None):
        self.x=x
        self.y=y
        self.mark=mark


    def check_coincident(self, peer_p):

        return (self.x == peer_p.x and self.y == peer_p.y and self.mark == peer_p.mark)

    def shift_point(self, x_shift, y_shift):

        self.x += x_shift
        self.y += y_shift

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.mark == other.mark

    def __str__(self):
        return "x=%f,y=%f,mark=%s"%(self.x,self.y,self.mark)

    def __add__(self, other):
        return Point(self.x+other.x,self.y+other.y,self.mark)

